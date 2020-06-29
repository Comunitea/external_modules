# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class PartnerImportMapper(Component):
    _inherit = "prestashop.res.partner.mapper"

    @mapping
    def state_id(self, record):
        if record.get("id_country") and record.get("postcode"):
            binder = self.binder_for("prestashop.res.country")
            country = binder.to_internal(record["id_country"], unwrap=True)
            city_zip = self.env["res.city.zip"].search(
                [
                    ("name", "=", record.get("postcode")),
                    ("city_id.country_id", "=", country.id),
                ], limit=1
            )
            if not city_zip:
                # Portugal
                city_zip = self.env["res.city.zip"].search(
                    [
                        ("name", "=", record.get("postcode").replace(' ', '-')),
                        ("city_id.country_id", "=", country.id),
                    ], limit=1
                )
                if not city_zip:
                    # Portugal 2
                    city_zip = self.env["res.city.zip"].search(
                        [
                            ("name", "=", record.get("postcode")[:4] + '-' + record.get("postcode")[4:]),
                            ("city_id.country_id", "=", country.id),
                        ], limit=1
                    )
            if city_zip:
                return {"state_id": city_zip.city_id.state_id.id}
