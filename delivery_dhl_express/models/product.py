##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2022 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
#    Vicente Ángel Gutiérrez <vicente@comunitea.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import _, models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    dhl_express_code = fields.Char('DHL Express Code')
    dhl_express_description = fields.Char('DHL Express Description')
    dhl_express_measurement = fields.Selection([
        ('BOX', 'BOX'),
        ('2GM', '2GM'),
        ('2M', '2M'),
        ('2M3', '2M3'),
        ('3M3', '3M3'),
        ('M3', 'M3'),
        ('DPR', 'DPR'),
        ('DOZ', 'DOZ'),
        ('2NO', '2NO'),
        ('PCS', 'PCS'),
        ('GM', 'GM'),
        ('GRS', 'GRS'),
        ('KG', 'KG'),
        ('L', 'L'),
        ('M', 'M'),
        ('3GM', '3GM'),
        ('3L', '3L'),
        ('X', 'X'),
        ('NO', 'NO'),
        ('2KG', '2KG'),
        ('PRS', 'PRS'),
        ('2L', '2L'),
        ('3KG', '3KG'),
        ('CM2', 'CM2'),
        ('2M2', '2M2'),
        ('3M2', '3M2'),
        ('M2', 'M2'),
        ('4M2', '4M2'),
        ('3M', '3M'),
    ], string='DHL EXpress Mesurement', default="PCS")
    dhl_service_type = fields.Selection([
        ('discount', 'Discount'),
        ('delivery', 'Delivery'),
        ('other', 'Other'),
    ], string='DHL Service type')
