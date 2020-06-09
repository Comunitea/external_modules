# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import Component


class ProductTemplateImporter(Component):
    _inherit = 'prestashop.product.template.importer'

    def import_supplierinfo(self, binding):
        return
