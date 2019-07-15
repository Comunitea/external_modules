
from itertools import groupby
from zk.attendance import Attendance
from zk import ZK

class ZkOpenerp(ZK):

    def get_attendance(self):
        attendances = super(ZkOpenerp, self).get_attendance()
        # Group by users
        attendaces_openerp = []
        uniquekeys = []
        attendances = sorted(attendances, key=lambda x: x.user_id)
        for k, g in groupby(attendances, lambda x: x.user_id):
            attendaces_openerp.append(list(g))
            uniquekeys.append(k)
        return attendaces_openerp


class OpenerpAttendance(Attendance):

    @property
    def action_perform(self):
        actions = {
            0: 'sign_in',
            1: 'sign_out',
        }
        # return actions.get(self.status)
        return actions.get(self.punch)
