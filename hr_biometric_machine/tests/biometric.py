# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from datetime import datetime, timedelta
from itertools import groupby
from openerp.addons.hr_biometric_machine.pyzk.attendance import OpenerpAttendance as zk_openerp  
from zk.user import User
import pytz


class BiometricDevice(object):
    """
    Class use to mock the model biometric device
    """


class MockConnectToDevice(object):
    """
    Class uses to assure connetion to a device and closing of the same
    It is using to disable the device when it is been reading or busy
    """

    def __init__(self, ip, port=4370, timeout=60):
        self._ip = ip
        self._port = port
        self._timeout = timeout
        self.id = 1

    def __enter__(self):
        """
        return biometric connection
        """
        return self

    def connect(self):
        return self

    @staticmethod
    def __exit__(*args, **kargs):
        return

    @staticmethod
    def enable_device():
        return

    @staticmethod
    def disable_device():
        return

    @staticmethod
    def disconnect():
        return

    @staticmethod
    def clear_attendance():
        return

    def get_users(self):
        users = []
        users.append(User(uid=1, user_id=1, privilege='', name='Andres'))
        users.append(User(uid=2, user_id=2, privilege='', name='Ma. Josefina'))
        users.append(User(uid=3, user_id=3, privilege='', name='Lorena'))
        users.append(User(uid=4, user_id=4, privilege='', name='Jimena'))
        users.append(User(uid=5, user_id=5, privilege='', name='Natalia'))
        users.append(User(uid=6, user_id=6, privilege='', name='Alonda'))
        users.append(User(uid=7, user_id=7, privilege='', name='Paulina'))
        users.append(User(uid=8, user_id=8, privilege='', name='Sofia'))
        return users

    def get_attendance(self):
        """
        Create 10 attendance to test behaivor
        """
        def convert_from_local_to_utc(date):
            # Hardcode ? :O ... yes .. it is not necessary really to have it
            local = pytz.timezone('America/Mexico_City')
            date = date.replace(tzinfo=pytz.utc)
            date = date.astimezone(local)
            date.strftime('%Y-%m-%d: %H:%M:%S')
            return date.replace(tzinfo=None)

        attendances = []
        today = convert_from_local_to_utc(datetime.strptime(
            datetime.strftime(
                datetime.today(), '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S',))
        # Create three attendances with same user id
        # but timestamp difference for 5 minutes
        # both registers are entrance
        attendances.append(zk_openerp('1', today, 0))
        attendances.append(zk_openerp('1', today + timedelta(minutes=2), 0))
        attendances.append(zk_openerp('1', today + timedelta(minutes=5), 0))
        attendances.append(zk_openerp('1', today + timedelta(minutes=7), 0))
        # Create two attendances with same user id
        # but timestamp difference for 5 minutes
        # both registers are different action
        attendances.append(zk_openerp('2', today + timedelta(minutes=10), 0))
        attendances.append(zk_openerp('2', today + timedelta(minutes=15), 1))
        # Create two attendances with same user id
        # but timestamp difference for 2 minutes
        # same action
        attendances.append(zk_openerp('3', today + timedelta(minutes=20), 0))
        attendances.append(zk_openerp('4', today + timedelta(minutes=22), 0))
        # Create two attendances with same user id
        # but timestamp difference for 2 minutes
        # different action
        attendances.append(zk_openerp('3', today + timedelta(minutes=23), 0))
        attendances.append(zk_openerp('4', today + timedelta(minutes=25), 1))
        # Create four register with a perct perfection ;)
        # the idea is, the users used the device correctly all the time
        # they registered all correctly for two days
        attendances.append(zk_openerp('5', today, 0))
        attendances.append(zk_openerp('6', today, 0))
        attendances.append(zk_openerp('5', today + timedelta(hours=8), 1))
        attendances.append(zk_openerp('6', today + timedelta(hours=8), 1))
        attendances.append(zk_openerp('5', today + timedelta(days=1), 0))
        attendances.append(zk_openerp('6', today + timedelta(days=1), 0))
        attendances.append(zk_openerp(
            '5', today + timedelta(days=1, hours=8), 1),)
        attendances.append(zk_openerp(
            '6', today + timedelta(days=1, hours=8), 1),)
        # This user only registered inputs for 3 days
        for i in range(3):
            attendances.append(zk_openerp('7', today + timedelta(days=i), 0))
        # This user only registered outputs for 3 days
        for i in range(3):
            attendances.append(zk_openerp('8', today + timedelta(days=i), 1))
        # A pilon
        attendances.append(zk_openerp('1', today + timedelta(days=5), 0))
        # Attendace at the same time
        attendances.append(zk_openerp('9', today, 1))
        attendances.append(zk_openerp('9', today, 1))
        # Group by users
        attendaces_openerp = []
        uniquekeys = []
        attendances = sorted(attendances, key=lambda x: x.user_id)
        for k, g in groupby(attendances, lambda x: x.user_id):
            attendaces_openerp.append(list(g))
            uniquekeys.append(k)
        return attendaces_openerp
