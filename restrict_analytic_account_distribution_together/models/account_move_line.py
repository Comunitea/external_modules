from odoo import models, exceptions, _


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    def create_analytic_lines(self):
        for obj_line in self:
            if obj_line.analytic_tag_ids.\
                    filtered('active_analytic_distribution') and obj_line.\
                    analytic_account_id:
                raise exceptions.UserError(
                    _("Cannot coexists in the same line analytic distributions"
                      " and analytic account. Please select only one "
                      "imputation mode"))
        super().create_analytic_lines()
