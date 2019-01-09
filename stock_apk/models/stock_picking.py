# -*- coding: utf-8 -*-
# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, models, fields


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    def xml_rpc_action_done(self, values):
        ids = values.get('ids', [])
        picking_ids = self.browse(ids)
        return picking_ids.action_done()


