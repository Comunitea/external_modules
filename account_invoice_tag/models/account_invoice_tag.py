# -*- coding: utf-8 -*-
# Copyright 2017 Omar Castiñeira, Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountInvoiceTag(models.Model):

    _name = "account.invoice.tag"

    name = fields.Char("Tag Name", required=True, translate=True)
    active = fields.Boolean("Active", default=True,
                            help="The active field allows you to hide the "
                                 "tag without removing it.")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
