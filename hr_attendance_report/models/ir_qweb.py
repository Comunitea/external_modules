# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 Comunitea All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@comunitea.com>$
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

from openerp import models, fields, api, exceptions, _
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT


class QwebWidgetDate(models.AbstractModel):
    _name = 'ir.qweb.widget.date'
    _inherit = 'ir.qweb.widget'

    def _format(self, inner, options, qwebcontext):
        inner = self.pool['ir.qweb'].eval(inner, qwebcontext)
        inner_date = datetime.strptime(inner, DATE_FORMAT).date()
        lang_code = qwebcontext.context.get('lang') or 'en_US'
        lang_id = self.pool.get('res.lang').search(
            qwebcontext.cr, qwebcontext.uid, [('code', '=', lang_code)])
        date_format = self.pool.get('res.lang').read(
            qwebcontext.cr, qwebcontext.uid, lang_id, ['date_format'])
        return inner_date.strftime(date_format[0]['date_format'])


class QwebWidgetTime(models.AbstractModel):
    _name = 'ir.qweb.widget.time'
    _inherit = 'ir.qweb.widget'

    def _format(self, inner, options, qwebcontext):
        inner = self.pool['ir.qweb'].eval(inner, qwebcontext)
        if isinstance(inner, str):
            inner = float(inner)
        return '%02d:%02d' % (int(inner), (inner - int(inner)) * 60)
