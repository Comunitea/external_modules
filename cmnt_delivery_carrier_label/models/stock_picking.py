# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, fields, models
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
