from odoo.upgrade import util

# Renombrar el módulo "old_module" a "new_module"
@openupgrade.migrate()
def migrate(env, version):
    module = env['ir.module.module'].search([('name', '=', 'delivery_carrier_label_ncx')], limit=1)
    if module and module.state not in ['installed', 'to install']:
        util.rename_module(env.cr, 'delivery_carrier_label_ncx', 'delivery_nacex')
