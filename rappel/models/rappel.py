# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api, exceptions, _


class Rappel(models.Model):
    _name = 'rappel'
    _description = 'Rappel Model'
    _order = "sequence"

    CALC_MODE = [('fixed', 'Fixed'), ('variable', 'Variable')]
    QTY_TYPE = [('quantity', 'Quantity'), ('value', 'Value')]
    CALC_AMOUNT = [('percent', 'Percent'), ('qty', 'Quantity')]

    name = fields.Char('Concept', size=255, required=True, translate=True)
    type_id = fields.Many2one('rappel.type', 'Type', required=True)
    qty_type = fields.Selection(QTY_TYPE, 'Quantity type', required=True,
                                default='value')
    calc_mode = fields.Selection(CALC_MODE, 'Fixed/Variable', required=True)
    fix_qty = fields.Float('Fix')
    sections = fields.One2many('rappel.section', 'rappel_id')
    global_application = fields.Boolean('Global', default=True)
    product_id = fields.Many2one('product.product', 'Product')
    product_categ_id = fields.Many2one('product.category', 'Category')
    calc_amount = fields.Selection(CALC_AMOUNT, 'Percent/Quantity',
                                   required=True)
    customer_ids = fields.One2many("res.partner.rappel.rel", "rappel_id",
                                   "Customers")
    advice_timing_ids = fields.One2many(
        "rappel.advice.email", "rappel_id", "Email Timing Advice")
    sequence = fields.Integer(default=100)

    @api.constrains('global_application', 'product_id', 'product_categ_id')
    def _check_application(self):
        for rappel in self:
            if not rappel.global_application and not rappel.product_id \
                    and not rappel.product_categ_id:
                raise exceptions.\
                    ValidationError(_('Product and category are empty'))

    @api.multi
    def get_products(self):
        self.ensure_one()
        product_obj = self.env['product.product']
        product_ids = self.env['product.product']
        if not self.global_application:
            if self.product_id:
                product_ids |= self.product_id
            elif self.product_categ_id:
                product_ids |= product_obj.search(
                    [('categ_id', '=', self.product_categ_id.id)])
        else:
            product_ids |= product_obj.search([])
        return [x.id for x in product_ids]

    @api.model
    def compute_rappel(self):
        if not self.ids:
            rappels = self.search([])
        else:
            rappels = self
        rappel_infos = self.env["rappel.current.info"].search([])
        if rappel_infos:
            rappel_infos.unlink()
        for rappel in rappels:
            products = rappel.get_products()
            for customer in rappel.customer_ids:
                period = customer._get_next_period()
                if period:
                    invoice_lines, refund_lines = customer.\
                        _get_invoices(period, products)
                    customer.compute(period, invoice_lines, refund_lines,
                                     tmp_model=True)
        self.env["rappel.current.info"].send_rappel_info_mail()


class RappelSection(models.Model):

    _name = 'rappel.section'
    _description = 'Rappel section model'

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s - %s" % (record.rappel_from,
                                                   record.rappel_until)))

        return result

    rappel_from = fields.Float('From', required=True)
    rappel_until = fields.Float('Until')
    percent = fields.Float('Value', required=True)
    rappel_id = fields.Many2one('rappel', 'Rappel')


class RappelCalculated(models.Model):

    _name = 'rappel.calculated'
    _description = "Rappel computed"

    partner_id = fields.Many2one('res.partner', 'Customer', required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
    quantity = fields.Float(required=True)
    rappel_id = fields.Many2one('rappel', 'Rappel', required=True)
    invoice_id = fields.Many2one("account.invoice", "Invoice", readonly=True)
