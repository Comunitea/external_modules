# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Pexego All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@pexego.es>$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import except_orm
from openerp.addons.stock_account.wizard.stock_invoice_onshipping \
    import JOURNAL_TYPE_MAP

class FastReturn(models.TransientModel):

    _name = 'fast.return'

    @api.model
    def _get_journal(self):
        journal_obj = self.env['account.journal']
        journal_type = self._get_journal_type()
        journals = journal_obj.search([('type', '=', journal_type)])
        return journals and journals[0] or False

    @api.model
    def _get_journal_type(self):
        return JOURNAL_TYPE_MAP.get(('incoming', 'customer'), ['sale_refund'])[0]

    journal_id = fields.Many2one('account.journal', 'Destination Journal',
                                 required=True, default=_get_journal)
    journal_type = fields.Selection(
        [('purchase_refund', 'Refund Purchase'),
         ('purchase', 'Create Supplier Invoice'),
         ('sale_refund', 'Refund Sale'), ('sale', 'Create Customer Invoice')],
        'Journal Type', readonly=True, default=_get_journal_type)

    @api.multi
    def fast_return(self):
        pickings = self.env['stock.picking'].browse(self.env.context['active_ids'])
        picking_ids = pickings.fast_returns()
        self.create_invoice(picking_ids)

        data_pool = self.env['ir.model.data']

        #action_id = data_pool.xmlid_to_res_id('stock.action_picking_tree_ready')

        # Return the next view: Show 'done' view
        #
        model_data_ids = data_pool.search([
            ('model', '=', 'ir.ui.view'),
            ('module', '=', 'stock'),
            ('name', '=', 'vpicktree')
        ])
        model_data_form_ids = data_pool.search([
            ('model', '=', 'ir.ui.view'),
            ('module', '=', 'stock'),
            ('name', '=', 'view_picking_form')
        ])

        resource_id = model_data_ids.read(fields=['res_id'])[0]['res_id']
        resource_form_id = model_data_form_ids.read(fields=['res_id'])[0]['res_id']

        return {
            'name': _("New return pickings"),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(resource_id, 'tree'), (resource_form_id, 'form')],
            'domain': "[('id','in', ["+','.join(map(str, picking_ids))+"])]",
            'context': self.env.context,
            'target': 'current',
        }

        # if action_id:
        #     action_pool = self.env['ir.actions.act_window']
        #     action = action_pool.read(self.env.cr, self.env.uid, action_id)
        #     action['domain'] = "[('id','in', ["+','.join(map(str, picking_ids))+"])]"
        #     return action
        # return True

    def create_invoice(self, pickings):
        picks = self.env['stock.picking'].browse(pickings)
        pick_ids = [p.id for p in picks if p.invoice_state == '2binvoiced'
                    and p.partner_id.invoice_method == 'a']
        print pick_ids
        if pick_ids:
            invoice_wzd_vals = {
                'journal_id': self.journal_id.id,
                'journal_type': self.journal_type,
                'group': False,
                'invoice_date': False
            }
            invoice_wzd = self.env['stock.invoice.onshipping'].create(
                invoice_wzd_vals)
            invoice_ids = invoice_wzd.with_context(active_ids=pick_ids).create_invoice()
            invoices = self.env['account.invoice'].browse(invoice_ids)
            for invoice in invoices:
                rect_inv_id = invoice.picking_ids[0].move_lines[0].\
                    origin_returned_move_id.picking_id.invoice_ids[0].id
                print "Factura recitificada"
                print rect_inv_id
                vals = {'origin_invoices_ids': [(6, 0, [rect_inv_id,])]}
                print vals
                invoice.write(vals)
            invoices.signal_workflow('invoice_open')
