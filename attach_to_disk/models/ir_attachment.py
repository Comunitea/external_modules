# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api
import base64


class IrAttachment(models.Model):

    _inherit = 'ir.attachment'

    @api.model
    def att_to_disk(self, automatic=False, use_new_cursor=False):
        self._cr.execute('''
            delete from ir_attachment where db_datas is null and datas is null;
        ''')
        att_objs = self.sudo().search([('store_fname', '=', False),
                                       ('db_datas', '!=', False)])
        self._cr.execute("select id from ir_attachment where store_fname is "
			 "null and db_datas is not null")
        data = self._cr.fetchall()
        l = len(data)
        c = 1
        for att_id in data:
            att = self.browse(att_id)
            print "***********************"
            print "A disco el id: %s" % str(att.id)
            print "%s / %s" % (str(c), str(l))
            print "***********************"
            c += 1
            # We encode beacause in odoo 10 allways decode when download the
            # file. Old attachments from old versions are decoded in base 64
            # and it fails when downloading because odoo decode ir again.
            try:
                datas = base64.b64encode(att.db_datas)
                att.write({'datas': datas, 'db_datas': False})
            except:
                continue
