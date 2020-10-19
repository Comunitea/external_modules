# -*- coding: utf-8 -*-


from odoo import api, models, fields
import pprint
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ProductPutaway(models.Model):
    _inherit = "product.putaway"

    @api.multi
    def generate_inventory(self, fixed_location_id=False):
        si_ids = self.env['stock.inventory']
        sil = self.env['stock.inventory.line']
        sfps = self.env['stock.fixed.putaway.strat']
        domain = [('name', '=', 'STOCK')]
        sfp_id = self.env['product.putaway'].search(domain)
        lines_domain = [('putaway_id', '=', sfp_id.id)]
        if fixed_location_id:
            lines_domain += [('fixed_location_id', '=', 'id')]
        sfps_ids = sfps.search(lines_domain)
        strat_name = sfp_id.name
        for line in sfps_ids:
            name = '{}:{}'.format(strat_name, line.fixed_location_id.name)
            domain = [('name', '=', name), ('location_id', '=', line.fixed_location_id.id), ('state', '=', 'draft'), ('filter', '=', 'products')]
            si_id = si_ids.search(domain)
            if not si_id:
                val = {'name': name, 'location_id': line.fixed_location_id.id, 'filter': 'products', 'exhausted': True}
                si_id = si_ids.create(val)
            si_ids |= si_id
            si_id.write({'product_ids': [(4, line.product_id.id)]})
        for si in si_ids:
            si.action_start()

