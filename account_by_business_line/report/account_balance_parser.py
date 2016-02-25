# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 1015
#    Comunitea Servicios Tecnológicos (http://www.comunitea.com)
#    $Omar Castiñeira Saavedra$
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

from openerp.addons.account_financial_report_webkit.report.common_balance_reports import CommonBalanceReportHeaderWebkit

if 'old_get_comparison_details' not in dir(CommonBalanceReportHeaderWebkit):
    CommonBalanceReportHeaderWebkit.old_get_comparison_details = CommonBalanceReportHeaderWebkit._get_comparison_details

def _get_comparison_details(self, data, account_ids, target_move,
                            comparison_filter, index):
    fiscalyear = self._get_info(
        data, "comp%s_fiscalyear_id" % (index,), 'account.fiscalyear')
    start_period = self._get_info(
        data, "comp%s_period_from" % (index,), 'account.period')
    stop_period = self._get_info(
        data, "comp%s_period_to" % (index,), 'account.period')
    start_date = self._get_form_param("comp%s_date_from" % (index,), data)
    stop_date = self._get_form_param("comp%s_date_to" % (index,), data)
    init_balance = self.is_initial_balance_enabled(comparison_filter)

    accounts_by_ids = {}
    comp_params = {}
    details_filter = comparison_filter
    if comparison_filter != 'filter_no':
        start_period, stop_period, start, stop = \
            self._get_start_stop_for_filter(
                comparison_filter, fiscalyear, start_date, stop_date,
                start_period, stop_period)
        if comparison_filter == 'filter_year':
            details_filter = 'filter_no'

        initial_balance_mode = init_balance \
            and self._get_initial_balance_mode(start) or False
        accounts_by_ids = self._get_account_details(
            account_ids, target_move, fiscalyear, details_filter,
        start, stop, initial_balance_mode,
            context=data['form']["used_context"])
        comp_params = {
            'comparison_filter': comparison_filter,
            'fiscalyear': fiscalyear,
            'start': start,
            'stop': stop,
            'initial_balance': init_balance,
            'initial_balance_mode': initial_balance_mode,
        }

    return accounts_by_ids, comp_params

CommonBalanceReportHeaderWebkit._get_comparison_details = _get_comparison_details

if 'old_compute_balance_data' not in dir(CommonBalanceReportHeaderWebkit):
    CommonBalanceReportHeaderWebkit.old_compute_balance_data = CommonBalanceReportHeaderWebkit.compute_balance_data

def compute_balance_data(self, data, filter_report_type=None):
        new_ids = data['form']['account_ids'] or data[
            'form']['chart_account_id']
        max_comparison = self._get_form_param(
            'max_comparison', data, default=0)
        main_filter = self._get_form_param('filter', data, default='filter_no')

        comp_filters, nb_comparisons, comparison_mode = self._comp_filters(
            data, max_comparison)

        fiscalyear = self.get_fiscalyear_br(data)

        start_period = self.get_start_period_br(data)
        stop_period = self.get_end_period_br(data)

        target_move = self._get_form_param('target_move', data, default='all')
        start_date = self._get_form_param('date_from', data)
        stop_date = self._get_form_param('date_to', data)
        chart_account = self._get_chart_account_id_br(data)

        start_period, stop_period, start, stop = \
            self._get_start_stop_for_filter(main_filter, fiscalyear,
                                            start_date, stop_date,
                                            start_period, stop_period)

        init_balance = self.is_initial_balance_enabled(main_filter)
        initial_balance_mode = init_balance and self._get_initial_balance_mode(
            start) or False

        # Retrieving accounts
        account_ids = self.get_all_accounts(
            new_ids, only_type=filter_report_type)

        # get details for each accounts, total of debit / credit / balance
        accounts_by_ids = self._get_account_details(
            account_ids, target_move, fiscalyear, main_filter, start, stop,
            initial_balance_mode, context=data['form']["used_context"])

        comparison_params = []
        comp_accounts_by_ids = []
        for index in range(max_comparison):
            if comp_filters[index] != 'filter_no':
                comparison_result, comp_params = self._get_comparison_details(
                    data, account_ids, target_move, comp_filters[index], index)
                comparison_params.append(comp_params)
                comp_accounts_by_ids.append(comparison_result)

        objects = self.pool.get('account.account').browse(self.cursor,
                                                          self.uid,
                                                          account_ids)

        to_display_accounts = dict.fromkeys(account_ids, True)
        init_balance_accounts = dict.fromkeys(account_ids, False)
        comparisons_accounts = dict.fromkeys(account_ids, [])
        debit_accounts = dict.fromkeys(account_ids, False)
        credit_accounts = dict.fromkeys(account_ids, False)
        balance_accounts = dict.fromkeys(account_ids, False)

        for account in objects:
            if not account.parent_id:  # hide top level account
                continue
            if account.type == 'consolidation':
                to_display_accounts.update(
                    dict([(a.id, False) for a in account.child_consol_ids]))
            elif account.type == 'view':
                to_display_accounts.update(
                    dict([(a.id, True) for a in account.child_id]))
            debit_accounts[account.id] = \
                accounts_by_ids[account.id]['debit']
            credit_accounts[account.id] = \
                accounts_by_ids[account.id]['credit']
            balance_accounts[account.id] = \
                accounts_by_ids[account.id]['balance']
            init_balance_accounts[account.id] =  \
                accounts_by_ids[account.id].get('init_balance', 0.0)

            # if any amount is != 0 in comparisons, we have to display the
            # whole account
            display_account = False
            comp_accounts = []
            for comp_account_by_id in comp_accounts_by_ids:
                values = comp_account_by_id.get(account.id)
                values.update(
                    self._get_diff(account.balance, values['balance']))
                display_account = any((values.get('credit', 0.0),
                                       values.get('debit', 0.0),
                                       values.get('balance', 0.0),
                                       values.get('init_balance', 0.0)))
                comp_accounts.append(values)
            comparisons_accounts[account.id] = comp_accounts
            # we have to display the account if a comparison as an amount or
            # if we have an amount in the main column
            # we set it as a property to let the data in the report if someone
            # want to use it in a custom report
            display_account = display_account\
                or any((debit_accounts[account.id],
                        credit_accounts[account.id],
                        balance_accounts[account.id],
                        init_balance_accounts[account.id]))
            to_display_accounts.update(
                {account.id: display_account and
                 to_display_accounts[account.id]})

        context_report_values = {
            'fiscalyear': fiscalyear,
            'start_date': start_date,
            'stop_date': stop_date,
            'start_period': start_period,
            'stop_period': stop_period,
            'chart_account': chart_account,
            'comparison_mode': comparison_mode,
            'nb_comparison': nb_comparisons,
            'initial_balance': init_balance,
            'initial_balance_mode': initial_balance_mode,
            'comp_params': comparison_params,
            'to_display_accounts': to_display_accounts,
            'init_balance_accounts': init_balance_accounts,
            'comparisons_accounts': comparisons_accounts,
            'debit_accounts': debit_accounts,
            'credit_accounts': credit_accounts,
            'balance_accounts': balance_accounts,
        }

        return objects, new_ids, context_report_values

CommonBalanceReportHeaderWebkit.compute_balance_data = compute_balance_data
