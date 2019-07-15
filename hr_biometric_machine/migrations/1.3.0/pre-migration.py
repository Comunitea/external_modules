"""

Revision ID: hr_biometric_machine_1.2.2
Revises:
Create Date: 2017-02-14

"""
from openupgradelib import openupgrade as tools
from openerp import SUPERUSER_ID

revision = '1.2.0'
down_revision = '1.3.0'
branch_labels = None
depends_on = None

column_renames = {
    'hr_attendance': [
        ('fixme', None, 'boolean'),
    ],
}

def migrate(cr, installed_version):
    # Copy column to prevent lost data
    new_column = tools.get_legacy_name('fixme')
    if (
            tools.column_exists(cr, 'hr_attendance', 'fixme') and not
            tools.column_exists(cr, 'hr_attendance', new_column)):
        tools.copy_columns(cr, column_renames)
