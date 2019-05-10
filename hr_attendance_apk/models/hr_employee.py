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

        employee = self.env['hr.employee'].browse(vals.get('employee_id', False))
        last_signin = self.env['hr.attendance'].search([
                        ('employee_id', '=', employee.id)], limit=1, order='name DESC')

        last_signin_datetime = datetime.strptime(last_signin.name, '%Y-%m-%d %H:%M:%S')
        now_datetime = datetime.now()
        diffmins = (now_datetime - last_signin_datetime).seconds/60
        if diffmins <= MIN_MINUTE and False:
            return {'error': True, 'error_msg': (_('Not enogh time between logs: {} minutes').format(diffmins))}

        res = employee.attendance_action_change()
        if res:
            return {'error': False, 'error_msg': ''}

    @api.model
    def get_employee_info(self, vals):

        user_id = self.env['res.users'].browse(vals.get('user_id'))


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
        print "---------------------"
        print res
        print "---------------------"
        return res





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
    def get_logs(self, vals):
        def day(date):
            return datetime.strftime(datetime.strptime(date.split(' ')[0], '%Y-%m-%d'), '%d/%m/%Y')
        def hour(date):
            return date.split(' ')[1]
        print vals
        print self._context
        limit = vals.get('limit', 0)
        domain = self.get_logs_domain(vals)
        checks = self.env['hr.attendance'].search(domain, limit=limit, order = 'name desc')
        employee = self.env['hr.employee'].browse(vals.get('employee_id', False))
        state = employee.state
        checks_vals =[]
        check_val={}
        for check in checks:

         check_action = check.action == 'action' and self.action_desc.action_type or check.action or 'sign_in'

         if check.action == 'sign_out':
            check_val = {'id': check.id,
                         'day': day(check.name),
                         'action': check_action,
                         'log_out_hour': hour(check.name),
                         'log_out': check.name,
                         'worked_hours': check.worked_hours,
                         'same_day': True}

         elif check.action == 'sign_in' and not check_val:
             check_val = {'id': check.id,
                          'day': day(check.name),
                          'action': check_action,
                          'same_day': True,
                          'log_in_hour': hour(check.name),
                          'log_in': check.name}
             checks_vals.append(check_val)
             check_val = {}

         elif check.action == 'sign_in' and check_val:
             check_val.update(same_day=day(check.name) < check_val['day'],
                              log_in_hour=hour(check.name),
                              log_in=check.name)
             checks_vals.append(check_val)
             check_val = {}

        if check_val and check_val['action'] == 'sign_out':
            domain = [('employee_id', '=', employee.id), ('name', '<', check.name)]
            check = self.env['hr.attendance'].search(domain, limit=1, order = 'name desc')
            check_val.update(same_day=day(check.name) < check_val['day'],
                             log_in_hour=hour(check.name),
                             log_in=check.name)
            checks_vals.append(check_val)
            check_val = {}
        print checks_vals
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