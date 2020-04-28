# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, fields, models, api
from odoo.exceptions import UserError
from base64 import b64decode


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_generate_carrier_label(self):
        raise NotImplementedError(
            _("No label is configured for the selected delivery method.")
        )

    carrier_weight = fields.Float()
    carrier_packages = fields.Integer(default=1)
    carrier_service = fields.Many2one('delivery.carrier.service')

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
