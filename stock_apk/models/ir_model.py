# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class IrModel(models.Model):
    _inherit = 'ir.model'


    @api.model
    def search_read_obj(self, domain=None, fields=None, offset=0, limit=None, order=None):

        records = self.search(domain or [], offset=offset, limit=limit, order=order)
        if not records:
            return []
        res = []
        for record in records:
            val = {}
            for f in fields:
                field = fields[f]
                if record._fields['state'].type == 'selection':
                    val[field] = record._fields['state'].convert_to_export('cancel', record)
                else:
                    val[field] = record[field]
            res.append(val)
        return res



