# -*- coding: utf-8 -*-


from odoo import api, models, fields

class PurchaseOrder(models.Model):

    _inherit = ['info.apk', 'purchase.order']
    _name = 'purchase.order'

    @api.model
    def get_modal_info(self, values):
        id = int(values.get('id'))
        purchase_id = self.browse(id)

        res = {'name': purchase_id.name,
               'date_order': purchase_id.date_order,
               'amount_untaxed': purchase_id.amount_untaxed,
               'partner_id': {'id': purchase_id.partner_id.id, 'name': purchase_id.partner_id.name}}
        print(res)
        return res