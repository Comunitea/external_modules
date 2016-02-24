# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2015 Pexego Sistemas Informáticos All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@pexego.es>$
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
from openerp import models, fields


class rappel_type(models.Model):

    _name = 'rappel.type'
    _description = 'Rappel Type Model'

    name = fields.Char('Name', size=255, required=True)
    code = fields.Char('Code', size=56)
    product_id = fields.Many2one("product.product", "Rappel product",
                                 required=True, help="Product used to invoice"
                                                     " rappels this type.")
