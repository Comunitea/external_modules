# -*- coding: utf-8 -*-
# Copyright 2017 Omar Castiñeira, Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):

    _inherit = "res.partner"


    @api.multi
    def _count_partners_by_type(self):
        for partner in self.filtered(lambda x: x.parent_id):
            domain = [('parent_id', '=', partner.parent_id.id), ('type', '=', partner.type)]
            partner.count_partners_by_type = self.search_count(domain) - 1

    default_partner_by_type = fields.Boolean("Default partner by type", default=False, copy=False)
    count_partners_by_type = fields.Integer('Count partners by type', compute="_count_partners_by_type")

    @api.multi
    @api.constrains("parent_id", "type", "default_partner_by_type")
    def _check_default_partner_by_type(self):
        """Ensure details are given if required."""
        for partner in self:
            domain = (('parent_id', '=', partner.parent_id.id), ('type', '=', partner.type), ('default_partner_by_type','=',True))
            if partner.search_count(domain) > 1:
                raise ValidationError (_('Only one default by partner type for each child'))

    @api.multi
    def address_get(self, adr_pref=None):
        # Se cambia solo el to_scan para añadir un sorted, pero tengo que heredear toda la función
        """ Find contacts/addresses of the right type(s) by doing a depth-first-search
        through descendants within company boundaries (stop at entities flagged ``is_company``)
        then continuing the search at the ancestors that are within the same company boundaries.
        Defaults to partners of type ``'default'`` when the exact type is not found, or to the
        provided partner itself if no type ``'default'`` is found either. """
        adr_pref = set(adr_pref or [])
        if 'contact' not in adr_pref:
            adr_pref.add('contact')
        result = {}
        visited = set()
        for partner in self:
            current_partner = partner
            while current_partner:
                to_scan = [current_partner]
                # Scan descendants, DFS
                while to_scan:
                    record = to_scan.pop(0)
                    visited.add(record)
                    if record.type in adr_pref and not result.get(record.type):
                        result[record.type] = record.id
                    if len(result) == len(adr_pref):
                        return result
                    # to_scan = [c for c in record.child_ids
                    # Se cambia solo el para añadir un sorted
                    to_scan = [c for c in record.child_ids.sorted(
                        key=lambda r: (r.type and -4 or 0) + (r.default_partner_by_type and -2 or 0) + (
                                    r.display_name and -1))
                               if c not in visited
                               if not c.is_company] + to_scan

                # Continue scanning at ancestor if current_partner is not a commercial entity
                if current_partner.is_company or not current_partner.parent_id:
                    break
                current_partner = current_partner.parent_id

        # default to type 'contact' or the partner itself
        default = result.get('contact', self.id or False)
        for adr_type in adr_pref:
            result[adr_type] = result.get(adr_type) or default
        return result

    def set_as_default(self):
        if self.parent_id and not self.default_partner_by_type:
            domain = (('id','!=', self.id), ('parent_id', '=', self.parent_id.id), ('type', '=', self.type), ('default_partner_by_type', '=', True))
            not_defaults = self.search(domain)
            if not_defaults:
                not_defaults.write({'default_partner_by_type': False})
        self.default_partner_by_type = not self.default_partner_by_type
