# Copyright 2019 Omar Castiñeira <omar@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, _
import logging

_logger = logging.getLogger(__name__)


class WizardUpdateChartsAccounts(models.TransientModel):
    _inherit = 'wizard.update.charts.accounts'

    def _update_taxes(self):
        """Process taxes to create/update/deactivate."""
        for wiz_tax in self.tax_ids.filtered(lambda x: x.type != 'new'):
            template, tax = wiz_tax.tax_id, wiz_tax.update_tax_id
            # Deactivate tax
            if wiz_tax.type == 'deleted':
                tax.active = False
                _logger.info(_("Deactivated tax %s."), "'%s'" % tax.name)
                continue
            for key, value in self.diff_fields(template, tax).items():
                # We defer update because account might not be created yet
                if key in {'account_id', 'refund_account_id'}:
                    continue
                tax[key] = value
                _logger.info(_("Updated tax %s."), "'%s'" % template.name)
            if self.recreate_xml_ids and self.missing_xml_id(tax):
                self.recreate_xml_id(template, tax)
                _logger.info(_("Updated tax %s. (Recreated XML-IDs)"),
                             "'%s'" % template.name)
        new_templates = self.tax_ids.filtered(lambda x: x.type == 'new').\
            mapped('tax_id')
        if new_templates:
            new_templates._generate_tax(self.company_id)


class WizardUpdateChartsAccountsTax(models.TransientModel):
    _inherit = 'wizard.update.charts.accounts.tax'

    type = fields.Selection(readonly=False)


class WizardUpdateChartsAccountsAccount(models.TransientModel):
    _inherit = 'wizard.update.charts.accounts.account'

    type = fields.Selection(readonly=False)


class WizardUpdateChartsAccountsFiscalPosition(models.TransientModel):
    _inherit = 'wizard.update.charts.accounts.fiscal.position'

    type = fields.Selection(readonly=False)
