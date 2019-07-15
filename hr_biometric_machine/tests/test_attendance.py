# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp.tests.common import TransactionCase
from openerp.addons.hr_biometric_machine.tests.biometric import MockConnectToDevice
from mock import patch


class TestGetAttendance(TransactionCase):
    """For attendace creation for biometric advice"""

    def setUp(self):
        super(TestGetAttendance, self).setUp()
        self.biometric_machine = self.registry['biometric.machine']

    @patch(
        'openerp.addons.hr_biometric_machine.models.biometric_machine.ConnectToDevice',
        MockConnectToDevice)
    def test_attendace_time(self):
        """Test the minimum allowed time between each user registration"""
        cr, uid = self.cr, self.uid
        # TODO what would happend if there wouldn't be a biometric machine?
        biometric_ids = self.biometric_machine.search(cr, uid, [])
        attens = []
        for biometric in self.biometric_machine.browse(cr, uid, biometric_ids):
            attendances = biometric.getattendance()
            for user_attendance in attendances:
                # Sorted elements using timestamp
                user_attendance.sort(key=lambda x: x.timestamp)
                for item, atten in enumerate(attens):
                    # If the user or the performed action are not equal then
                    # we don't want to test a minimum time
                    if (atten.user_id == attens[item-1].user_id and
                            atten.action_perform == attens[item-1].action_perform):
                        self.assertNotAlmostEqual(
                            atten.timestamp, attens[item-1].timestamp,
                            msg='Your function is alowing user registration with '
                            'a time less than the allowed one',
                            delta=biometric.min_time)
