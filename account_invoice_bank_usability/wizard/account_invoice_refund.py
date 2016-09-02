# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, api


class AccountInvoiceRefund(models.TransientModel):
    _inherit = "account.invoice.refund"

    @api.multi
    def compute_refund(self, mode='refund'):
        result = super(AccountInvoiceRefund, self).compute_refund(mode)
        active_ids = self.env.context.get('active_ids')
        if not active_ids:
            return result
        inv_obj = self.env['account.invoice']
        created_inv = [x[2] for x in result['domain']
                       if x[0] == 'id' and x[1] == 'in']
        if created_inv and created_inv[0]:
            orig_invoice = inv_obj.browse(active_ids[0])
            refund_inv_id = created_inv[0][0]
            inv_obj.browse(refund_inv_id).write(
                {'payment_mode_id': orig_invoice.payment_mode_id and
                 orig_invoice.payment_mode_id.id or False,
                 'partner_bank_id': orig_invoice.partner_bank_id and
                 orig_invoice.partner_bank_id.id or False})
                 #'mandate_id': orig_invoice.mandate_id and
                 #orig_invoice.mandate_id.id or False})
        return result
