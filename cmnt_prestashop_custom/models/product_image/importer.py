# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
import base64
from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping
from odoo import tools

_logger = logging.getLogger(__name__)


class ProductImageMapper(Component):
    _inherit = "prestashop.product.image.import.mapper"

    @mapping
    def image_url(self, record):
        if self.backend_record.import_image_type == "url":
            return {"url": record["full_public_url"]}
        elif self.backend_record.import_image_type == "db":
            image_data = record["content"]
            return {"file_db_store": image_data}

    @mapping
    def storage(self, record):
        return {"storage": self.backend_record.import_image_type}
