from odoo import api, models, tools

import logging
import threading

_logger = logging.getLogger(__name__)


class ProcucreSupplierCompute(models.TransientModel):
    _name = 'procure.supplier.compute'
    _description = 'Check Orderpoint For supplier'

    def _procure_calculation_orderpoint(self):
        with api.Environment.manage():
            # As this function is in a new thread, I need to open a new cursor, because the old one may be closed
            new_cr = self.pool.cursor()
            ctx = self._context.copy()
            active_ids = self.env.context.get('active_ids')
            ctx.update( supplier_ids=active_ids)
            self = self.with_context(ctx)
            self = self.with_env(self.env(cr=new_cr))

            for company in self.env.user.company_ids:
                self.env['procurement.group']._run_orderpoints_supplier(
                    use_new_cursor=True,
                    company_id=company.id)
            new_cr.close()
            return {}

    def procure_calculation(self):
        threaded_calculation = threading.Thread(target=self._procure_calculation_orderpoint, args=())
        threaded_calculation.start()
        return {'type': 'ir.actions.act_window_close'}
