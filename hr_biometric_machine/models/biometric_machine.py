# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from mock import patch
from openerp.addons.hr_biometric_machine.pyzk.attendance import ZkOpenerp
from openerp.addons.hr_biometric_machine.pyzk.attendance import OpenerpAttendance
from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _

import datetime
import itertools
import pytz
import sys


class BiometricData(models.Model):
    _name = 'biometric.machine'

    @property
    def min_time(self):
        # Get min time
        if self.interval_min == 'sec':
            min_time = datetime.timedelta(seconds=self.time_interval_min)
        elif self.interval_min == 'min':
            min_time = datetime.timedelta(minutes=self.time_interval_min)
        elif self.interval_min == 'hour':
            min_time = datetime.timedelta(hours=self.time_interval_min)
        else:
            min_time = datetime.timedelta(days=self.time_interval_min)
        return min_time

    @property
    def max_time(self):
        # Get min time
        if self.interval_max == 'sec':
            max_time = datetime.timedelta(seconds=self.time_interval_max)
        elif self.interval_max == 'min':
            max_time = datetime.timedelta(minutes=self.time_interval_max)
        elif self.interval_max == 'hour':
            max_time = datetime.timedelta(hours=self.time_interval_max)
        else:
            max_time = datetime.timedelta(days=self.time_interval_max)
        return max_time

    @api.model
    def _tz_get(self):
        # Copied from base model
        return [
            (tz, tz) for tz in
            sorted(
                pytz.all_timezones,
                key=lambda tz: tz if not
                tz.startswith('Etc/') else '_')]

    name = fields.Char('Name')
    ip_address = fields.Char('Ip address')
    port = fields.Integer('Port')
    sequence = fields.Integer('Sequence')
    timezone = fields.Selection(
        _tz_get, 'Timezone', size=64,
        help='Divice timezone',
    )
    time_interval_min = fields.Integer(
        'Min time',
        help='Min allowed time  between two registers')
    interval_min = fields.Selection(
        [('sec', 'Sec(s)'), ('min', 'Min(s)'),
         ('hour', 'Hour(s)'), ('days', 'Day(s)'), ],
        'Min allowed time', help='Min allowed time between two registers',)
    time_interval_max = fields.Integer(
        'Max time',
        help='Max allowed time  between two registers',)
    interval_max = fields.Selection(
        [('sec', 'Sec(s)'), ('min', 'Min(s)'),
         ('hour', 'Hour(s)'), ('days', 'Day(s)'), ],
        'Max allowed time', help='Max allowed time between two registers',)

    @api.model
    def get_users(self):
        """
        Function use to get all the registered users
        at the biometric device
        """
        with ConnectToDevice(self.ip_address, self.port) as conn:
            users = conn.get_users()
        return users

    @api.model
    def clean_attendance(self):
        """
        Function use to clean all attendances
        at the biometric device
        """
        with ConnectToDevice(self.ip_address, self.port) as conn:
            conn.clear_attendance()

    @api.model
    def create_user(self):
        """
        function uses to assure that all users are alredy
        created in openerp
        """
        biometric_user_obj = self.env['biometric.user']
        users = self.get_users()
        openerp_users = biometric_user_obj.search([
            ('biometric_device', '=', self.id), ], )
        openerp_users_id = [user.biometric_id for user in openerp_users]
        for user in users:
            if int(user.user_id) not in openerp_users_id:
                biometric_user_obj.create({
                     'biometric_id': int(user.user_id),
                     'name': user.name,
                     'biometric_device': self.id, }
                )

    @patch('zk.base.Attendance', OpenerpAttendance)
    def getattendance(self):
        """
        Function uses to get attendances
        """
        self.create_user()
        with ConnectToDevice(self.ip_address, self.port) as conn:
            attendaces = conn.get_attendance()
        # Attendances are group by user
        for user_attendances in attendaces:
            # Compare each user attendance to review 
            # if fulfill minimun time condition
            for a, b in itertools.combinations(user_attendances, 2):
                if a.action_perform != b.action_perform:
                    continue
                if abs(a.timestamp - b.timestamp) < self.min_time:
                    user_attendances.remove(a)
        return attendaces


class ConnectToDevice(object):
    """
    Class uses to assure connetion to a device and closing of the same
    It is using to disable the device when it is been reading or busy
    """

    def __init__(self, ip_address, port):
        try:
            zk = ZkOpenerp(ip_address, port)
            conn = zk.connect()
        except:
            raise UserError(
                _('Unexpected error: {error}'.format(error=sys.exc_info()),)
            )
        conn.disable_device()
        self.conn = conn

    def __enter__(self):
        """
        return biometric connection
        """
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        enable device and close connection
        """
        self.conn.enable_device  # noqa: W0104
        self.conn.disconnect()
