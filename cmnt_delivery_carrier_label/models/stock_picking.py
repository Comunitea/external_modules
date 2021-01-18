# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, fields, models, api
from odoo.exceptions import UserError
from base64 import b64decode
from odoo.addons import decimal_precision as dp


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_generate_carrier_label(self):
        raise NotImplementedError(
            _("No label is configured for the selected delivery method.")
        )

    carrier_weight = fields.Float()
    carrier_packages = fields.Integer(default=1)
    carrier_service = fields.Many2one('delivery.carrier.service')
    delivered = fields.Boolean()
    payment_on_delivery = fields.Boolean("Payment on delivery", related="sale_id.payment_on_delivery")
    pdo_quantity = fields.Float("PDO amount", digits=dp.get_precision("Product Price"))

    def print_created_labels(self):
        self.ensure_one()

        if not self.carrier_id.account_id.printer:
            raise UserError('Printer not defined')
        labels = self.env['shipping.label'].search([
            ('res_id', '=', self.id),
            ('res_model', '=', 'stock.picking')])
        for label in labels:
            self.carrier_id.account_id.printer.print_document(
                None, b64decode(label.datas), doc_format="raw"
            )

    @api.model
    def create(self, vals):
        res = super(StockPicking, self).create(vals)
        res.onchange_partner_id_or_carrier_id()
        return res

    @api.onchange('partner_id', 'carrier_id')
    def onchange_partner_id_or_carrier_id(self):
        self.ensure_one()

        if self.carrier_id:
            state_id = self.env['res.country.state']
            country_id = self.env['res.country']
            if self.partner_id.state_id.id:
                state_id = self.partner_id.state_id
                country_id = self.partner_id.country_id

            available_services = self.env['delivery.carrier.service'].search([
                ('carrier_id', '=', self.carrier_id.id),
                ('auto_apply', '=', True),
                ('state_ids', 'in', state_id.id)
            ])

            regular_service = self.env['delivery.carrier.service'].search([
                ('carrier_id', '=', self.carrier_id.id),
                ('auto_apply', '=', True),
                ('country_id', '=', country_id.id)
            ]).filtered(lambda x: len(x.state_ids) == 0)

            international_service = self.env['delivery.carrier.service'].search([
                ('carrier_id', '=', self.carrier_id.id),
                ('auto_apply', '=', True),
                ('country_id', '=', None)
            ]).filtered(lambda x: len(x.state_ids) == 0)

            if available_services:
                self.carrier_service = available_services[0].id
            elif regular_service:
                self.carrier_service = regular_service[0].id
            elif international_service:
                self.carrier_service = international_service[0].id
            else:
                self.carrier_service = None

    def check_shipment_status(self):
        return True

    @api.model
    def cron_check_shipment_status(self):
        pickings = self.env['stock.picking'].search([
            ('delivered', '=', False), ('carrier_tracking_ref', '!=', False)
        ])
        for picking in pickings:
            picking.check_shipment_status()

    @api.multi
    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for pick in self:
            pick.write({
                'pdo_quantity': pick.get_pdo_quantity()
            })
        return res

    @api.multi
    def get_pdo_quantity(self):
        for pick in self:
            pickings_total_value = 0.0
            pick._compute_amount_all()
            pickings_total_value += pick.amount_total
            if pick.sale_id and (not pick.sale_id.paid_shipping_picking_id or pick.sale_id.paid_shipping_picking_id == pick):
                pickings_total_value += pick.sale_id.shipping_amount_total
            return pickings_total_value

    @api.multi
    def mark_as_paid_shipping(self):
        for pick in self:
            if pick.sale_id and not pick.sale_id.paid_shipping_picking_id:
                pick.sale_id.paid_shipping_picking_id = pick.id

    @api.multi
    def mark_as_unpaid_shipping(self):
        for pick in self:
            if pick.sale_id and pick.sale_id.paid_shipping_picking_id and pick.sale_id.paid_shipping_picking_id == pick.id:
                sale.paid_shipping_batch_id = None

    @api.multi
    def remove_tracking_info(self):
        for pick in self:
            pick.update({"carrier_tracking_ref": False})

            self.env["ir.attachment"].search(
                [
                    ("name", "=", "Label: {}".format(pick.name)),
                    ("res_id", "=", pick.id),
                    ("res_model", "=", self._name),
                ]
            ).unlink()
        
        if pick.payment_on_delivery:
            pick.mark_as_unpaid_shipping()
