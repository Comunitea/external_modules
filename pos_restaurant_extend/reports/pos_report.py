
from unittest import result
from odoo import api, fields, models, tools


class PosSessionReport(models.Model):
    _name = "report.pos.session"
    _description = "Point of Sale Session Report"
    _auto = False
    _order = 'date desc'

    table_count = fields.Integer(string='Tables', group_operator="count")
    customer_count = fields.Integer(string='Guests', help='The amount of customers that have been served by this order.', group_operator="sum")
    average_customer_price = fields.Float(
        string='Average Ticket', readonly=True, group_operator="avg")

    date = fields.Datetime(string='Order Date', readonly=True)
    order_id = fields.Many2one('pos.order', string='Order', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    state = fields.Selection(
        [('draft', 'New'), ('paid', 'Paid'), ('done', 'Posted'),
         ('invoiced', 'Invoiced'), ('cancel', 'Cancelled')],
        string='Status')
    user_id = fields.Many2one('res.users', string='User', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    journal_id = fields.Many2one('account.journal', string='Journal')
    delay_validation = fields.Integer(string='Delay Validation')
    invoiced = fields.Boolean(readonly=True)
    config_id = fields.Many2one('pos.config', string='Point of Sale', readonly=True)
    session_id = fields.Many2one('pos.session', string='Session', readonly=True)
    amount_total = fields.Float(string='Total', digits=0, readonly=True)
    employee_id = fields.Many2one(
                'hr.employee', string='Employee', readonly=True)

    def _select(self):
        return """
            SELECT
                MIN(s.id) AS id,
                s.date_order AS date,
                SUM(cast(to_char(date_trunc('day',s.date_order) - date_trunc('day',s.create_date),'DD') AS INT)) AS delay_validation,
                s.customer_count AS customer_count,
                count(s.table_id) AS table_count,
                 CASE 
                     WHEN s.amount_total = 0 THEN NULL
                     ELSE ROUND(avg(s.amount_total/CASE COALESCE (s.customer_count,0)WHEN 0 THEN 1 ELSE s.customer_count END),2)
                END AS average_customer_price,
                s.id as order_id,
                s.partner_id AS partner_id,
                s.state AS state,
                s.user_id AS user_id,
                s.company_id AS company_id,
                s.sale_journal AS journal_id,
                ps.config_id,
                s.pricelist_id,
                s.session_id,
                s.account_move IS NOT NULL AS invoiced,
                s.amount_total AS amount_total,
                s.employee_id AS employee_id

        """

    def _from(self):
        return """
            FROM pos_order AS s
                INNER JOIN pos_session ps ON (s.session_id=ps.id)
                LEFT JOIN res_company co ON (s.company_id=co.id)
                LEFT JOIN res_currency cu ON (co.currency_id=cu.id)
        """

    def _group_by(self):
        return """
            GROUP BY
                s.id, s.date_order, s.partner_id,s.state,
                s.user_id, s.company_id, s.sale_journal,
                s.pricelist_id, s.account_move, s.create_date, s.session_id,
                ps.config_id, s.employee_id
        """

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s
            )
        """ % (self._table, self._select(), self._from(), self._group_by())
        )