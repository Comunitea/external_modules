# © 2021 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class L10nEsAeatMod347PartnerRecord(models.Model):
    _inherit = 'l10n.es.aeat.mod347.partner_record'

    report_year = fields.Integer(related='report_id.year', store=True)

    def _compute_access_url(self):
        super()._compute_access_url()
        for record in self:
            record.access_url = '/my/347_detail/%s' % (record.id)
