# © 2024 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError, UserError

class StockQuant(models.Model):
    _inherit = "stock.quant"


    def check_location_id(self):
        if self.env.context.get('skip_check_location_id'):
            return True
        return super().check_location_id()

