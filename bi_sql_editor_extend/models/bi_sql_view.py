# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from datetime import datetime
from psycopg2 import ProgrammingError

from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.tools import pycompat, sql
from odoo.addons.base.models.ir_model import IrModel

_logger = logging.getLogger(__name__)


class BiSQLView(models.Model):
    _inherit = 'bi.sql.view'

    _STATE_SQL_EDITOR = [
        ('fields_edition', 'Edición campos')
    ]

    state = fields.Selection(selection_add=_STATE_SQL_EDITOR)

    @api.multi
    def button_fields_edition(self):
        self.state = 'fields_edition'

    def button_update_fields(self):

        self._drop_view()
        if self._clean_query_enabled:
            self._clean_query()
        if self._check_prohibited_words_enabled:
            self._check_prohibited_words()
        if self._check_execution_enabled:
            self._check_execution()
        self._create_view()

    @api.multi
    def button_update_or_create_fields(self):
        for sql_view in self:
            sql_view.menu_id.unlink()
            sql_view.action_id.unlink()
            sql_view.tree_view_id.unlink()
            sql_view.graph_view_id.unlink()
            sql_view.pivot_view_id.unlink()
            sql_view.search_view_id.unlink()
        self._update_or_create_fields()

    @api.multi
    def _update_or_create_fields(self):
        self.ensure_one()

        model_id = self.model_id
        for field in self.bi_sql_view_field_ids.filtered(
                lambda x: x.field_description is not False):
            model_field = model_id.field_id.filtered(lambda x: x.name == field.name)
            if model_field:
                model_field.write(field._prepare_model_field())
            else:
                vals = field._prepare_model_field()
                vals['model_id'] = model_id.id
                self.env['ir.model.fields'].create(vals)

        self.state = 'model_valid'

