# -*- coding: utf-8 -*-
# © 2015 Pexego Sistemas Informáticos
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
import csv
from odoo.tools import pycompat
import base64
import io
import re
from odoo import models, fields, api, _


class AccountAdminToolsImporter(models.TransientModel):
    """
    Account Importer

    Creates accounts from a CSV file.

    The CSV file lines are expected to have at least the code and name of the
    account.

    The wizard will find the account brothers (or parent) having the same
    account code sufix, and will autocomplete the rest of the account
    parameters (account type, reconcile, parent account...).

    The CSV file lines are tested to be valid account lines using the regular
    expresion options of the wizard.
    """
    _name = "account.admin.tools.importer"
    _description = "Account importation wizard"

    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 default=lambda self:
                                     self.env.user.company_id.id)
    overwrite = fields.Boolean(
        'Overwrite', help="If the account already exists, overwrite its name?")

    file = fields.Binary(filters="*.csv", required=True)
    csv_delimiter = fields.Char('Delimiter', size=1, required=True,
                                default=';')
    csv_quotechar = fields.Char('Quote', size=1, required=True, default='"')
    csv_code_index = fields.Integer('Code field', required=True, default=0)
    csv_code_regexp = fields.Char('Code regexp', size=32, required=True,
                                  default=r'^[0-9]+$')
    csv_name_index = fields.Integer('Name field', required=True, default=1)
    csv_name_regexp = fields.Char('Name regexp', size=32, required=True,
                                  default=r'^.*$')

    @api.multi
    def _find_brother_account_id(self, account_code):
        """
        Finds a brother account given an account code.
        It will remove the last digit of the code until it finds an
        account that matches the begin of the code.
        """
        if len(account_code) > 0:
            brother_account_code = account_code[:-1]
            while len(brother_account_code) > 0:
                accounts = self.env['account.account'].search(
                    [('code', '=like', brother_account_code + '%%'),
                     ('company_id', '=', self.company_id.id)])
                if accounts:
                    return accounts[0]
                brother_account_code = brother_account_code[:-1]
        return None

    @api.multi
    def action_import(self):
        """
        Imports the accounts from the CSV file using the options from the
        wizard.
        """
        # List of the imported accounts
        imported_accounts = self.env['account.account']

        logger = logging.getLogger("account_importer")

        csv_data = base64.b64decode(self.file)
        csv_data = csv_data.decode('utf-8').encode('utf-8')
        reader = pycompat.csv_reader(
            io.BytesIO(csv_data),
            delimiter=str(self.csv_delimiter),
            quotechar=str(self.csv_quotechar))

        for record in reader:
            # Ignore short records
            if len(record) > self.csv_code_index \
                    and len(record) > self.csv_name_index:

                record_code = record[self.csv_code_index]
                record_name = record[self.csv_name_index]

                #
                # Ignore invalid records
                #
                if re.match(self.csv_code_regexp, record_code) and \
                        re.match(self.csv_name_regexp, record_name):

                    accounts = self.env['account.account'].search(
                        [('code', '=', record_code),
                         ('company_id', '=', self.company_id.id)])
                    if accounts:
                        if self.overwrite:
                            logger.debug("Overwriting account: %s %s" %
                                         (record_code, record_name))
                            accounts.write({'name': record_name})
                            imported_accounts += accounts
                    else:
                        brother_account = self._find_brother_account_id(
                            record_code)

                        if not brother_account:
                            logger.warning("Couldn't find a\
                                brother account for: %s" % record_code)

                        logger.debug("Creating new account:\
                            %s %s" % (record_code, record_name))
                        account = self.env['account.account'].create(
                            {
                                'code': record_code,
                                'name': record_name,
                                'internal_type': brother_account.internal_type,
                                'user_type_id':
                                    brother_account.user_type_id.id,
                                'reconcile': brother_account.reconcile,
                                'company_id': self.company_id.id,
                                'currency_id': brother_account.currency_id.id,
                                'tax_ids': [(6, 0, [tax.id for
                                                    tax in
                                                    brother_account.tax_ids])],
                                'note': False,
                            })

                        imported_accounts += account
                else:
                    logger.warning("Invalid record format\
                        (ignoring line): %s" % repr(record))
            else:
                logger.warning("Too short record \
                        (ignoring line): %s" % repr(record))

        account_view = self.env.ref('account.view_account_form')
        return {
            'name': _("Imported accounts"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.account',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(False, 'tree'), (account_view.id, 'form')],
            'domain': "[('id', 'in', %s)]" % str(imported_accounts._ids),
            'context': self.env.context,
        }
