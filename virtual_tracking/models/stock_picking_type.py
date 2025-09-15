# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models

class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    bypass_tracking = fields.Boolean("By pass tracking")
    check_serial_qties = fields.Boolean("Check Qties with Serial Numbers")
    bypass_serial_error_location = fields.Boolean("By pass Location/Error")