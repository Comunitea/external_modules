# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import Warning, UserError

import logging
_logger = logging.getLogger(__name__)


class FacilityRestaurant(models.Model):
    _inherit = "restaurant.floor"

    rest_floor_facility = fields.One2many(
        comodel_name='restaurant.floor.line',
        inverse_name='ref_field',
        string='Floor Facility',
    )

    facility_service_percentage = fields.Float(
        compute='onchange_rest_facility',
        string="Active Facility Charge %",
    )

    @api.depends('rest_floor_facility')
    def onchange_rest_facility(self):
        for rec in self:
            sum_of_percentage = 0.0
            if rec.rest_floor_facility:
                for records in rec.rest_floor_facility:
                    sum_of_percentage += records.line_percentage
            rec.facility_service_percentage = sum_of_percentage


class FacilityRestaurantLines(models.Model):
    _name = "restaurant.floor.line"

    name = fields.Many2one(
        comodel_name='restaurant.floor.facility',
    )

    line_percentage = fields.Float(
        string="Extra Charging Percentage",
    )

    ref_field = fields.Many2one(
        comodel_name='restaurant.floor',
        invisible=True,
        ondelete='cascade',
    )

    @api.onchange('name')
    def onchange_facility(self):
        if self.name:
            self.line_percentage = self.name.percentage


class FloorFacility(models.Model):
    _name = "restaurant.floor.facility"

    name = fields.Char(
        string="Name",
        required=True,
    )

    percentage = fields.Float(
        string="Extra Charging Percentage(%)",
        required=True,
        help="Increment percentage of the each Product Price",
    )

    description = fields.Html(
        string="Description",
    )
