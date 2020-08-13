# # Copyright (C) 2019 - Comunitea
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# from odoo import fields, models, api, _
# from odoo.exceptions import ValidationError, UserError
# import datetime
# from dateutil.relativedelta import relativedelta



# class ContractContract(models.Model):
#     _inherit = "contract.contract"
    
#     # FIX!! OVERWRITE PORQUE EL MODULO DE SALE_CONTRACT_INVOICING NO
#     # TIENE EN CUENTA QUE ES API MULTI, TODO PR A OCA
#     # @api.multi
#     # def _recurring_create_invoice(self, date_ref=False):
#     #     # CODIGO DE SALE_CONTRACT_INVOICING CON BUCLE (FIX OCA BUG)
#     #     for contract in self:
#     #         if not contract.invoicing_sales:
#     #             continue
#     #         sales = self.env['sale.order'].search([
#     #             ('analytic_account_id', '=', contract.group_id.id),
#     #             ('partner_invoice_id', 'child_of',
#     #             contract.partner_id.commercial_partner_id.ids),
#     #             ('invoice_status', '=', 'to invoice'),
#     #             ('date_order', '<=',
#     #             '{} 23:59:59'.format(contract.recurring_next_date)),
#     #         ])
#     #         if sales:
#     #             invoice_ids = sales.action_invoice_create()
#     #             invoices |= self.env['account.invoice'].browse(invoice_ids)[:1]
#         # return invoices
    
#     # OVERWRITE API MULTI
#     # si hacemos la accion de servidor pueden venir mas de uno.
#     @api.multi
#     def recurring_create_invoice(self):
#         """
#         This method triggers the creation of the next invoices of the contracts
#         even if their next invoicing date is in the future.
#         """
#         invoice = self._recurring_create_invoice()
#         for inv in invoice:
#             inv.message_post(
#                 body=_(
#                     'Contract manually invoiced: '
#                     '<a href="#" data-oe-model="%s" data-oe-id="%s">Invoice'
#                     '</a>'
#                 )
#                 % (inv._name, inv.id)
#             )
#         return invoice
    
#     @api.multi
#     # OVERWRITE, NOT INVOICE TO RENE
#     def _get_lines_to_invoice(self, date_ref):
#         """
#         Sobreescrito para quitar también los cerrados.
#         Sino el cron los factura también
#         """
#         self.ensure_one()
#         return self.contract_line_ids.filtered(
#             lambda l: not l.is_canceled and
#             not l.state == 'closed'
#             and l.recurring_next_date
#             and l.recurring_next_date <= date_ref
#         )
    
#     # OTRO FIX PARA PORUQE AL IR EL NEW SIN COMPAÑÍA, 
#     # ENTRA EN EL ONCHANGE DE ACCOUNT_PAYMENT_PARTNER CON LA FACTURA SIN 
#     # COMPAÑÍA, AL HACER EL CUSTOMER_payment_mode CON FORCE COMPANY A FALSE
#     # DEVUELVE LA COMPAÑÍA 1, Y SERÁ ERROR DE PERMISOS
#     @api.multi
#     def _prepare_invoice(self, date_invoice, journal=None):
#         import ipdb; ipdb.set_trace()
#         self.ensure_one()
#         if not journal:
#             journal = (
#                 self.journal_id
#                 if self.journal_id.type == self.contract_type
#                 else self.env['account.journal'].search(
#                     [
#                         ('type', '=', self.contract_type),
#                         ('company_id', '=', self.company_id.id),
#                     ],
#                     limit=1,
#                 )
#             )
#         if not journal:
#             raise ValidationError(
#                 _("Please define a %s journal for the company '%s'.")
#                 % (self.contract_type, self.company_id.name or '')
#             )
#         currency = (
#             self.pricelist_id.currency_id
#             or self.partner_id.property_product_pricelist.currency_id
#             or self.company_id.currency_id
#         )
#         invoice_type = 'out_invoice'
#         if self.contract_type == 'purchase':
#             invoice_type = 'in_invoice'
#         vinvoice = self.env['account.invoice'].with_context(
#             force_company=self.company_id.id,
#         ).new({
#             'partner_id': self.invoice_partner_id.id,
#             'type': invoice_type,
#             'company_id': self.company_id.id,  # ESTE ES EL FIX
#         })
#         vinvoice._onchange_partner_id()
#         invoice_vals = vinvoice._convert_to_write(vinvoice._cache)
#         invoice_vals.update({
#             'name': self.code,
#             'currency_id': currency.id,
#             'date_invoice': date_invoice,
#             'journal_id': journal.id,
#             'origin': self.name,
#             'company_id': self.company_id.id,
#             'user_id': self.user_id.id,
#         })
#         if self.payment_term_id:
#             invoice_vals['payment_term_id'] = self.payment_term_id.id
#         if self.fiscal_position_id:
#             invoice_vals['fiscal_position_id'] = self.fiscal_position_id.id
#         return invoice_vals
    
# class ContractLine(models.Model):
#     _inherit = "contract.line"

    
#     def _get_period_to_invoice(self, last_date_invoiced, recurring_next_date, 
#                                stop_at_date_end=True):
#         """
#         Esta función se va a eliminar, pero si next_period_date_end
#         da False porque el proyecto está cerrado hay que fallar. 
#         """
#         import ipdb; ipdb.set_trace()
#         res = super()._get_period_to_invoice(
#             last_date_invoiced, recurring_next_date, 
#             stop_at_date_end=stop_at_date_end)
        
#         if res[1] == False:
#             raise ValidationError(
#                     _("No hay siguiente fecha de fin de periodo. \
#                       Revise la fecha fin")
#                 )
#         return res
    
#     # FIX!!! overwrited NO INVOICE IF NOT NEXT RECURRING INTERVAL
#     @api.depends('recurring_next_date', 'date_start', 'date_end')
#     def _compute_create_invoice_visibility(self):
#         """
#         Si dejo crear factura sin next_period_date_end, falla en la
#         función de insert markers y en la de update recurring invoice date,
#         no espera esta situación
#         """
#         import ipdb; ipdb.set_trace()
#         today = fields.Date.context_today(self)
#         for rec in self:
#             # ADDED AND Rec.next_period_date_end
#             if rec.date_start and rec.next_period_date_end:
#                 if today < rec.date_start:
#                     rec.create_invoice_visibility = False
#                 else:
#                     rec.create_invoice_visibility = bool(
#                         rec.recurring_next_date
#                     )

 
      
# # FIX BUG NO ME DEJA SUPRIMIR UNA LINEA SI HE USADO EL ASISTENTE POR CULPA DEL
# # REQUIRED
# class ContractLineWizard(models.TransientModel):

#     _inherit = 'contract.line.wizard'
#     contract_line_id = fields.Many2one(
#         comodel_name="contract.line",
#         string="Contract Line",
#         required=False,
#         index=True,
#     )