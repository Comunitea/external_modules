# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import time
import logging
from odoo.tools import pycompat
import base64
import io
import re
from odoo import models, fields, api, _, exceptions


class AccountAdminToolsMoveImporter(models.TransientModel):
    """
    Account Move Importer

    Wizard that imports a CSV file into a new account move.

    The CSV file is expected to have at least the account code, a reference
    (description of the move line), the debit and the credit.

    The lines of the CSV file are tested to be valid account move lines
    using the regular expresions set on the wizard.
    """
    _name = "account.admin.tools.move.importer"
    _description = "Account move importation wizard"

    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 default=lambda self:
                                     self.env.user.company_id.id)
    ref = fields.Char('Ref', size=64, required=True)
    journal_id = fields.Many2one('account.journal', 'Journal', required=True)
    date = fields.Date('Date', required=True,
                       default=lambda * a: time.strftime('%Y-%m-%d'))

    input_file = fields.Binary('File', filters="*.csv", required=True)
    csv_delimiter = fields.Char('Delimiter', size=1, required=True,
                                default=';')
    csv_quotechar = fields.Char('Quote', size=1, required=True, default='"')
    csv_decimal_separator = fields.Char('Decimal sep.', size=1, required=True,
                                        default='.')
    csv_thousands_separator = fields.Char('Thousands sep.', size=1,
                                          required=True, default=',')
    csv_code_index = fields.Integer('Code field', required=True, default=0)
    csv_code_regexp = fields.Char('Code regexp', size=32, required=True,
                                  default=r'^[0-9]+$')
    csv_ref_index = fields.Integer('Ref field', required=True, default=1)
    csv_ref_regexp = fields.Char('Ref regexp', size=32, required=True,
                                 default=r'^.*$')
    csv_debit_index = fields.Integer('Debit field', required=True, default=2)
    csv_debit_regexp = fields.Char('Debit regexp', size=32, required=True,
                                   default=r'^[0-9\-\.\,]*$')
    csv_credit_index = fields.Integer('Credit field', required=True, default=3)
    csv_credit_regexp = fields.Char('Credit regexp', size=32, required=True,
                                    default=r'^[0-9\-\.\,]*$')
    csv_partner_ref_index = fields.Integer('Partner Ref field', required=True,
                                           default=4)
    csv_partner_ref_regexp = fields.Char('Partner Ref regexp', size=32,
                                         required=True, default=r'^.*$')

    @api.multi
    def _get_default_ref_field(self):
        """ This method set the default value to ref field in res.partner
             model for the oerp_partner_ref_field field
             @return: return default value
         """
        default_model_field = self.env['ir.model.fields'].search(
            [('model', '=', 'res.partner'), ('name', '=', 'ref')])
        return default_model_field

    oerp_partner_ref_field = fields.Many2one(
        'ir.model.fields', 'Odoo Partner field', required=True,
        domain=[('model', '=', 'res.partner'), '|', '|',
                ('ttype', '=', 'char'),
                ('ttype', '=', 'text'), ('ttype', '=', 'many2one')],
        default=_get_default_ref_field)

    @api.model
    def _get_accounts_map(self):
        """
        Find the receivable/payable accounts that are associated with
        a single partner and return a (account.id, partner.id) map
        """
        accounts_map = {}
        for partner in self.env['res.partner'].search([]):
            if partner.property_account_receivable_id.id not in accounts_map:
                accounts_map[
                    partner.property_account_receivable_id.id] = partner.id
            else:
                accounts_map.pop(partner.property_account_receivable_id.id)

            if partner.property_account_payable_id.id not in accounts_map:
                accounts_map[partner.property_account_payable_id.id] = \
                    partner.id
            else:
                accounts_map.pop(partner.property_account_payable_id.id)
        return accounts_map

    @api.multi
    def action_import(self):
        """
        Imports a CSV file into a new account move using the options from
        the wizard.
        """
        accounts_map = self._get_accounts_map()
        logger = logging.getLogger("account_move_importer")

        account_move_data = self.env['account.move'].default_get(
            ['state', 'name'])
        account_move_data.update({
            'ref': self.ref,
            'journal_id': self.journal_id.id,
            'date': self.date,
            'line_ids': [],
            'partner_id': False,
        })

        lines_data = account_move_data['line_ids']

        csv_data = base64.b64decode(self.input_file)
        csv_data = csv_data.decode('utf-8').encode('utf-8')
        reader = pycompat.csv_reader(
            io.BytesIO(csv_data),
            delimiter=str(self.csv_delimiter),
            quotechar=str(self.csv_quotechar))

        for record in reader:
            # Ignore short records
            if self.csv_partner_ref_index \
                    and len(record) > self.csv_code_index \
                    and len(record) > self.csv_ref_index \
                    and len(record) > self.csv_debit_index \
                    and len(record) > self.csv_credit_index:

                record_code = record[self.csv_code_index]
                record_ref = record[self.csv_ref_index]
                record_debit = record[self.csv_debit_index]
                record_credit = record[self.csv_credit_index]
                record_partner_ref = False

                if len(record) > self.csv_partner_ref_index:
                    record_partner_ref = record[self.csv_partner_ref_index]

                # Ignore invalid records
                if re.match(self.csv_code_regexp, record_code) \
                        and re.match(self.csv_ref_regexp, record_ref) \
                        and re.match(self.csv_debit_regexp, record_debit) \
                        and re.match(self.csv_credit_regexp, record_credit):

                    # Clean the input amounts
                    record_debit = float(
                        record_debit.replace(self.csv_thousands_separator,
                                             '').replace(
                                             self.csv_decimal_separator, '.'))
                    record_credit = float(record_credit.replace(
                        self.csv_thousands_separator, '').replace(
                        self.csv_decimal_separator, '.'))

                    accounts = self.env['account.account'].search(
                        [('code', '=', record_code),
                         ('company_id', '=', self.company_id.id)])
                    if not accounts:
                        raise exceptions.Warning(
                            _("Account not found: %s!") % record_code)

                    partner = False
                    if record_partner_ref and \
                            re.match(self.csv_partner_ref_regexp,
                                     record_partner_ref):
                        partner = self.env['res.partner'].search(
                            [(self.oerp_partner_ref_field.name, '=',
                              record_partner_ref)])

                    line_data = {
                        'account_id': accounts[0].id,
                        'name': record_ref,
                        'partner_id': partner and partner[0].id or
                        accounts_map.get(accounts[0].id, False),
                    }

                    #
                    # Create a debit line + a credit line if needed
                    #
                    line_data_debit = line_data.copy()
                    line_data_credit = line_data
                    if record_debit != 0.0:
                        line_data_debit['debit'] = record_debit
                        lines_data.append((0, 0, line_data_debit))
                    if record_credit != 0.0:
                        line_data_credit['credit'] = record_credit
                        lines_data.append((0, 0, line_data_credit))
                else:
                    logger.warning("Invalid record format\
                                    (ignoring line): %s" % repr(record))
            else:
                logger.warning("Too short record\
                    (ignoring line): %s" % repr(record))
        move = self.env['account.move'].create(account_move_data)

        next_view = self.env.ref('account.view_move_form')
        return {
            'name': _("Imported account moves"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_type': 'form',
            'view_mode': 'form, tree',
            'views': [(False, 'tree'), (next_view.id, 'form')],
            'domain': "[('id', '=', %s)]" % move.id,
            'context': self._context,
        }
