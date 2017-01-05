# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class ResPartner(models.Model):

    _inherit = 'res.partner'

    partner_type_id = fields.Many2one('partner.type',
                                      string="Partner Type")

    @api.model
    def create(self, vals):
        if vals.get('partner_type_id', False):
            p_type = self.env['partner.type'].browse(vals['partner_type_id'])
            if not vals.get('ref', False):
                seq_id = p_type.sequence_id.id
                vals.update(ref=self.env['ir.sequence'].next_by_id(seq_id))
        res = super(ResPartner, self).create(vals)
        return res

    @api.multi
    def write(self, vals):
        for partner in self:
            if vals.get('partner_type_id', False) and \
                    not vals.get('ref', False) and not partner.ref:
                p_type = self.env['partner.type'].\
                    browse(vals['partner_type_id'])
                # If parent contact we take the parent reference:
                new_ref = False
                if partner.parent_id:
                    new_ref = partner.parent_id.ref
                else:
                    seq_id = p_type.sequence_id.id
                    new_ref = self.env['ir.sequence'].next_by_id(seq_id)
                vals.update(ref=new_ref)
        res = super(ResPartner, self).write(vals)
        return res


class PartnerType(models.Model):

    _name = 'partner.type'

    name = fields.Char('Name', required=True)
    sequence_id = fields.Many2one('ir.sequence',
                                  string="Sequence")
