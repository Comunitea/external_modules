# Part of Odoo. See LICENSE file for full copyright and licensing details.
import pytz
from odoo import fields, models, api, _
from odoo.osv.expression import AND
from odoo.exceptions import AccessDenied
from datetime import timedelta
from odoo.addons.point_of_sale.wizard.pos_box import PosBox


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    position = fields.Integer('Service')
    table_id = fields.Many2one(related="order_id.table_id")
    note = fields.Char()


class PosOrder(models.Model):
    _inherit = 'pos.order'

    pos_printed = fields.Boolean(default=False)
    last_requested_service = fields.Integer('Last requested service')
    has_notes = fields.Boolean('Has notes', compute='_compute_has_notes')

    def _compute_has_notes(self):
        for order in self:
            order.has_notes = any(l.note != '' for l in order.lines)

    def _prepare_mail_values(self, name, message, client, receipt):
        res = super()._prepare_mail_values(name, message, client, receipt)
        # Cambiar email
        if (res['email_from'] == self.env.user.email_formatted and
                self.env.user.company_id):
            res['email_from'] = self.env.user.company_id.email_formatted
        return res

    def _get_fields_for_order_line(self):
        res = super(PosOrder, self)._get_fields_for_order_line()
        res.append('position')
        res.append('table_id')
        return res

    def _get_fields_for_draft_order(self):
        res = super(PosOrder, self)._get_fields_for_draft_order()
        res.append('pos_printed')
        res.append('last_requested_service')
        return res

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        order_fields['pos_printed'] = ui_order.get('pos_printed', False)
        order_fields['last_requested_service'] = (
            ui_order.get('last_requested_service', False)
        )
        return order_fields

    def _export_for_ui(self, order):
        result = super(PosOrder, self)._export_for_ui(order)
        result['pos_printed'] = order.pos_printed
        result['last_requested_service'] = order.last_requested_service
        return result

    def write(self, vals):
        for order in self:
            if vals.get('state') and vals['state'] == 'paid' and order.\
                    config_id.iface_l10n_es_simplified_invoice and (
                    not order.is_l10n_es_simplified_invoice and not vals.
                    get('is_l10n_es_simplified_invoice')) and \
                    (not vals.get('account_move') and not order.account_move):
                vals['is_l10n_es_simplified_invoice'] = True
                vals['l10n_es_unique_id'] = order.config_id.\
                    l10n_es_simplified_invoice_sequence_id._next()
        return super(PosOrder, self).write(vals)

    @api.model
    def _process_order(self, order, draft, existing_order):
        order_data = order['data']
        pos_session = self.env['pos.session'].browse(
            order_data['pos_session_id']
        )
        if (pos_session.state == 'closing_control' or
                pos_session.state == 'closed'):
            raise AccessDenied(_("NO PUEDES CREAR SESIONES DE RESCATE"))
        return super()._process_order(order, draft, existing_order)


