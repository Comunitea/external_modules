from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _get_fields_for_order_line(self):
        res = super(PosOrder, self)._get_fields_for_order_line()
        res.append('selected_attribute_value_ids')
        return res


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    selected_attribute_value_ids = fields.Char('Attribute IDs')