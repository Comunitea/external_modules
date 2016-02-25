# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015
#    Comunitea Servicios Tecnológicos (http://www.comunitea.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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

from openerp import models, exceptions, _, api, fields
from lxml import etree


class BankingExportSddWizard(models.TransientModel):

    _inherit = "banking.export.sdd.wizard"

    group_by_partner = fields.Boolean("Group by partner")

    @api.model
    def generate_remittance_info_block2(self, parent_node, line, print_line,
                                        gen_args):

        remittance_info_2_91 = etree.SubElement(
            parent_node, 'RmtInf')
        if line.state == 'normal':
            remittance_info_unstructured_2_99 = etree.SubElement(
                remittance_info_2_91, 'Ustrd')
            remittance_info_unstructured_2_99.text = \
                self._prepare_field('Remittance Unstructured Information',
                    "line['communication']", {'line': print_line}, 140,
                    gen_args=gen_args)
        else:
            if not line.struct_communication_type:
                raise exceptions.Warning(
                    _("Missing 'Structured Communication Type' on payment "
                        "line with reference '%s'.")
                    % line.name)
            remittance_info_structured_2_100 = etree.SubElement(
                remittance_info_2_91, 'Strd')
            creditor_ref_information_2_120 = etree.SubElement(
                remittance_info_structured_2_100, 'CdtrRefInf')
            if gen_args.get('pain_flavor') == 'pain.001.001.02':
                creditor_ref_info_type_2_121 = etree.SubElement(
                    creditor_ref_information_2_120, 'CdtrRefTp')
                creditor_ref_info_type_code_2_123 = etree.SubElement(
                    creditor_ref_info_type_2_121, 'Cd')
                creditor_ref_info_type_issuer_2_125 = etree.SubElement(
                    creditor_ref_info_type_2_121, 'Issr')
                creditor_reference_2_126 = etree.SubElement(
                    creditor_ref_information_2_120, 'CdtrRef')
            else:
                creditor_ref_info_type_2_121 = etree.SubElement(
                    creditor_ref_information_2_120, 'Tp')
                creditor_ref_info_type_or_2_122 = etree.SubElement(
                    creditor_ref_info_type_2_121, 'CdOrPrtry')
                creditor_ref_info_type_code_2_123 = etree.SubElement(
                    creditor_ref_info_type_or_2_122, 'Cd')
                creditor_ref_info_type_issuer_2_125 = etree.SubElement(
                    creditor_ref_info_type_2_121, 'Issr')
                creditor_reference_2_126 = etree.SubElement(
                    creditor_ref_information_2_120, 'Ref')

            creditor_ref_info_type_code_2_123.text = 'SCOR'
            creditor_ref_info_type_issuer_2_125.text = \
                line.struct_communication_type
            creditor_reference_2_126.text = \
                self._prepare_field('Creditor Structured Reference',
                    "line['communication']", {'line': print_line}, 35,
                    gen_args=gen_args)
        return True

    @api.multi
    def create_sepa(self):
        """Creates the SEPA Direct Debit file. That's the important code !"""
        if not self[0].group_by_partner:
            return super(BankingExportSddWizard, self).create_sepa()
        else:
            pain_flavor = self.payment_order_ids[0].mode.type.code
            convert_to_ascii = \
                self.payment_order_ids[0].mode.convert_to_ascii
            if pain_flavor == 'pain.008.001.02':
                bic_xml_tag = 'BIC'
                name_maxsize = 70
                root_xml_tag = 'CstmrDrctDbtInitn'
            elif pain_flavor == 'pain.008.001.03':
                bic_xml_tag = 'BICFI'
                name_maxsize = 140
                root_xml_tag = 'CstmrDrctDbtInitn'
            elif pain_flavor == 'pain.008.001.04':
                bic_xml_tag = 'BICFI'
                name_maxsize = 140
                root_xml_tag = 'CstmrDrctDbtInitn'
            else:
                raise Warning(
                    _("Payment Type Code '%s' is not supported. The only "
                      "Payment Type Code supported for SEPA Direct Debit are "
                      "'pain.008.001.02', 'pain.008.001.03' and "
                      "'pain.008.001.04'.") % pain_flavor)
            gen_args = {
                'bic_xml_tag': bic_xml_tag,
                'name_maxsize': name_maxsize,
                'convert_to_ascii': convert_to_ascii,
                'payment_method': 'DD',
                'file_prefix': 'sdd_',
                'pain_flavor': pain_flavor,
                'pain_xsd_file':
                'account_banking_sepa_direct_debit/data/%s.xsd' % pain_flavor,
            }
            pain_ns = {
                'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                None: 'urn:iso:std:iso:20022:tech:xsd:%s' % pain_flavor,
            }
            xml_root = etree.Element('Document', nsmap=pain_ns)
            pain_root = etree.SubElement(xml_root, root_xml_tag)
            # A. Group header
            group_header_1_0, nb_of_transactions_1_6, control_sum_1_7 = \
                self.generate_group_header_block(pain_root, gen_args)
            transactions_count_1_6 = 0
            total_amount = 0.0
            amount_control_sum_1_7 = 0.0
            lines_per_group = {}
            # key = (requested_date, priority, sequence type)
            # value = list of lines as objects
            # Iterate on payment orders
            today = fields.Date.context_today(self)
            for payment_order in self.payment_order_ids:
                total_amount = total_amount + payment_order.total
                # Iterate each payment lines
                for line in payment_order.line_ids:
                    priority = line.priority
                    if payment_order.date_prefered == 'due':
                        requested_date = line.ml_maturity_date or today
                    elif payment_order.date_prefered == 'fixed':
                        requested_date = payment_order.date_scheduled or today
                    else:
                        requested_date = today
                    if not line.mandate_id:
                        raise exceptions.Warning(
                            _("Missing SEPA Direct Debit mandate on the payment "
                              "line with partner '%s' and Invoice ref '%s'.")
                            % (line.partner_id.name,
                               line.ml_inv_ref.number))
                    scheme = line.mandate_id.scheme
                    if line.mandate_id.state != 'valid':
                        raise exceptions.Warning(
                            _("The SEPA Direct Debit mandate with reference '%s' "
                              "for partner '%s' has expired.")
                            % (line.mandate_id.unique_mandate_reference,
                               line.mandate_id.partner_id.name))
                    if line.mandate_id.type == 'oneoff':
                        seq_type = 'OOFF'
                        if line.mandate_id.last_debit_date:
                            raise exceptions.Warning(
                                _("The mandate with reference '%s' for partner "
                                  "'%s' has type set to 'One-Off' and it has a "
                                  "last debit date set to '%s', so we can't use "
                                  "it.")
                                % (line.mandate_id.unique_mandate_reference,
                                   line.mandate_id.partner_id.name,
                                   line.mandate_id.last_debit_date))
                    elif line.mandate_id.type == 'recurrent':
                        seq_type_map = {
                            'recurring': 'RCUR',
                            'first': 'FRST',
                            'final': 'FNAL',
                        }
                        seq_type_label = \
                            line.mandate_id.recurrent_sequence_type
                        assert seq_type_label is not False
                        seq_type = seq_type_map[seq_type_label]
                    key = (requested_date, priority, seq_type, scheme)
                    if key in lines_per_group:
                        lines_per_group[key].append(line)
                    else:
                        lines_per_group[key] = [line]
                    # Write requested_exec_date on 'Payment date' of the pay line
                    if requested_date != line.date:
                        line.date = requested_date

            for (requested_date, priority, sequence_type, scheme), lines in \
                    lines_per_group.items():
                # B. Payment info
                payment_info_2_0, nb_of_transactions_2_4, control_sum_2_5 = \
                    self.generate_start_payment_info_block(
                        pain_root,
                        "self.payment_order_ids[0].reference + '-' + "
                        "sequence_type + '-' + requested_date.replace('-', '')  "
                        "+ '-' + priority",
                        priority, scheme, sequence_type, requested_date, {
                            'self': self,
                            'sequence_type': sequence_type,
                            'priority': priority,
                            'requested_date': requested_date,
                        }, gen_args)

                self.generate_party_block(
                    payment_info_2_0, 'Cdtr', 'B',
                    'self.payment_order_ids[0].mode.bank_id.partner_id.'
                    'name',
                    'self.payment_order_ids[0].mode.bank_id.acc_number',
                    'self.payment_order_ids[0].mode.bank_id.bank.bic or '
                    'self.payment_order_ids[0].mode.bank_id.bank_bic',
                    {'self': self}, gen_args)
                charge_bearer_2_24 = etree.SubElement(payment_info_2_0, 'ChrgBr')
                charge_bearer_2_24.text = self.charge_bearer
                creditor_scheme_identification_2_27 = etree.SubElement(
                    payment_info_2_0, 'CdtrSchmeId')
                self.generate_creditor_scheme_identification(
                    creditor_scheme_identification_2_27,
                    'self.payment_order_ids[0].company_id.'
                    'sepa_creditor_identifier',
                    'SEPA Creditor Identifier', {'self': self}, 'SEPA', gen_args)
                transactions_count_2_4 = 0
                amount_control_sum_2_5 = 0.0

                partner_lines = {}
                for line in lines:
                    key = (line.partner_id.id, line.bank_id.id)
                    if not partner_lines.get(key):
                        transactions_count_1_6 += 1
                        partner_lines[key] = {}
                        partner_lines[key]['name'] = line.name
                        partner_lines[key]['amount_currency'] = \
                            line.amount_currency
                        partner_lines[key]['mandate'] = line.mandate_id
                        partner_lines[key]['line'] = line
                        partner_lines[key]['bank_id'] = line.bank_id
                        partner_lines[key]['communication'] = \
                            line.communication
                    else:
                        partner_lines[key]['name'] += (u", " + line.name)
                        partner_lines[key]['amount_currency'] += \
                            line.amount_currency
                        partner_lines[key]['communication'] += \
                            (u", " + line.communication)

                for record in partner_lines:
                    line = partner_lines[record]
                    transactions_count_2_4 += 1
                    # C. Direct Debit Transaction Info
                    dd_transaction_info_2_28 = etree.SubElement(
                        payment_info_2_0, 'DrctDbtTxInf')
                    payment_identification_2_29 = etree.SubElement(
                        dd_transaction_info_2_28, 'PmtId')
                    end2end_identification_2_31 = etree.SubElement(
                        payment_identification_2_29, 'EndToEndId')
                    end2end_identification_2_31.text = self._prepare_field(
                        'End to End Identification', "line['name']",
                        {'line': line}, 35, gen_args=gen_args)
                    currency_name = self._prepare_field(
                        'Currency Code', 'line.currency.name',
                        {'line': line['line']}, 3, gen_args=gen_args)
                    instructed_amount_2_44 = etree.SubElement(
                        dd_transaction_info_2_28, 'InstdAmt', Ccy=currency_name)
                    instructed_amount_2_44.text = '%.2f' % \
                        line['amount_currency']
                    amount_control_sum_1_7 += line['amount_currency']
                    amount_control_sum_2_5 += line['amount_currency']
                    dd_transaction_2_46 = etree.SubElement(
                        dd_transaction_info_2_28, 'DrctDbtTx')
                    mandate_related_info_2_47 = etree.SubElement(
                        dd_transaction_2_46, 'MndtRltdInf')
                    mandate_identification_2_48 = etree.SubElement(
                        mandate_related_info_2_47, 'MndtId')
                    mandate_identification_2_48.text = self._prepare_field(
                        'Unique Mandate Reference',
                        'line.mandate_id.unique_mandate_reference',
                        {'line': line['line']}, 35, gen_args=gen_args)
                    mandate_signature_date_2_49 = etree.SubElement(
                        mandate_related_info_2_47, 'DtOfSgntr')
                    mandate_signature_date_2_49.text = self._prepare_field(
                        'Mandate Signature Date',
                        'line.mandate_id.signature_date',
                        {'line': line['line']}, 10, gen_args=gen_args)
                    if sequence_type == 'FRST' and (
                            line['mandate'].last_debit_date or
                            not line['mandate'].sepa_migrated):
                        previous_bank = self._get_previous_bank(line['line'])
                        if previous_bank or not line['mandate'].sepa_migrated:
                            amendment_indicator_2_50 = etree.SubElement(
                                mandate_related_info_2_47, 'AmdmntInd')
                            amendment_indicator_2_50.text = 'true'
                            amendment_info_details_2_51 = etree.SubElement(
                                mandate_related_info_2_47, 'AmdmntInfDtls')
                        if previous_bank:
                            if (previous_bank.bank.bic or
                                previous_bank.bank_bic) == \
                                (line['bank_id'].bank.bic or
                                 line['bank_id'].bank_bic):
                                ori_debtor_account_2_57 = etree.SubElement(
                                    amendment_info_details_2_51, 'OrgnlDbtrAcct')
                                ori_debtor_account_id = etree.SubElement(
                                    ori_debtor_account_2_57, 'Id')
                                ori_debtor_account_iban = etree.SubElement(
                                    ori_debtor_account_id, 'IBAN')
                                ori_debtor_account_iban.text = self._validate_iban(
                                    self._prepare_field(
                                        'Original Debtor Account',
                                        'previous_bank.acc_number',
                                        {'previous_bank': previous_bank},
                                        gen_args=gen_args))
                            else:
                                ori_debtor_agent_2_58 = etree.SubElement(
                                    amendment_info_details_2_51, 'OrgnlDbtrAgt')
                                ori_debtor_agent_institution = etree.SubElement(
                                    ori_debtor_agent_2_58, 'FinInstnId')
                                ori_debtor_agent_bic = etree.SubElement(
                                    ori_debtor_agent_institution, bic_xml_tag)
                                ori_debtor_agent_bic.text = self._prepare_field(
                                    'Original Debtor Agent',
                                    'previous_bank.bank.bic or '
                                    'previous_bank.bank_bic',
                                    {'previous_bank': previous_bank},
                                    gen_args=gen_args)
                                ori_debtor_agent_other = etree.SubElement(
                                    ori_debtor_agent_institution, 'Othr')
                                ori_debtor_agent_other_id = etree.SubElement(
                                    ori_debtor_agent_other, 'Id')
                                ori_debtor_agent_other_id.text = 'SMNDA'
                                # SMNDA = Same Mandate New Debtor Agent
                        elif not line['mandate'].sepa_migrated:
                            ori_mandate_identification_2_52 = etree.SubElement(
                                amendment_info_details_2_51, 'OrgnlMndtId')
                            ori_mandate_identification_2_52.text = \
                                self._prepare_field(
                                    'Original Mandate Identification',
                                    'line.mandate_id.'
                                    'original_mandate_identification',
                                    {'line': line['line']},
                                    gen_args=gen_args)
                            ori_creditor_scheme_id_2_53 = etree.SubElement(
                                amendment_info_details_2_51, 'OrgnlCdtrSchmeId')
                            self.generate_creditor_scheme_identification(
                                ori_creditor_scheme_id_2_53,
                                'self.payment_order_ids[0].company_id.'
                                'original_creditor_identifier',
                                'Original Creditor Identifier',
                                {'self': self}, 'SEPA', gen_args)

                    self.generate_party_block(
                        dd_transaction_info_2_28, 'Dbtr', 'C',
                        'line.partner_id.name',
                        'line.bank_id.acc_number',
                        'line.bank_id.bank.bic or '
                        'line.bank_id.bank_bic',
                        {'line': line['line']}, gen_args)

                    self.generate_remittance_info_block2(
                        dd_transaction_info_2_28, line['line'], line, gen_args)

                nb_of_transactions_2_4.text = unicode(transactions_count_2_4)
                control_sum_2_5.text = '%.2f' % amount_control_sum_2_5
            nb_of_transactions_1_6.text = unicode(transactions_count_1_6)
            control_sum_1_7.text = '%.2f' % amount_control_sum_1_7

            return self.finalize_sepa_file_creation(
                xml_root, total_amount, transactions_count_1_6, gen_args)
