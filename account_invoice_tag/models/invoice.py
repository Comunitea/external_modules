# -*- coding: utf-8 -*-
# Copyright 2017 Omar Castiñeira, Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    tag_ids = fields.Many2many("account.invoice.tag",
                               'account_invoice_tag_rel', 'invoice_id',
                               'tag_id', string='Tags')
