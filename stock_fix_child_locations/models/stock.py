# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning


class StockMove(models.Model):

    _inherit = 'stock.move'

    def action_done(self, cr, uid, ids, context=None):
        for move in self.browse(cr, uid, ids, context=context):
            if len(move.location_dest_id.child_ids) and not \
                    len(move.linked_move_operation_ids) and not \
                    context.get('ignore_child', False):
                raise Warning(_('Location Error'), _('Location %s has child locations. \
The movements should be at an end location') % move.location_dest_id.name)
            for link in move.linked_move_operation_ids:
                if len(link.operation_id.location_dest_id.child_ids):
                    raise Warning(_('Location Error'), _('Location %s has child locations. \
The movements should be at an end location') % move.location_dest_id.name)
        return super(StockMove, self).action_done(cr, uid, ids, context)
