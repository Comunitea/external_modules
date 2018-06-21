# -*- coding: utf-8 -*-
# Copyright (C) 2013 Julius Network Solutions SARL <contact@julius.fr>
# Copyright (C) 2015 credativ ltd. <info@credativ.co.uk>
# Copyright 2017 Omar Castiñeira, Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, exceptions, _


class ProductTag(models.Model):
    _description = 'Product Tags'
    _name = "product.tag"

    name = fields.Char('Tag Name', required=True, translate=True)
    active = fields.Boolean(help='The active field allows you to hide the '
                                 'tag without removing it.', default=True)
    parent_id = fields.Many2one(string='Parent Tag',
                                comodel_name='product.tag', index=True,
                                ondelete='cascade')
    child_ids = fields.One2many(string='Child Tags',
                                comodel_name='product.tag',
                                inverse_name='parent_id')
    parent_left = fields.Integer('Left Parent', index=True)
    parent_right = fields.Integer('Right Parent', index=True)

    image = fields.Binary('Image')

    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise exceptions.\
                ValidationError(_('Error! You can not create recursive tags.'))

    @api.multi
    def name_get(self):
        res = []
        for tag in self:
            names = []
            current = tag
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((tag.id, u' / '.join(reversed(names))))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        return self.search(args, limit=limit).name_get()


class ProductTemplate(models.Model):
    _inherit = "product.template"

    tag_ids = fields.Many2many(string='Tags',
                               comodel_name='product.tag',
                               relation='product_product_tag_rel',
                               column1='tag_id',
                               column2='product_id')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