class ReportSaleDetails(models.AbstractModel):
    _inherit = 'report.point_of_sale.report_saledetails'

    @api.model
    def get_sale_details(self, date_start=False, date_stop=False,
                         config_ids=False, session_ids=False):
        data = super().\
            get_sale_details(date_start=date_start, date_stop=date_stop,
                             config_ids=config_ids, session_ids=session_ids)
        domain = [('state', 'in', ['paid', 'invoiced', 'done'])]

        if (session_ids):
            domain = AND([domain, [('session_id', 'in', session_ids)]])
        else:
            if date_start:
                date_start = fields.Datetime.from_string(date_start)
            else:
                # start by default today 00:00:00
                user_tz = pytz.timezone(self.env.context.get('tz') or self.
                                        env.user.tz or 'UTC')
                today = user_tz.localize(fields.Datetime.
                                         from_string(fields.Date.
                                                     context_today(self)))
                date_start = today.astimezone(pytz.timezone('UTC'))

            if date_stop:
                date_stop = fields.Datetime.from_string(date_stop)
                # avoid a date_stop smaller than date_start
                if (date_stop < date_start):
                    date_stop = date_start + timedelta(days=1, seconds=-1)
            else:
                # stop by default today 23:59:59
                date_stop = date_start + timedelta(days=1, seconds=-1)

            domain = AND([domain,
                          [('date_order', '>=',
                            fields.Datetime.to_string(date_start)),
                           ('date_order', '<=',
                            fields.Datetime.to_string(date_stop))]])

            if config_ids:
                domain = AND([domain, [('config_id', 'in', config_ids)]])

        orders = self.env['pos.order'].search(domain)
        attendeees = 0
        for order in orders:
            sign = 1
            if order.amount_total < 0.0:
                sign = -1
            attendeees += (sign * order.customer_count)
        sessions = orders.mapped('session_id')
        statements = self.env['account.bank.statement'].\
            search([('pos_session_id', 'in', sessions.ids)])
        manual_lines = statements.mapped('line_ids').\
            filtered(lambda x: not x.payment_ref.startswith('POS'))

        data.update({'sessions': sessions,
                     'total_attendees': attendeees,
                     'orders_count': len(orders),
                     'manual_statements': manual_lines})

        return data


class PosBoxOut(PosBox):
    _inherit = 'cash.box.out'

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        res_id = self._context.get('active_id')
        res_model = self._context.get('active_model')
        if res_model == 'pos.session' and self._context.get('cash_out_proposal'):
            session = self.env['pos.session'].browse(res_id)
            res.update({
                'name': _("Cash out proposal"),
                'amount': -session.cash_register_total_entry_encoding,
            })
        return res


class PosSession(models.Model):
    _inherit = "pos.session"

    def _compute_average_customer_price(self):
        for session in self:
            media = 0
            session.average_customer_price = 0
            for order in session.order_ids:
                if not order.customer_count:
                    media += round(order.amount_total, 2)
                else:
                    media += round(order.amount_total / order.customer_count, 2)
            if len(session.order_ids):
                session.average_customer_price = (
                    round(media / len(session.order_ids), 2)
                )

    average_customer_price = fields.Float(
        string='Average Ticket', readonly=True,
        compute='_compute_average_customer_price')

    def action_open_session_details(self):
        self.ensure_one()
        wzd = self.env['pos.details.wizard'].\
            create({'start_date': self.start_at,
                    'end_date': self.stop_at,
                    'pos_config_ids': [(6, 0, [self.config_id.id])]})

        return {
            'name': _('Sales Details'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pos.details.wizard',
            'view_id':
            self.env.ref('point_of_sale.view_pos_details_wizard').id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': wzd.id,
        }

    def action_pos_session_validate(self):
        res = super().action_pos_session_validate()
        if (self.config_id.session_close_send and self.config_id.
                session_close_partner):
            report_view = self.env["ir.actions.report"]._get_report_from_name(
                "pos_report_session_summary.report_session_summary"
            )

            pdf_report = (
                report_view.sudo()._render_qweb_pdf([self.id])[0] or False
            )

            attachment = [
                (
                    "resumen_caja.pdf",
                    pdf_report,
                )
            ]

            self.message_post(
                body="Resumen de la sesión TPV del día de hoy.",
                subject="Resumen sesión TPV",
                message_type='email',
                subtype_xmlid='mail.mt_comment',
                email_layout_xmlid='mail.mail_notification_light',
                attachments=attachment,
                partner_ids=self.config_id.session_close_partner.ids,
            )
        return res

    def _create_account_move(self):
        ctx = self.env.context.copy()
        ctx.update({
            'force_open_date': self.start_at,
        })
        return super(PosSession, self.with_context(ctx))._create_account_move()


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def create(self, vals):
        if self.env.context.get('force_open_date', False):
            vals['date'] = self.env.context.get('force_open_date', False).date()
        return super(AccountMove, self).create(vals)