class StockLocation(models.Model):
    _name = 'stock.location'
    _inherit = ['info.apk', 'stock.location']

    @api.multi
    def compute_apk_name(self):
        for obj in self:
            obj.apk_name = obj.name

    def get_location_from_apk_values(self, barcode, move_id= False):
        if barcode:
            location = self.search([('barcode', '=', barcode)], limit=1)
        if not location and move_id:
            location = move_id.active_location_id
        return location

    @api.multi
    def compute_apk_name(self):
        for obj in self:
            obj.apk_name = obj.name

    def return_fields(self, mode='tree'):
        return ['id', 'name', 'usage', 'barcode', 'display_name', 'removal_priority', 'usage']

    @api.model
    def delete_inventory_obj(self, values):
        location_id = values.get('location_id', False)
        if location_id == 13 and False:
            raise ValidationError ('Has intentado vaciar el almacén completo. Debes hacerlo por ubicaciones')


        line_ids = values.get('line_id', False)
        if line_ids:
            if isinstance(line_ids, list):
                domain = [('id', 'in', line_ids)]
            else:
                domain = [('id', '=', line_ids)]
        else:
            inventory_id = values.get('inventory_id', False)
            if not line_ids and inventory_id:
                domain = [('inventory_id', '=', inventory_id),
                          ('inventory_id.state', '=', 'confirm'),
                          ('location_id', '=', values.get('location_id', False)),
                          ('product_id', '=', values.get('product_id', False))
                          ]
        line_ids = self.env['stock.inventory.line'].search(domain)
        product_qty = values.get('product_qty', 0)
        if line_ids:
            line_ids.write({'product_qty': product_qty})
            #self.env['stock.inventory.line'].browse(line_id).unlink()
        return self.get_apk_inventory(values)


    @api.model
    def change_inventory_line_qty(self, values):

        def create_new_inv_line(inventory_id, product_id, location_id):
            pre_filter = inventory_id.filter
            pre_product = inventory_id.product_id
            exhausted = inventory_id.exhausted
            inventory_id.filter = 'product'
            inventory_id.product_id = product_id
            inventory_id.exhausted = True
            line_vals = inventory_id._get_inventory_lines_values()
            ctx = self._context.copy()
            ctx.update(default_inventory_id = inventory_id.id, default_company_id = inventory_id.company_id.id)
            self.env['stock.inventory.line'].with_context(ctx).create(line_vals)
            inventory_id.product_id = pre_product
            inventory_id.filter = pre_filter
            inventory_id.exhausted = exhausted

        def write_qty():
            if product_id.tracking != 'serial':
                if product_qty:
                    line_id.product_qty = product_qty
                else:
                    line_id.product_qty += inc or 1.0
            else:
                line_id.product_qty = inc or 1.0

        line_id = values.get('line', False)
        line_id = self.env['stock.inventory.line'].browse(line_id)
        inc = values.get('inc', False)
        if line_id and inc and line_id.product_id.tracking == 'none':
            _logger.info ("Ajuste de stock en {} para el artículo {}: {}".format(line_id.location_id.name,
                                                                                 line_id.product_id.default_code,
                                                                                 line_id.product_qty))
            line_id.product_qty += inc
            values.update(active_location=line_id.location_id.id, active_product = line_id.product_id.id)
            return self.get_apk_inventory(values)

        product_id = values.get('product_id', False)
        lot_name = values.get('serial', False)
        if lot_name and product_id:
            lot_names = lot_name.split(',')
            if len(lot_names) > 1:
                for lot in lot_names:
                    values.update(wh_code=False, serial=lot, lot_name=lot)
                    res = self.change_inventory_line_qty(values)
                return res
        ## de momento lo pongo aquí como un parámetro
        create_lot = values.get('create_lot', True)
        wh_code = values.get('wh_code', False)
        product_qty = values.get('product_qty', False)


        #print("change_inventory_line_qty con values:\n#######################################")
        #pprint.PrettyPrinter(indent=2).pprint(values)
        inventory_id = self.env['stock.inventory'].browse(values.get('inventory_id', False))
        if not inventory_id:
                raise ValidationError('No ha definido un inventario para ajustar')
        print('Para el inventario la linea {}'.format(inventory_id.display_name))
        if line_id:
            ## Nunca para lotes o series
            print ('Encuentro la linea {}'.format(line_id.display_name))
            location_id = line_id.location_id
            product_id = line_id.product_id
            inventory_id = line_id.inventory_id
        else:
            location_id = values.get('location_id', False)
            location_id = self.env['stock.location'].browse(location_id)
            if not location_id:
                raise ValidationError('No ha definido ubicación para ajustar')
            print('Para la ubicación la linea {}'.format(location_id.display_name))
            if product_id:
                product_id = self.env['product.product'].browse(product_id)
                ## tengo que verificar que el wh_code no es ningún serie este producto
                lot_id = self.get_apk_lot(wh_code, product_id)
                strict_product = self.get_apk_product(wh_code)

                if not lot_id and strict_product or lot_id and lot_id.product_id == strict_product:
                    product_id = strict_product
                    values.update(product_id=product_id.id)

                if product_id.tracking == 'none':
                    ## puede haber un cambio de artículo
                    values['filter']['product_id'] = product_id.id
                    values.update(active_location=location_id.id,
                                      active_product=product_id.id)
                    domain = [('location_id', '=', location_id.id),
                              ('product_id', '=', product_id.id),
                              ('inventory_id', '=', inventory_id.id)]
                    line_id = self.env['stock.inventory.line'].search(domain)
                print('Para el artículo {}'.format(product_id.display_name))
            if not product_id:
                product_id = self.get_apk_product(wh_code)
                if product_id:
                    ## Como he utilizado el wh_code para buscar artículo, no puedo utlizarlo para crear un lote nuevc
                    print('Para el artículo {}'.format(product_id.display_name))
                    lot_name = False
                if product_id and product_id.tracking == 'none':
                    domain = [('location_id', '=', location_id.id),
                              ('product_id', '=', product_id.id),
                              ('inventory_id', '=', inventory_id.id)]
                    line_id = self.env['stock.inventory.line'].search(domain, limit=1)

                elif not product_id and lot_name:
                    ## miro si en las líneas del inventario hay un producto para este lote o serie
                    domain = [('location_id', '=', location_id.id),
                              ('prod_lot_id.name', '=', lot_name),
                              ('inventory_id', '=', inventory_id.id)]
                    line_id = self.env['stock.inventory.line'].search(domain)


                # if line_id:
                #     print('Vuelvo a entrar con la línea {}'.format(line_id.id))
                #     values['id'] = line_id.id
                #     return self.change_inventory_line_qty(values)

        if product_id.tracking != 'none':
            values.update(product_id=product_id.id, active_product=product_id.id)
        if line_id:
            product_id = line_id.product_id
            print('Ajuste de la línea con cantidad {}'.format(line_id.product_qty))
            write_qty()
            print('a  {}'.format(line_id.product_qty))
            values.update(active_location=line_id.location_id.id)
            return self.get_apk_inventory(values)

        if not product_id:
            raise ValidationError('No ha definido un artículo para ajustar')
        ## Si envío un producto sin trackin +1

        if product_id.tracking == 'none':
            domain = [('location_id', '=', location_id.id),
                      ('inventory_id', '=', inventory_id.id),
                      ('product_id', '=', product_id.id)]
            line_id = self.env['stock.inventory.line'].search(domain)
            if line_id:
                line_id.product_qty += 1
            else:
                create_new_inv_line(inventory_id, product_id, location_id)
            values.update(product_id=product_id.id,
                          active_product=product_id.id,
                          active_location=location_id.id)
            return self.get_apk_inventory(values)
        ## a partir de aquí solo articulos con tracking

        lot_id = self.env['stock.production.lot']
        if lot_name:
            lot_id = self.get_apk_lot(lot_name.upper(), product_id)
            if not lot_id and create_lot:
                ## lo creo, a saber debe venir la orden de crear en el values de la pda
                new_lot_vals = {'product_id': product_id.id, 'name': lot_name.upper()}
                lot_id = self.env['stock.production.lot'].create(new_lot_vals)
                print ("Creo un nuevo lote para {}: {}: {}".format(product_id.display_name, lot_id.id, lot_id.name))

        if not lot_id and product_id:
            domain = [('location_id', '=', location_id.id),
                      ('inventory_id', '=', inventory_id.id),
                      ('product_id', '=', product_id.id),
                      ('prod_lot_id', '=', False)]
            line_id = self.env['stock.inventory.line'].search(domain)

            if line_id:
                raise ValidationError ('Ya hay una línea sin lote para el artículo {}'.format(product_id.wh_code))
            else:
                create_new_inv_line(inventory_id, product_id, location_id)
                values.update(
                          active_location=location_id.id)
                return self.get_apk_inventory(values)

        if lot_id and product_id:
            domain = [('location_id', '=', location_id.id),
                      ('inventory_id', '=', inventory_id.id),
                      ('product_id', '=', product_id.id),

                      '|', ('prod_lot_id', '=', lot_id.id), ('prod_lot_id', '=', False)]

            line_id = self.env['stock.inventory.line'].search(domain, limit=1, order="prod_lot_id desc")
            if not line_id:
                line_vals = {'inventory_id': inventory_id.id,
                             'product_id': product_id.id,
                             'location_id': location_id.id,
                             'product_qty': 0
                             }
                line_id = self.env['stock.inventory.line'].create(line_vals)
            line_id.prod_lot_id = lot_id.id
            write_qty()
            values.update(
                active_product = product_id.id,
                active_location = location_id.id)
            return self.get_apk_inventory(values)
        print ("--------------------\n Se ha escapado algo ..... \n-------------")
        raise ValidationError('Se ha escapado algo :-( {}'.format(values))

        return self.get_apk_inventory(values)


    @api.model
    def delete_inventory_location(self, values):
        print ("Entrando en delete ...")

        location_id = values.get('location_id', False)
        product_id = values.get('product_id', False)
        inventory_id = values.get('inventory_id', False)
        option = values.get('option', 'unlink')
        domain = [('inventory_id', '=', inventory_id)]
        if product_id:
            domain += [('product_id', '=', product_id)]
        if location_id:
            domain += [('location_id', '=', location_id)]
        domain += [('inventory_id.state', '=', 'confirm')]
        lines = self.env['stock.inventory.line'].search(domain)
        if option == 'unlink':
            lines.unlink()
        elif option == 'reset':
            lines.write({'product_qty': 0})
        values = {'inventory_id': inventory_id}
        return self.get_apk_inventory(values)


    @api.model
    def get_apk_inventory(self, values):
        def filter_lines(lines):
            if product_id and location_id:
                return lines.filtered(lambda x: x.product_id.id == product_id and x.location_id.id == location_id)
            elif product_id:
                return lines.filtered(lambda x: x.product_id.id == product_id)
            elif location_id:
                return lines.filtered(lambda x: x.location_id.id == location_id)
            return lines
        max_serial_lines = values.get('max_serial_lines', 15)
        product_id = values.get('product_id', False)

        active_location = values.get('active_location', False)
        location_id = values.get('location_id', active_location)

        active_product = values.get('active_product', False)
        filter_line = values.get('filter', {})
        if active_product:
            filter_line.update(product_id= active_product)
        if active_location:
            filter_line.update(location_id= active_location)
        if location_id == -1:
            location_id = False
        inventory_id = values.get('inventory_id', False)
        res = {'inventory': True,
               'inventory_id': 0,
               'inventory_location_ids': [],
               'ActiveLocation': active_location,
               'ActiveProduct': active_product}

        if inventory_id:
            inventory_id = self.env['stock.inventory'].browse(inventory_id).filtered(lambda x: x.state =='confirm')
            #inventory_location = active_location
        else:
            domain = [('filter', 'in', ['none', 'partial', 'product', 'products']), ('state', '=', 'confirm'), ('location_id', '=', self.id)]
            inventory_id = self.env['stock.inventory'].search(domain, limit=1)
            #inventory_location = inventory_id.location_id
            if not inventory_id:
                ## Busco si hay lineas inventario de tipo none por las líneas,
                domain = [('inventory_id.filter', 'in', ['none', 'partial', 'product', 'products']), ('inventory_id.state', '=', 'confirm'), ('location_id', '=', self.id)]
                inventory_id = self.env['stock.inventory.line'].search(domain, limit=1).mapped('inventory_id')
                # Si pasa esto
                #inventory_location = self
        if not inventory_id:
            _logger.info("No encuentro inventario")
            res = {'inventory': False,
                   'inventory_id': 0,
                   'inventory_name': '',
                   'barcode_re': self.apk_warehouse_id.barcode_re,
                   'product_re': self.apk_warehouse_id.product_re}
            return res

        if filter_line:
            line_domain = [('inventory_id', '=', inventory_id.id), ('inventory_id.state', '=', 'confirm')]
            filter_location_id = filter_line.get('location_id', False)
            if filter_location_id:
                line_domain += [('location_id', '=', filter_location_id)]
                res['ActiveLocation'] = filter_location_id
            if filter_line.get('product_id', False):
                line_domain += [('product_id', '=', filter_line.get('product_id', False))]
            lines = self.env['stock.inventory.line'].search(line_domain)
        else:
            lines = inventory_id.line_ids
        #res = {'inventory': True, 'inventory_id': 0, 'inventory_location_ids': []}
        if inventory_id:
            empty_location = values.get('empty_location', False)
            if empty_location:
                product = inventory_id.product_id
                if product:
                    product_id = product.id
                if not product_id:
                    product_id = values.get('active_product', False)
                if not product_id:
                    raise ValidationError('Para que artículo?')
                empty_location_id = self.search([('barcode', '=', empty_location)])
                if empty_location_id:
                    ## Creo una linea nueva para este artículo
                    vals = {'inventory_id': inventory_id.id,
                            'product_id': product_id,
                            'location_id': empty_location_id.id}
                    if inventory_id.product_id:
                        vals.update(location_id=empty_location_id.id)
                    self.env['stock.inventory.line'].create(vals)


            LineIndex = -1
            ProductIndex = -1
            LocationIndex = -1
            res['inventory'] = True
            res['inventory_id'] = inventory_id.id
            res['inventory_name'] = inventory_id.name
            res['barcode_re'] = self.apk_warehouse_id.barcode_re
            res['product_re'] = self.apk_warehouse_id.product_re
            line_ids = filter_lines(lines.sorted(key=lambda r: (r.location_id.removal_priority, r.write_date), reverse = True))
            lines = {}
            _logger.info("Inventario: {} ({})".format(inventory_id.display_name, inventory_id.id))
            _logger.info("---> Lineas para esta ubicación/producto: {}".format(len(line_ids)))
            for line in line_ids:
                barcode = line.location_id.barcode
                code = line.product_id.wh_code
                if not barcode in lines.keys():
                    LocationIndex += 1
                    lines[barcode] = {'id': line.location_id.id,
                                      'LocationIndex': LocationIndex,
                                      'show': True,
                                      'name': line.location_id.name,
                                      'barcode': line.location_id.barcode, 'product_ids': {}}
                if not code in lines[barcode]['product_ids'].keys():
                    ProductIndex += 1
                    lines[barcode]['product_ids'][code] = { 'id': line.product_id.id,
                                                            'ProductIndex': ProductIndex,
                                                            'default_code': line.product_id.default_code,
                                                            'wh_code': line.product_id.wh_code,
                                                            'tracking': line.product_id.tracking,
                                                            'theoretical_qty': 0,
                                                            'product_qty': 0,
                                                            'barcode_length': 0,
                                                            'line_ids': []}
                LineIndex += 1
                val = {
                    'id': line.id,
                    'LineIndex': LineIndex,
                    'lot_id': {'id': line.prod_lot_id.id, 'name': line.prod_lot_id.name},
                    'qty_dirty': line.product_qty > 0,
                    'theoretical_qty': line.theoretical_qty,
                    'product_qty': line.product_qty}
                if line.prod_lot_id:
                    lines[barcode]['product_ids'][code]['barcode_length'] = len(line.prod_lot_id.name)
                lines[barcode]['product_ids'][code]['theoretical_qty'] += line.theoretical_qty
                lines[barcode]['product_ids'][code]['product_qty'] += line.product_qty
                if len(lines[barcode]['product_ids'][code]['line_ids']) < max_serial_lines:
                    lines[barcode]['product_ids'][code]['line_ids'].append(val)
            res_lines = []
            for barcode in lines.keys():
                loc = lines[barcode]
                product_ids = []
                for wh_code in loc['product_ids'].keys():
                    product = loc['product_ids'][wh_code]
                    product_ids.append(product)
                loc['product_ids'] = product_ids
                res_lines.append(loc)
            res['inventory_location_ids'] = res_lines

        if len(res['inventory_location_ids']) == 1:
            res['ActiveLocation'] = location_id
            product_ids = res['inventory_location_ids'][0]['product_ids']
            if len(product_ids) == 1:
                res['barcode_length'] = product_ids[0]['barcode_length']
        if not res['ActiveLocation']:
            res['ActiveLocation'] = location_id
        if False:
            print("\n\n#######################################\n#######################################")
            pprint.PrettyPrinter(indent=2).pprint(res)
            print("#######################################\n#######################################")
            pprint.PrettyPrinter(indent=2).pprint(values)
            print("#######################################\n#######################################")
        return res

    def get_model_object(self, values={}):
        if False:
            print("#######################################\n#######################################")
            pprint.PrettyPrinter(indent=2).pprint(values)

        if self and not values:
            return super().get_model_object(values=values)
        id = values.get('id', self and self.id or False)
        show_stock = values.get('show_stock', False)
        show_inventory = values.get('show_inventory', True)
        show_list = not(show_stock or show_inventory)
        location_id = id
        filter_inventory = values.get('filter_inventory', {})
        product_id = values.get('product_id', filter_inventory.get('product_id', False))
        values['inventory_id'] = inventory_id = values.get('inventory_id', filter_inventory.get('inventory_id', False))
        domain = values.get('domain', [])
        inventory = self.env['stock.inventory']
        if not location_id and not product_id and not inventory_id and not domain:
            raise ValidationError ('No puedo mostrar datos sin ubicación, artículo o inventario')
        ## Si hay un inventario para ese producto voy directo al inventario

        if not inventory_id and show_inventory:
            _logger.info ('Saco la ubicación de un inventario del producto')
            domain = [('filter', '=', 'product'),
                      ('state', '=', 'confirm')]
            if product_id:
                domain += [('product_id', '=', product_id)]
            if location_id:
                domain += [('location_id', '=', location_id)]
            inventory = self.env['stock.inventory'].search(domain, limit=1)

            if not inventory_id:
                domain = [('inventory_id.filter', '=', 'none'),
                          ('inventory_id.state', '=', 'confirm')]
                if product_id:
                    domain += [('product_id', '=', product_id)]
                if location_id:
                    domain += [('location_id', '=', location_id)]
                inventory = self.env['stock.inventory.line'].search(domain, limit=1).mapped('inventory_id')

            if inventory:
                if not location_id:
                    location_id = inventory.location_id.id
                inventory_id = inventory.id
                values.update(show_inventory=True, inventory_id=inventory_id)

        if self or domain:
            res = super().get_model_object(values=values)
        elif location_id:
            values['domain'] = [('id', '=', location_id)]
            res = super().get_model_object(values=values)


        if not values.get('active_location', False) and location_id:
            res[0]['ActiveLocation'] = values['active_location'] = location_id
        if not values.get('active_product', False) and product_id:
            res[0]['ActiveProduct'] = values['active_product'] = product_id

        if show_list:
            ##LISTADO DE UBICACIONES
            _logger.info("Sacando listado de ubicaciones")
            return res

        if show_inventory:
            ## INFORMACIÓN DE INVENTARIO
            _logger.info("Sacando inventario")
            res[0].update(self.get_apk_inventory(values))
            # _logger.info (res)
            #pprint.PrettyPrinter(indent=2).pprint(res)
            return res

        ## SACO STOCK
        if location_id or product_id:
            res[0]['empty'] = True
            res[0].update({'inventory': False,
                           'inventory_id': 0})
            q_values = {}
            if location_id:
                q_values.update(location_id=location_id)
            if product_id:
                q_values.update(product_id=product_id)
            res[0]['quants'] = self.env['stock.quant']._gather_apk(q_values)
            if res[0]['quants']:
                res[0]['empty'] = False


        if False:
            print("#######################################\n#######################################")
            pprint.PrettyPrinter(indent=2).pprint(values)
            print("#######################################\n#######################################")
            pprint.PrettyPrinter(indent=2).pprint(res)
            print("#######################################\n#######################################")
        return res

    @api.model
    def new_inventory(self, values):

        location_id = self.env['stock.location'].browse(values.get('location_id'))
        product_id = self.env['product.product'].browse(values.get('product_id'))
        filter_name = values.get('filter', 'none')
        # Creo un inventario
        # Si no hay ubicación cojo por defecto
        if not location_id:
            company_user = self.env.user.company_id
            wh_id = self.env['stock.warehouse'].search([('company_id', '=', company_user.id)], limit=1)
            location_id = wh_id.lot_stock_id
        # Si no hay producto, sobreescribo el filtro

        if not product_id:
            if filter_name == 'none':
                filter_name = 'Todos'
            else:
                filter_name = 'Manual'
                vals = {'location_id': location_id.id,
                        'filter': values.get('filter'),
                        'name': '{}: {}'.format(location_id.name, filter_name)}

        if product_id:
            vals.update(filter='partial')
        else:
            vals.update(filter='none')

        ##Busco un inventario
        inv_domain = [('state', '=', 'confirm'),
                      ('location_id', '=', location_id.id)]
        if product_id:
            inv_domain += [('product_id', '=', product_id.id)]
        inventory = self.env['stock.inventory'].search(inv_domain, limit=1)

        if not inventory:
            inv_domain = [('inventory_id.state', '=', 'confirm'),
                          ('location_id', '=', location_id.id)]
            if product_id:
                inv_domain += [('product_id', '=', product_id.id)]
            inventory = self.env['stock.inventory.line'].search(inv_domain, limit=1).mapped('inventory_id')
            if inventory:
                raise ValidationError ("Ya existe un inventario: {} ({})".format(inventory.name, inventory.id))
        if not inventory and values.get('create_inventory', False):
            ##Entonces lo creo
            vals = {'location_id': location_id.id,
                    'filter': 'none',
                    'name': '{}: {}'.format(location_id.name, product_id.default_code)}
            if product_id:
                vals.update(product_id=product_id.id, filter='product')
            inventory = self.env['stock.inventory'].create(vals)
            inventory.action_start()

        values.update(inventory_id=inventory.id,
                      location_id = location_id.id,
                      filter={},
                      show_inventory=True)

        return location_id.get_model_object(values)
        if product_id:
            if product_id.tracking != 'serial':
                strat_id = location_id.putaway_strategy_id
                ## si el inventario no tiene líneas creo una en la ubicación predeterminada si el producto la tiene
                ##PORQUEEEEEE
                line = product_id.product_putaway_ids.filtered(lambda x: x.putaway_id == strat_id)
                if line:
                    self.env['stock.inventory.line'].create(
                            {'product_id': product_id.id,
                             'location_id': line.fixed_location_id.id,
                             'inventory_id': inventory and inventory.id})
            return {'location_id': location_id.id, 'inventory_id': inventory and inventory.id}
        return location_id.get_model_object(values)


    @api.multi
    def update_stock_location(self):
        for loc in self.search([('usage', '=', 'internal')]):
            loc.barcode = loc.name
    @api.multi
    def generate_inventory(self):
        si_ids = self.env['stock.inventory']
        sfps = self.env['stock.fixed.putaway.strat']
        putaway_strategy_id = False
        location_id = self
        while not putaway_strategy_id and location_id:
            putaway_strategy_id = location_id.putaway_strategy_id
            if not putaway_strategy_id:
                location_id = location_id.location_id

        if not putaway_strategy_id:
            raise ValidationError ('No se ha encontrado estrategia de traslado para la ubicación')

        lines_domain = [('putaway_id', '=', putaway_strategy_id.id), ('fixed_location_id', 'child_of', self.id)]
        sfps_ids = sfps.search(lines_domain)
        strat_name = putaway_strategy_id.name
        for line in sfps_ids:
            name = '{}:{}'.format(strat_name, line.fixed_location_id.name)
            domain = [('name', '=', name), ('location_id', '=', line.fixed_location_id.id), ('state', '=', 'draft'),
                      ('filter', '=', 'products')]
            si_id = si_ids.search(domain)
            if not si_id:
                val = {'name': name, 'location_id': line.fixed_location_id.id, 'filter': 'products', 'exhausted': True}
                si_id = si_ids.create(val)
            si_ids |= si_id
            si_id.write({'product_ids': [(4, line.product_id.id)]})
        for si in si_ids:
            si.action_start()