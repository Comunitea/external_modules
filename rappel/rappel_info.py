# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Comunitea Servicios Tecnológicos All Rights Reserved
#    $Omar Castiñeira Saaevdra <omar@comunitea.com>$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from openerp import models, fields, _, api
from datetime import datetime
from dateutil import relativedelta
from openerp import exceptions


class RappelAdvices(models.Model):

    _name="rappel.advice.email"

    ADVICE_TIMING = [('fixed', 'Days to finish'), ('variable', '% Periodo')]

    rappel_id = fields.Many2one("rappel", "Rappel", required=True)
    advice_timing = fields.Selection(ADVICE_TIMING, "Fixed/Variable", required = True,
         help="fixed: days to finish, % days" )
    timing = fields.Integer("Value", required = True)

    @api.one
    @api.constrains('advice_timing', 'timing')
    def check_timing(self):
        if self.advice_timing == 'variable':
            if self.timing <=0 or self.timing >=100:
                raise exceptions.\
                    ValidationError (_("Timing must be between 0 and 100 %"))




class RappelCurrentInfo(models.Model):

    _name = "rappel.current.info"

    CALC_MODE = [('fixed', 'Fixed'), ('variable', 'Variable')]
    QTY_TYPE = [('quantity', 'Quantity'), ('value', 'Value')]
    CALC_AMOUNT = [('percent', 'Percent'), ('qty', 'Quantity')]

    rappel_id = fields.Many2one("rappel", "Rappel", required=True)
    partner_id = fields.Many2one("res.partner", "Customer", required=True)
    date_start = fields.Date("Start date", required=True)
    date_end = fields.Date("End date", required=True)
    amount = fields.Float("Current Amount", default = 0)
    qty_type = fields.Selection(QTY_TYPE, 'Quantity type', readonly=True,
                                related="rappel_id.qty_type")
    calc_mode = fields.Selection(CALC_MODE, 'Fixed/Variable', readonly=True,
                                 related="rappel_id.calc_mode")
    calc_amount = fields.Selection(CALC_AMOUNT, 'Percent/Quantity',
                                   readonly=True,
                                   related="rappel_id.calc_amount")
    curr_qty = fields.Float("Curr. qty", readonly=True)
    section_id = fields.Many2one("rappel.section", "Section")
    section_goal = fields.Float("Section goal", readonly=True,
                                related="section_id.rappel_until")


    @api.model
    def send_rappel_info_mail(self):
        mail_pool = self.env['mail.mail']
        mail_ids = self.env['mail.mail']
        partner_pool = self.env['res.partner'].search([('rappel_ids','!=', '')])
        for partner in partner_pool:
            partner_list=[]
            partner_list.append(partner.id)
            pool_partners = self.search([('partner_id','=',partner.id)])
            send=False
            if pool_partners:

                values={}
                for rappel in pool_partners:

                    date_end = datetime.strptime(str(rappel.date_end), '%Y-%m-%d')
                    date_start = datetime.strptime(str(rappel.date_start), '%Y-%m-%d')
                    today = datetime.strptime(str(fields.Date.today()), '%Y-%m-%d')

                    for rappel_timing in rappel.rappel_id.advice_timing_ids:

                        if rappel_timing.advice_timing == 'fixed':
                            timing = (date_end - today).days
                            if timing == rappel_timing.timing:
                                send = True

                        if rappel_timing.advice_timing == 'variable':

                            timing = (date_end - date_start).days*rappel_timing.timing/100
                            timing2= (today - date_start).days

                            if timing == timing2:
                                send = True

                        if send == True and rappel.curr_qty:
                            if values.get(partner.id):
                                values[partner.id].append ({
                                    'concepto' : rappel.rappel_id.name,
                                    'date_start' : date_start.strftime('%d/%m/%Y'),
                                    'date_end':date_end.strftime('%d/%m/%Y'),
                                    'advice_timing' : rappel_timing.advice_timing,
                                    'timing' : rappel_timing.timing,
                                    'curr_qty' : rappel.curr_qty,
                                    'section_goal': rappel.section_goal,
                                    'section_id': rappel.section_id,
                                    'amount': rappel.amount
                                })
                            else:
                                values[partner.id]= [{
                                    'concepto' : rappel.rappel_id.name,
                                    'date_start' : date_start.strftime('%d/%m/%Y'),
                                    'date_end':date_end.strftime('%d/%m/%Y'),
                                    'advice_timing' : rappel_timing.advice_timing,
                                    'timing' : rappel_timing.timing,
                                    'curr_qty' : rappel.curr_qty,
                                    'section_goal': rappel.section_goal,
                                    'section_id': rappel.section_id,
                                    'amount': rappel.amount
                                }]
                        send = False

                if values.get(partner.id):
                    template = self.env.ref('rappel.rappel_mail_advice')
                    ctx = dict(self._context)
                    ctx.update({
                        'partner_email': partner.email,
                        'partner_id': partner.id,
                        'partner_lang': partner.lang,
                        'partner_name': partner.name,
                        'mail_from': self.env.user.company_id.email,
                        'values' : values[partner.id]
                    })

                    mail_id = template.with_context(ctx).send_mail(rappel.partner_id.id)
                    mail_ids += mail_pool.browse(mail_id)
                    send_ = False
                    if mail_ids:
                        mail_ids.send()
