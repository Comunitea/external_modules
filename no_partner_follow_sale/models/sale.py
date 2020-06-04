# -*- coding: utf-8 -*-
# © 2019 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # @api.model
    # def create(self, vals, **kwargs):
    #     """
    #     Esto no funciona a pesar de que la clave está bien
    #     """
    #     ctx = dict(self._context, mail_create_nosubscribe=True)
    #     return super(SaleOrder, self.with_context(ctx)).create(
    #         vals, **kwargs)

    @api.multi
    def action_confirm(self):
        """
        Al confirmar paso una nueva clave para que no me añada el partner
        como seguidor
        """
        ctx = dict(self._context, disable_message_subscribe=True)
        res = super(SaleOrder, self.with_context(ctx)).\
            action_confirm()
        return res

    @api.multi
    def message_subscribe(self, partner_ids=None, channel_ids=None, 
                          subtype_ids=None, force=True):
        if self._context.get('disable_message_subscribe'):
            return True
        else:
            return super(SaleOrder, self).message_subscribe(
                partner_ids, subtype_ids=subtype_ids)

    # @api.model
    # def _message_get_auto_subscribe_fields(
    #         self, updated_fields, auto_follow_fields=None):
    #     """
    #     Esto eliminaría cualquier seguidor, incluso el comercial al crear
    #     factura
    #     """
    #     return []