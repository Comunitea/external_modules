# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True, uid=1, context={})
def migrate(env, version):
    payment_mode_type = env.ref(
        'account_banking_sepa_direct_debit.export_sdd_008_001_02')
    payment_modes = env['payment.mode'].search(
        [('type', '=', payment_mode_type.id)])
    invoices = env['account.invoice'].search(
        [('payment_mode_id', 'in', payment_modes.ids),
         ('mandate_id', '=', False),
         ('state', 'in', ('draft', 'open'))])
    for invoice in invoices:
        if invoice.partner_id.commercial_partner_id.bank_ids:
            bank = invoice.partner_id.commercial_partner_id.bank_ids[0]
            invoice.mandate_id = bank.mandate_ids and bank.mandate_ids[0] or False
