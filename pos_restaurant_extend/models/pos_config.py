# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
from odoo import api, fields, models, _
from odoo.exceptions import Warning, UserError

import logging
_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    _inherit = 'pos.config'

    service_level = fields.Integer(
        string='Service level',
        default=3,
    )

    service_level_default = fields.Boolean(
        string='Service level default',
        default=True,
        help=_("""If the box is not checked, a pop up will appear asking"""
               """ for the service number with each new order line."""),
    )

    service_level_categories = fields.Many2many(
        comodel_name='pos.category',
        relation="pos_config_pos_category_service_level_rel",
        string='Service level categories',
    )

    receipt_logo = fields.Binary(
        string='Receipt logo',
        help=_('This field holds the image used as image for the point of sale'
               ' receipt'),
    )

    receipt_company_label_1 = fields.Char(
        string='Receipt Company Label 1',
    )

    receipt_company_label_2 = fields.Char(
        string='Receipt Company Label 2',
    )

    receipt_company_vat = fields.Char(
        string='Receipt Company Vat',
    )

    receipt_company_address_1 = fields.Char(
        string='Receipt Company Address 1',
    )

    receipt_company_address_2 = fields.Char(
        string='Receipt Company Address 2',
    )

    receipt_company_phone = fields.Char(
        string='Receipt Company Phone',
    )

    print_address = fields.Boolean("Print custom address")

    @api.depends('floor_ids')
    def _compute_floor_facility_ids(self):
        floor_facility_ids = list()
        for facility in self.floor_ids.mapped('rest_floor_facility'):
            if facility.ref_field.id and facility.line_percentage:
                floor_facility_ids.append({
                    "floor_id": facility.ref_field.id,
                    "line_percentage": facility.line_percentage
                })
        self.floor_facility_ids = json.dumps(floor_facility_ids)

    floor_facility_ids = fields.Binary(
        string='Floor facility',
        default='',
        compute='_compute_floor_facility_ids'
    )

    show_guests_popup = fields.Boolean(
        string='Show guests popup',
        default=True,
    )

    session_close_send = fields.Boolean('Send session inform')
    session_close_partner = fields.Many2one('res.partner', string='Session inform partner')
    iface_not_autoprint_cash = fields.Boolean(string='Not autoprint cash', default=False)

    def get_tables_order_count(self):
        self.ensure_one()
        res = super(PosConfig, self).get_tables_order_count()
        for table in res:
            if table['orders'] > 0:
                domain = [('state', '=', 'draft'), ('table_id', 'in', [table['id']])]
                order_stats = self.env['pos.order'].read_group(domain, ['pos_printed'], 'pos_printed')
                orders_map = dict((s['pos_printed'], s['pos_printed_count']) for s in order_stats)
                if True in orders_map:
                    table['pos_printed'] = (orders_map[True]/table['orders']) * 100
                else:
                    table['pos_printed'] = 0
            else:
                table['pos_printed'] = 0
        return res
