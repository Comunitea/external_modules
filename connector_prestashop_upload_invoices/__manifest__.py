# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "connector prestashop upload invoices",
    "version": "12.0.1.0.0",
    "summary": "Upload invoice reports to prestashop (requires https://github.com/Comunitea/cmntuploadodooinvoice installed on prestashop)",
    "category": "Connector",
    "author": "Comunitea",
    "website": "www.comunitea.com",
    "license": "AGPL-3",
    "depends": ["connector_prestashop"],
    "external_dependencies": {"python": ["paramiko"]},
    "data": ["views/prestashop_backend.xml"],
}
