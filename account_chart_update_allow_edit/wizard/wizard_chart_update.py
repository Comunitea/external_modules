# Copyright 2019 Omar Castiñeira <omar@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class WizardUpdateChartsAccountsTax(models.TransientModel):
    _inherit = 'wizard.update.charts.accounts.tax'

    type = fields.Selection(readonly=False)


class WizardUpdateChartsAccountsAccount(models.TransientModel):
    _inherit = 'wizard.update.charts.accounts.account'

    type = fields.Selection(readonly=False)


class WizardUpdateChartsAccountsFiscalPosition(models.TransientModel):
    _inherit = 'wizard.update.charts.accounts.fiscal.position'

    type = fields.Selection(readonly=False)
