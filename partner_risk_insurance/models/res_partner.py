
# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

# V8 CODE
# from openerp import models, fields, api


# class ResPartner(models.Model):
#     _inherit = 'res.partner'

#     @api.one
#     @api.depends('company_credit_limit', 'insurance_credit_limit')
#     def _credit_limit(self):
#         self.credit_limit = (self.company_credit_limit +
#                              self.insurance_credit_limit)

#     credit_limit = fields.Float('Credit Limit', store=True,
#                                 compute=_credit_limit)
#     company_credit_limit = fields.Float("Company's Credit Limit",
#                                         help='Credit limit granted by the '
#                                         'company.')
#     insurance_credit_limit = fields.Float("Insurance's Credit Limit",
#                                           help='Credit limit granted by the '
#                                           'insurance company.')
#     risk_insurance_coverage_percent = fields.Float(
#         "Insurance's Credit Coverage", help='Percentage of the credit covered '
#         'by the insurance.')
#     risk_insurance_requested = fields.Boolean(
#         'Insurance Requested', help='Mark this field if an insurance was '
#         'requested for the credit of this partner.')
#     risk_insurance_grant_date = fields.Date('Insurance Grant Date',
#                                             help='Date when the insurance was '
#                                             'granted by the insurance company.'
#                                             )
#     risk_insurance_code = fields.Char('Insurance Code',
#                                       help='Code assigned to this partner by '
#                                       'the risk insurance company.')
#     risk_insurance_code_2 = fields.Char('Insurance Code 2',
#                                         help='Secondary code assigned to this '
#                                         'partner by the risk insurance '
#                                         'company.')

from openerp.osv import orm, fields

# Pedro module code.
RISK_STATUS = [('company_granted', 'Credit granted by the company'),
               ('insurance_granted', 'Credit granted by the insurance'),
               ('requested', 'Insurance requested'), 
               ('request_again', 'Insurance credit should be requested again'), 
               ('denied', 'Credit denied by the insurance company'), 
               ('incidents', 'Customer with incidents at risk'), 
               ('new_customer', 'Warning! New customer - See payments')]


class res_partner(orm.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    def _credit_limit(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for partner in self.browse(cr, uid, ids, context):
            if partner.risk_insurance_status in ('company_granted'):                
                res[partner.id] = partner.company_credit_limit
            elif partner.risk_insurance_status in ('insurance_granted'):
                res[partner.id] = partner.insurance_credit_limit
            else:
                res[partner.id] = 0.0
        return res

    _columns = {
        'credit_limit': fields.function(_credit_limit, method=True, store=False, string='Credit Limit', type='float'),
        'company_credit_limit': fields.property(type='float',
                                                string="Company's Credit Limit", 
                                                help='Credit limit granted by the company.'),
        'insurance_credit_limit': fields.property(type='float',
                                                  string="Insurance's Credit Limit",
                                                  help='Credit limit granted by the insurance company.'),
        'risk_insurance_coverage_percent': fields.property(type='float',
                                                           string="Insurance's Credit Coverage",
                                                           help='Percentage of the credit covered by the insurance.'),
        'risk_insurance_status': fields.selection(RISK_STATUS, 'Risk Status', required=True,
                                                  help="This option is used to define the risk status.\n" \
                                                  "Credit granted by the company: Only company's credit limit are applied.\n"\
                                                  "Credit granted by the insurance: Only insurance's credit limit are applied.\n"\
                                                  "Insurance requested: The risk has been requested to the insurance company.\n"\
                                                  "Insurance credit should be requested again: The risk should be requested again to the insurance company.\n"\
                                                  "Credit denied by the insurance company: The insurance company has denied the risk.\n"\
                                                  "Customer with incidents at risk: The customer have incidents at risk.\n"\
                                                  "Warning! New customer - See payments: New customer. Track payments."),
        'risk_insurance_grant_date': fields.property(type='date',
                                                     string="Insurance Grant Date",
                                                     help='Date when the insurance was granted by the insurance company.'),
        'risk_insurance_code': fields.property(type='char',
                                               string="Insurance Code",
                                               help='Code assigned to this partner by the risk insurance company.'),
        'risk_insurance_code_2': fields.property(type='char',
                                                 string="Insurance Code 2",
                                                 help='Secondary code assigned to this partner by the risk insurance company.'),
        'risk_insurance_notes': fields.property(type='text',
                                                string="Notes"),
    }
    _defaults = {
        'risk_insurance_status': 'new_customer',
    }
