# Copyright 2019 Comunitea Servicios Tecnológicos S.L.

from odoo import api, models, fields, _
from datetime import datetime
import pytz

MIN_MINUTE = 3

EMPLOYEE_FIELDS = ['id', 'name', 'company_id']
USER_FIELDS = ['id', 'login', 'name', 'company_id']
CONF_FIELDS = ['image', 'logo_color', 'min_minute', 'distance_filter',
               'stationary_radius', 'min_accuracity']


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.model
    def attendance_action_change_apk(self, vals):
        employee = self.env['hr.employee'].\
            browse(vals.get('employee_id', False))
        last_signin = self.env['hr.attendance'].\
            search([('employee_id', '=', employee.id)], limit=1,
                   order='id DESC')
        if last_signin:
            last_signin_datetime = datetime.strptime(last_signin.create_date,
                                                     '%Y-%m-%d %H:%M:%S')
            now_datetime = datetime.now()
            diffmins = (now_datetime - last_signin_datetime).seconds/60
            if diffmins <= MIN_MINUTE and False:
                return {'error': True,
                        'error_msg':
                        (_('Not enough time between logs: {} minutes').
                         format(diffmins))}
            
        ctx = self._context.copy()
        if 'gps_info' in vals:
            ctx.update(gps_info=vals['gps_info'])
            if not last_signin.check_out and ('latitude' in vals['gps_info'] and 'longitude' in vals['gps_info']):
                position_vals = {
                    'employee_id': vals['employee_id'],
                    'latitude': vals['gps_info']['latitude'],
                    'longitude': vals['gps_info']['longitude']
                }
                self.env['hr.attendance.position'].insert_position_apk(position_vals)
        res = employee.with_context(ctx).attendance_action_change()
        if res:
            return {'error': False, 'error_msg': ''}

    @api.model
    def get_employee_info(self, vals):

        user_id = vals.get('user_id', False)
        if user_id:
            user_id = self.env['res.users'].browse(user_id)

        employee_id = vals.get('employee_id', False)

        if not user_id and not employee_id:
            return {'error': True,
                    'error_msg': 'No coincide el usuario/contraseña'}
        if employee_id:
            employee_id = self.browse(employee_id)
        if user_id and not employee_id:
            domain = [('user_id', '=', user_id.id)]
            employee_id = self.env['hr.employee'].search(domain, limit=1)

            if not employee_id:
                return {'error': True,
                        'error_msg':
                        'Este usuario no tiene asignado un empleado'}

            domain = [('company_id', '=', user_id.company_id.id)]
            apk = self.env['clock.company.apk'].search(domain, limit=1)
            if not apk:
                return {'error': True,
                        'error_msg':
                        'Esta compañia no tiene configurada la aplicación '
                        'móvil'}
        if employee_id:
            employee = {}
            for f in EMPLOYEE_FIELDS:
                if f == 'company_id':
                    employee[f] = employee_id[f].id or False
                else:
                    employee[f] = employee_id[f]

            if vals.get('employee_info', False):
                # EQUIVALE A UN SEARCH READ
                active_attendance = self.env['hr.attendance'].search([('employee_id', '=', employee_id.id)], limit=1, order='id DESC')
                if not active_attendance.check_out:
                    employee['state'] = 'present'
                else:
                    employee['state'] = 'not-present'
                return employee
        if user_id:
            res = {}
            for f in USER_FIELDS:
                if f == 'company_id':
                    res[f] = user_id[f].id or False
                else:
                    res[f] = user_id[f]
        if apk:
            conf = {}
            for f in CONF_FIELDS:
                conf[f] = apk[f]
                conf[f] = apk[f]
            res['apk'] = conf
        res['employee'] = employee

        return {'error': False, 'data': res}


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    
    @api.model
    def get_google_maps_url(self):
        for att in self:
            origin = '{},{}'.format(att.latitude, att.longitude)
            destination = att.get_related_attendance()
            if destination:
                destination_obj = self.env['hr.attendance'].browse(destination)
                destination_point = '{},{}'.format(destination_obj.latitude,
                                                   destination_obj.longitude)
            else:
                if att.attendance_position_ids:
                    destination_point = '{},{}'.\
                        format(att.attendance_position_ids[-1].latitude,
                               att.attendance_position_ids[-1].longitude)
                else:
                    destination_point = origin
            waypoints = att.attendance_position_ids
            waypoints_str = ''
            if waypoints:
                for point in waypoints:
                    if point == waypoints[0]:
                        waypoints_str = '{},{}'.format(point.latitude,
                                                       point.longitude)
                    else:
                        waypoints_str = '{}%7C{},{}'.format(waypoints_str,
                                                            point.latitude,
                                                            point.longitude)

            att.google_maps_url = \
                ("https://www.google.com/maps/dir/?api=1&origin={}&destination"
                 "={}&travelmode=driving&waypoints={}").\
                format(origin, destination_point, waypoints_str)

    google_maps_url = fields.Char(compute="get_google_maps_url")

    @api.model
    def get_attendance_data(self, attendance_id):
        attendance = self.browse(attendance_id)
        if attendance.check_out:
            action = 'sign_out'
        else:
            action = 'sign_in'
        return {
            'action': action,
            'related_attendance_id': attendance.id,
        }

    def get_related_attendance(self):
        for attendance in self:
            return self.env['hr.attendance'].search([('employee_id', '=', attendance.employee_id.id)\
                , ('id', '>', attendance.id)], limit=1, order='id DESC').id or False


    @api.model
    def get_name_to_user_zone(self, date):
        ctx = self._context.copy()
        tz = pytz.timezone('UTC')

        if 'tz' in ctx:
            tz = pytz.timezone(ctx['tz'])
        name = datetime.strftime(pytz.utc.localize(datetime.strptime(date, \
            '%Y-%m-%d %H:%M:%S')).astimezone(tz),'%Y-%m-%d %H:%M:%S')
        return name

    def get_logs_domain(self, vals):
        from_date = vals.get('from_date', False)
        to_date = vals.get('to_date', False)
        employee_id = vals.get('employee_id', False)

        domain = [('employee_id', '=', employee_id)]
        if from_date:
            domain += [('check_in', '>=', from_date)]
        if to_date:
            domain += ['|', ('check_out', '<=', to_date),
                       ('check_out', '=', False)]
        return domain

    @api.model
    def get_vals(self, vals_type='sign_out', check_val={}, min_accuracity=0):

        def day(date):
            try:
                day = datetime.strftime(datetime.strptime(date.split(' ')[0],
                                        '%Y-%m-%d'), '%d/%m/%Y')
            except Exception:
                day = False
            return day

        def hour(date):
            try:
                hour = date.split(' ')[1]
            except Exception:
                hour = False
            return hour

        if vals_type == 'sign_out':
            name = self.get_name_to_user_zone(self.check_out)
            check_val = {'id': self.id,
                         'action': 'sign_out',
                         'day': day(name),
                         'log_out_hour': hour(name),
                         'log_out': name,
                         'worked_hours': self.worked_hours,
                         'gps_out': (self.accuracity <= min_accuracity),
                         'same_day': True,
                         'google_maps_url': self.google_maps_url}

        if vals_type == 'sign_in':
            name = self.get_name_to_user_zone(self.check_in)
            check_val = {'id': self.id,
                         'action': 'sign_in',
                         'day': day(name),
                         'log_in_hour': hour(name),
                         'log_in': name,
                         'worked_hours': self.worked_hours,
                         'gps_in': (self.accuracity <= min_accuracity),
                         'same_day': True,
                         'google_maps_url': self.google_maps_url}
        if vals_type == 'update':
            name = self.get_name_to_user_zone(self.check_in)
            check_val.update(same_day=day(name) < check_val['day'],
                             gps_in=(self.accuracity <= min_accuracity),
                             log_in_hour=hour(name),
                             log_in=name)
        return check_val

    @api.model
    def get_logs(self, vals):
        
        limit = vals.get('limit', 0)
        domain = self.get_logs_domain(vals)
        checks = self.env['hr.attendance'].search(domain, limit=limit,
                                                  order='id desc')
        employee = self.env['hr.employee'].browse(vals.get('employee_id',
                                                  False))
        ctx = self._context.copy()
        if employee.user_id.tz:
            ctx.update(tz=employee.user_id.tz)

        checks_vals = []
        check_val = {}
        apk = employee.company_id.get_clock_apk()
        for check in checks:

            if check.check_out:
                check_val = check.with_context(ctx).get_vals(vals_type='sign_out',
                                           min_accuracity=apk.min_accuracity)
                if check.check_in:
                    check_val = check.with_context(ctx).get_vals(vals_type='update', check_val=check_val,
                                            min_accuracity=apk.min_accuracity)

            elif not check.check_out:
                check_val = check.with_context(ctx).get_vals(vals_type='sign_in',
                                           min_accuracity=apk.min_accuracity)
            
            checks_vals.append(check_val)

        return checks_vals

    @api.multi
    def _get_url_gps(self):
        for att in self:
            url = ("https://www.google.com/maps/place/Comunitea/@43.0097445,"
                   "-7.5688814,21z/data=!4m5!3m4!1s0xd31ce7d707316cf:"
                   "0x9164e52878aa4c6c!8m2!3d43.009771!4d-7.568765")
            if att.latitude and att.longitude:
                url = "https://maps.google.com/?ll={},{}&z=16".\
                    format(att.latitude, att.longitude)
            att.url_gps = url

    latitude = fields.Float('Latitude')
    longitude = fields.Float('Longitude')
    accuracity = fields.Float('Error')
    ip = fields.Char('IP')
    url_gps = fields.Char('Position', compute="_get_url_gps")
    attendance_position_ids = fields.One2many(
        comodel_name="hr.attendance.position",
        inverse_name="attendance_id", string="Attendance positions")

    @api.model
    def create(self, vals):
        gps_info = self._context.get('gps_info', False)
        if gps_info:
            vals.update(gps_info)
        return super(HrAttendance, self).create(vals)


class HrAttendancePosition(models.Model):
    _name = "hr.attendance.position"

    attendance_id = fields.Many2one(comodel_name='hr.attendance',
                                    string="User Attendance")
    latitude = fields.Float('Latitude')
    longitude = fields.Float('Longitude')

    @api.model
    def insert_position_apk(self, vals):
        employee_id = vals.get('employee_id', False)
        latitude = vals.get('latitude', False)
        longitude = vals.get('longitude', False)
        domain = [('employee_id', '=', employee_id)]
        last_attendance = self.env['hr.attendance'].\
            search(domain, limit=1, order='id desc')
        if not last_attendance.check_out:
            values = {
                'attendance_id': last_attendance.id,
                'latitude': latitude,
                'longitude': longitude,
            }
            attendance_position = self.env['hr.attendance.position'].\
                create(values)

            return attendance_position
        return False
