# -*- coding: utf-8 -*-
# Copyright 2019 Comunitea Servicios Tecnológicos S.L.

import logging
from openerp import api, models, fields, _
from datetime import datetime
_logger = logging.getLogger(__name__)

MIN_MINUTE = 3

EMPLOYEE_FIELDS = ['id', 'name', 'state', 'last_sign']
USER_FIELDS = ['id', 'login', 'name']
CONF_FIELDS = ['image', 'logo_color', 'min_minute']


class HrEmployee(models.Model):
    _inherit = "hr.employee"


    @api.model
    def attendance_action_change_apk(self, vals):
        print vals
        employee = self.env['hr.employee'].browse(vals.get('employee_id', False))
        last_signin = self.env['hr.attendance'].search([
                        ('employee_id', '=', employee.id)], limit=1, order='name DESC')
        if last_signin:
            last_signin_datetime = datetime.strptime(last_signin.name, '%Y-%m-%d %H:%M:%S')

            now_datetime = datetime.now()
            diffmins = (now_datetime - last_signin_datetime).seconds/60
            if diffmins <= MIN_MINUTE and False:
                return {'error': True, 'error_msg': (_('Not enough time between logs: {} minutes').format(diffmins))}

        ctx = self._context.copy()
        if 'gps_info' in vals:
            ctx.update(gps_info=vals['gps_info'])

        res = employee.with_context(ctx).attendance_action_change()
        if res:
            return {'error': False, 'error_msg': ''}

    @api.model
    def get_employee_info(self, vals):

        user_id = self.env['res.users'].browse(vals.get('user_id'))
        if not user_id:
            return {'error': True, 'error_msg': 'No conincide el usuario/contraseña'}

        domain = [('user_id', '=',user_id.id)]
        employee_id = self.env['hr.employee'].search(domain, limit=1)

        domain = [('company_id', '=', user_id.company_id.id)]
        apk = self.env['clock.company.apk'].search(domain, limit=1)

        if not employee_id:
            return {'error': True, 'error_msg': 'Este usuario no tiene asignado un empleado'}
        if not apk:
            return {'error': True, 'error_msg': 'Esta compañia no tiene configurada la aplicación móvil'}

        res = {}
        for f in USER_FIELDS:
            res[f] = user_id[f]

        employee = {}
        for f in EMPLOYEE_FIELDS:
            employee[f] = employee_id[f]

        conf = {}
        for f in CONF_FIELDS:
            conf[f]= apk[f]

        res['employee'] = employee
        res['apk'] = conf
        return {'error': False, 'data': res}


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    def get_logs_domain(self, vals):
         from_date = vals.get('from_date', False)
         to_date = vals.get('to_date', False)
         employee_id = vals.get('employee_id', False)

         domain = [('employee_id', '=', employee_id)]
         if from_date:
             domain += [('name', '>=', from_date)]
         if to_date:
             domain += [('name', '<=', to_date)]
         return domain

    @api.model
    def get_vals(self, vals_type='out', check_val={}, min_accuracity=0):

        def day(date):
            try:
                day = datetime.strftime(datetime.strptime(date.split(' ')[0], '%Y-%m-%d'), '%d/%m/%Y')
            except:
                day = False
            return day

        def hour(date):
            try:
                hour = date.split(' ')[1]
            except:
                hour=False
            return hour


        if vals_type == 'sign_out':
            check_val = {'id': self.id,
                         'action': self.action == 'action' and self.action_desc.action_type or self.action or 'sign_in',
                         'day': day(self.name),
                         'log_out_hour': hour(self.name),
                         'log_out': self.name,
                         'worked_hours': self.worked_hours,
                         'gps_out': (self.accuracity <= min_accuracity),
                         'same_day': True}

        if vals_type== 'sign_in':
            check_val = {'id': self.id,
                         'action': self.action == 'action' and self.action_desc.action_type or self.action or 'sign_in',
                         'day': day(self.name),
                         'log_in_hour': hour(self.name),
                         'log_in': self.name,
                         'worked_hours': self.worked_hours,
                         'gps_in': (self.accuracity <= min_accuracity),
                         'same_day': True}
        if vals_type=='update':
            check_val.update(same_day=day(self.name) < check_val['day'],
                             gps_in=(self.accuracity <= min_accuracity),
                             log_in_hour=hour(self.name),
                             log_in=self.name)
        return check_val


    @api.model
    def get_logs(self, vals):

        limit = vals.get('limit', 0)
        domain = self.get_logs_domain(vals)
        checks = self.env['hr.attendance'].search(domain, limit=limit, order = 'name desc')
        employee = self.env['hr.employee'].browse(vals.get('employee_id', False))
        checks_vals =[]
        check_val={}
        apk = employee.company_id.get_clock_apk()
        for check in checks:
            check_action = (check.action == 'action' and check.action_desc.action_type or check.action)

            if check_action == 'sign_out':
                check_val = check.get_vals(vals_type='sign_out', min_accuracity=apk.min_accuracity)

            elif check_action == 'sign_in' and not check_val:
                checks_vals.append(check.get_vals(vals_type='sign_in', min_accuracity=apk.min_accuracity))
                check_val = {}

            elif check_action == 'sign_in' and check_val:
                checks_vals.append(check.get_vals(vals_type='update', check_val=check_val, min_accuracity=apk.min_accuracity))
                check_val = {}

            if check_val and check_val['action'] == 'sign_out' and False:
                domain = [('employee_id', '=', employee.id), ('name', '<', check.name)]
                check = check.env['hr.attendance'].search(domain, limit=1, order = 'name desc')
                checks_vals.append(check.get_vals(vals_type='update', check_val=check_val, min_accuracity=apk.min_accuracity))
                check_val = {}
        return checks_vals


    @api.multi
    def _get_url_gps(self):
        for att in self:
            url="https://www.google.com/maps/place/Comunitea/@43.0097445,-7.5688814,21z/data=!4m5!3m4!1s0xd31ce7d707316cf:0x9164e52878aa4c6c!8m2!3d43.009771!4d-7.568765"
            if att.latitude and att.longitude:
                url = "https://maps.google.com/?ll={},{}&z=16".format(att.latitude, att.longitude)
            att.url_gps = url

    latitude = fields.Float('Latitude')
    longitude = fields.Float('Longitude')
    accuracity = fields.Float('Error')
    ip = fields.Char('IP')
    url_gps = fields.Char('Position', compute="_get_url_gps")


    @api.model
    def create(self, vals):
        print self._context

        gps_info = self._context.get('gps_info', False)
        if gps_info:
            vals.update(gps_info)

        print vals
        return super(HrAttendance, self).create(vals)
