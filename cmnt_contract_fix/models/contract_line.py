# Copyright 2023 Comunitea - Javier Colmenero Fernández
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models


class ContractLine(models.Model):
    _inherit = "contract.line"
    
    def _insert_markers(self, first_date_invoiced, last_date_invoiced):
        """
        Sobreescrita dado el caso de que no haya fin de período
        last_date_invoice estará a False y fallara si no se hace el if que
        añado
        """
        self.ensure_one()
        lang_obj = self.env["res.lang"]
        lang = lang_obj.search([("code", "=", self.contract_id.partner_id.lang)])
        date_format = lang.date_format or "%m/%d/%Y"
        name = self.name
        if first_date_invoiced:
            name = name.replace("#START#", first_date_invoiced.strftime(date_format))
        if last_date_invoiced:
            name = name.replace("#END#", last_date_invoiced.strftime(date_format))
        return name