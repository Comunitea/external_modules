# © 2021 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models


class PaymentReturn(models.Model):
    _inherit = 'payment.return'

    @api.multi
    def _prepare_move_line(self, move, total_amount):
        self.ensure_one()
        move_lines = []
        for return_line in self.line_ids:
            move_lines.append({
                'name': move.ref,
                'debit': 0.0,
                'credit': return_line.amount,
                'account_id': self.journal_id.default_credit_account_id.id,
                'move_id': move.id,
                'journal_id': move.journal_id.id,
                'partner_id': return_line.partner_id.id
            })
        return move_lines
