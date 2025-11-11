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
            if image_data and self.backend_record.resize_images:
                try:
                    # Validar que los datos de imagen son válidos antes de procesarlos
                    if isinstance(image_data, str):
                        # Si es una cadena, podría estar en base64, intentar decodificar
                        try:
                            base64.b64decode(image_data, validate=True)
                            # Si es base64 válido, usar directamente
                            image_data = base64.b64decode(image_data)
                        except Exception:
                            # Si no es base64, asumir que es binario
                            pass

                    # Redimensionar con image_process
                    image_data = tools.image_process(image_data, size=(256, 256))
                except Exception as e:
                    # Si falla el procesamiento, usar la imagen original
                    # o retornar None para saltar esta imagen
                    _logger.warning("Error processing image: %s", e)
                    if isinstance(record["content"], str):
                        try:
                            image_data = base64.b64decode(record["content"])
                        except Exception:
                            image_data = record["content"].encode() if isinstance(record["content"], str) else record["content"]
                    else:
                        image_data = record["content"]

            return {"file_db_store": image_data}

    @mapping
    def storage(self, record):
        return {"storage": self.backend_record.import_image_type}
