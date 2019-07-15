"""

Revision ID: hr_biometric_machine_1.2.2
Revises:
Create Date: 2017-02-14

"""
from openupgradelib import openupgrade as tools

revision = '1.2.0'
down_revision = '1.3.0'
branch_labels = None
depends_on = None

def migrate(cr, installed_version):
    new_column = tools.get_legacy_name('fixme')
    query_update = """
        update hr_attendance set state = 'fix' where  {new_column} = True
    """.format(new_column=new_column)
    cr.execute(query_update)
    query_update = """
        update hr_attendance set state = 'right'
        where {new_column} = False or  {new_column} is Null 
    """.format(new_column=new_column)
    cr.execute(query_update)
    # Drop new_column
    tools.drop_columns(cr, [['hr.attendance', new_column]])