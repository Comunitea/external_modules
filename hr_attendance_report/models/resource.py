# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import api, fields, models
from datetime import datetime, timedelta
from openerp.osv import fields as fields2
import pytz


class resource_calendar_attendance(models.Model):

    _inherit = 'resource.calendar.attendance'

    date_to = fields.Date('End Date')


class resource_calendar(models.Model):
    _inherit = "resource.calendar"

    @api.multi
    def get_attendances_for_weekdays(self, day_dt):
        """ Given a day datetime, return matching attendances """
        self.ensure_one()
        weekday = day_dt.weekday()
        attendances = self.env['resource.calendar.attendance']

        for attendance in self.attendance_ids.filtered(
            lambda att:
                int(att.dayofweek) == weekday and
                not (att.date_from and fields.Date.from_string(att.date_from) > day_dt.date()) and
                not (att.date_to and fields.Date.from_string(att.date_to) < day_dt.date())):
            attendances |= attendance
        return attendances

    def get_working_intervals_of_day(self, cr, uid, id, start_dt=None, end_dt=None,
                                     leaves=None, compute_leaves=False, resource_id=None,
                                     default_interval=None, context=None):
        """ Get the working intervals of the day based on calendar. This method
        handle leaves that come directly from the leaves parameter or can be computed.

        :param int id: resource.calendar id; take the first one if is a list
        :param datetime start_dt: datetime object that is the beginning hours
                                  for the working intervals computation; any
                                  working interval beginning before start_dt
                                  will be truncated. If not set, set to end_dt
                                  or today() if no end_dt at 00.00.00.
        :param datetime end_dt: datetime object that is the ending hour
                                for the working intervals computation; any
                                working interval ending after end_dt
                                will be truncated. If not set, set to start_dt()
                                at 23.59.59.
        :param list leaves: a list of tuples(start_datetime, end_datetime) that
                            represent leaves.
        :param boolean compute_leaves: if set and if leaves is None, compute the
                                       leaves based on calendar and resource.
                                       If leaves is None and compute_leaves false
                                       no leaves are taken into account.
        :param int resource_id: the id of the resource to take into account when
                                computing the leaves. If not set, only general
                                leaves are computed. If set, generic and
                                specific leaves are computed.
        :param tuple default_interval: if no id, try to return a default working
                                       day using default_interval[0] as beginning
                                       hour, and default_interval[1] as ending hour.
                                       Example: default_interval = (8, 16).
                                       Otherwise, a void list of working intervals
                                       is returned when id is None.

        :return list intervals: a list of tuples (start_datetime, end_datetime)
                                of work intervals """
        if isinstance(id, (list, tuple)):
            id = id[0]

        # Computes start_dt, end_dt (with default values if not set) + off-interval work limits

        work_limits = []
        if start_dt is None and end_dt is not None:
            start_dt = end_dt.replace(hour=0, minute=0, second=0)
        elif start_dt is None:
            start_dt = datetime.now().replace(hour=0, minute=0, second=0)
        else:
            work_limits.append((start_dt.replace(hour=0, minute=0, second=0), start_dt))
        if end_dt is None:
            end_dt = start_dt.replace(hour=23, minute=59, second=59)
        else:
            work_limits.append((end_dt, end_dt.replace(hour=23, minute=59, second=59)))
        assert start_dt.date() == end_dt.date(), 'get_working_intervals_of_day is restricted to one day'

        intervals = []
        work_dt = start_dt.replace(hour=0, minute=0, second=0)

        # no calendar: try to use the default_interval, then return directly
        if id is None:
            working_interval = []
            if default_interval:
                working_interval = (start_dt.replace(hour=default_interval[0], minute=0, second=0), start_dt.replace(hour=default_interval[1], minute=0, second=0))
            intervals = self.interval_remove_leaves(working_interval, work_limits)
            return intervals
        working_intervals = []
        tz_info = fields2.datetime.context_timestamp(cr, uid, work_dt, context=context).tzinfo
        for calendar_working_day in self.get_attendances_for_weekdays(cr, uid, id, start_dt, context):
            x = work_dt.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(seconds=(calendar_working_day.hour_from * 3600))
            y = work_dt.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(seconds=(calendar_working_day.hour_to * 3600))
            x = x.replace(tzinfo=tz_info).astimezone(pytz.UTC).replace(tzinfo=None)
            y = y.replace(tzinfo=tz_info).astimezone(pytz.UTC).replace(tzinfo=None)
            working_interval = (x, y)
            working_intervals += self.interval_remove_leaves(working_interval, work_limits)

        # find leave intervals
        if leaves is None and compute_leaves:
            leaves = self.get_leave_intervals(cr, uid, id, resource_id=resource_id, context=None)

        # filter according to leaves
        for interval in working_intervals:
            work_intervals = self.interval_remove_leaves(interval, leaves)
            intervals += work_intervals
        return intervals
