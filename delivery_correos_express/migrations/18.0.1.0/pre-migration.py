from openupgradelib import openupgrade

# Renombrar el módulo "old_module" a "new_module"
@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_module(env.cr, 'delivery_carrier_label_cex', 'delivery_correos_express')
