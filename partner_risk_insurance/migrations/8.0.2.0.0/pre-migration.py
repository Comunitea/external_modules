# -*- coding: utf-8 -*-
# © 2016 Comunitea Servicios Tecnológicos (<http://www.comunitea.com>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

__name__ = ('Copy field risk_insurance_status to risk_insurance_status_old')


def copy_risk_insurance_status_values(cr):
    cr.execute("""
       alter table res_partner
       add risk_insurance_status_old character varying
    """)
    cr.execute("""
       update res_partner
       set risk_insurance_status_old = risk_insurance_status
    """)


def migrate(cr, version):
    if not version:
        return
    # import ipdb; ipdb.set_trace()
    copy_risk_insurance_status_values(cr)
