# -*- coding: utf-8 -*-


from odoo import api, models, fields

class SaleOrder(models.Model):

    _inherit = ['info.apk', 'sale.order']
    _name = 'sale.order'

    @api.model
    def get_modal_info(self, values):
        id = int(values.get('id'))
        sale_id = self.browse(id)

        res = {'name': sale_id.name,
               'date_order': sale_id.date_order,
               'amount_untaxed': sale_id.amount_untaxed,
               'partner_id': {'id': sale_id.partner_shipping_id.id, 'name': sale_id.partner_shipping_id.name}}
        return res