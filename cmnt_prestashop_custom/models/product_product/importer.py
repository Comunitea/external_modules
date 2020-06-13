# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import Component


class ProductCombinationImporter(Component):
    _inherit = 'prestashop.product.combination.importer'

    def import_supplierinfo(self, binding):
        return
