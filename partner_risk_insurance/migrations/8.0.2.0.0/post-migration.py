# -*- coding: utf-8 -*-
# © 2016 Comunitea Servicios Tecnológicos (<http://www.comunitea.com>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

__name__ = ('copy from risk_insurance_status_old to ir_property values')


def migrate_risk_status_to_property(cr):
    cr.execute("select id from res_company")
    for row in cr.fetchall():
        cr.execute("""
            INSERT INTO ir_property
            (value_text, name, type,  company_id,  fields_id, res_id)
            (SELECT risk_insurance_status_old,
                    'risk_insurance_status',
                    'selection',
                    %s,
                    (SELECT id FROM ir_model_fields
                     WHERE name = 'risk_insurance_status'
                           AND model = 'res.partner'),
                    'res.partner,' || CAST(id AS TEXT)
            FROM res_partner)""" % row[0])
    cr.execute("alter table res_partner drop column risk_insurance_status_old")


def migrate(cr, version):
    if not version:
        return
    migrate_risk_status_to_property(cr)
