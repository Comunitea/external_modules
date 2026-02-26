from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare
from odoo.osv import expression
import logging
_logger = logging.getLogger(__name__)
import re
import xmlrpc.client
DB='a-sec'
UID=6
PASS='ko_1Ki24'

models = xmlrpc.client.ServerProxy('https://erp.leistung.es/xmlrpc/2/object')

def get_xml_id(model, id):
    return models.execute_kw(DB, UID, PASS, model, 'get_xml_id', [id])

def execute_kw(model, function, domain, limit=0):
    return models.execute_kw(DB, UID, PASS, model, 'search', [domain], {'limit': limit})

def import_from_odoo (model, domain, fields, limit=0):
    ids = execute_kw(model, 'search', domain, limit)
    return models.execute_kw(DB, UID, PASS, model, 'read', [ids], {'fields': fields})

class ResUsers(models.Model):
    _inherit = 'res.users'


    def get_xmlstr_id(self, model, id):
        json =  self.env[model].get_xml_id(id)
        if json[id]:
            return json[id]
        return False

    def import_brand_ids(self, test=True):
        brand_ids = import_from_odoo('product.brand', [], ['name'])
        if test:
            return brand_ids
        else:
            for brand in brand_ids:
                self.env['product.brand'].create(brand)

    def import_categ_ids(self, test=True):
        categ_ids = import_from_odoo('product.category', [('name', '!=', 'All')], ['name', 'parent_id'])
        if test:
            return categ_ids
        else:
            ## Primero las creo
            for categ in categ_ids:
                vals = {
                    'name': categ['name'],
                }

                categ_id = self.env['product.category'].create(vals)
            self._cr.commit()
            ## Ahora las relaciono
            for categ in categ_ids:
                if categ['parent_id']:
                    name = categ['parent_id'][1].split(' / ')[-1]

                    parent_id = self.env['product.category'].search([('name', '=', name)], limit=1)
                    if parent_id:
                        categ_id = self.env['product.category'].search([('name', '=', categ['name'])], limit=1)
                        categ_id.parent_id = parent_id.id
            
