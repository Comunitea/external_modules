# -*- coding: utf-8 -*-


from odoo import api, models, fields

class StockInventory(models.Model):
    _inherit = ['stock.inventory']

    @api.model
    def action_validate_apk(self, values):
        inventory_id = self.browse(values.get('inventory_id'))
        if values.get('cancel', False):
            inventory_id.action_cancel_draft()
            inventory_id.unlink()
        else:
            inventory_id.action_validate()
        location_id = self.env['stock.location'].browse(values.get('location_id'))
        return location_id.get_model_object()

    def _get_inventory_lines_values_apk(self, location_id, product_id):
        # TDE CLEANME: is sql really necessary ? I don't think so
        locations = self.env['stock.location'].search([('id', 'child_of', [location_id.id])])
        domain = ' location_id in %s AND quantity != 0 AND active = TRUE'
        args = (tuple(locations.ids),)

        vals = []
        Product = self.env['product.product']
        # Empty recordset of products available in stock_quants
        quant_products = self.env['product.product']
        # Empty recordset of products to filter
        products_to_filter = self.env['product.product']

        # case 0: Filter on company
        if self.company_id:
            domain += ' AND company_id = %s'
            args += (self.company_id.id,)

        #case 1: Filter on One owner only or One product for a specific owner
        if self.partner_id:
            domain += ' AND owner_id = %s'
            args += (self.partner_id.id,)
        #case 2: Filter on One Lot/Serial Number
        if self.lot_id:
            domain += ' AND lot_id = %s'
            args += (self.lot_id.id,)
        #case 3: Filter on One product
        if self.product_id:
            domain += ' AND product_id = %s'
            args += (product_id.id,)
            products_to_filter |= product_id
        #case 4: Filter on A Pack
        if self.package_id:
            domain += ' AND package_id = %s'
            args += (self.package_id.id,)
        #case 5: Filter on One product category + Exahausted Products
        if self.category_id:
            categ_products = Product.search([('categ_id', 'child_of', self.category_id.id)])
            domain += ' AND product_id = ANY (%s)'
            args += (categ_products.ids,)
            products_to_filter |= categ_products

        self.env.cr.execute("""SELECT product_id, sum(quantity) as product_qty, location_id, lot_id as prod_lot_id, package_id, owner_id as partner_id
            FROM stock_quant
            LEFT JOIN product_product
            ON product_product.id = stock_quant.product_id
            WHERE %s
            GROUP BY product_id, location_id, lot_id, package_id, partner_id """ % domain, args)

        for product_data in self.env.cr.dictfetchall():
            # replace the None the dictionary by False, because falsy values are tested later on
            for void_field in [item[0] for item in product_data.items() if item[1] is None]:
                product_data[void_field] = False
            product_data['theoretical_qty'] = product_data['product_qty']
            if product_data['product_id']:
                product_data['product_uom_id'] = Product.browse(product_data['product_id']).uom_id.id
                quant_products |= Product.browse(product_data['product_id'])
            vals.append(product_data)

            exhausted_vals = self._get_exhausted_inventory_line(products_to_filter, quant_products)
            vals.extend(exhausted_vals)
        return vals

    @api.model
    def load_eans(self, values):
        inventory_id = self.browse(values.get('inventory_id', False))
        product_id = values.get('product_id', False)
        location_id = values.get('location_id', False)
        ean_ids = values.get('ean_ids', '')
        vals = []
        domain = [('inventory_id', '=', inventory_id.id), ('product_id', '=', product_id), ('location_id', '=', location_id)]
        sil = self.env['stock.inventory.line']
        pre_filter = inventory_id.filter
        pre_product = inventory_id.product_id
        inventory_id.filter = 'product'
        inventory_id.product_id = product_id
        lot_names = []
        if ean_ids:
            ean_ids = values.get('ean_ids').split()
        else:
            ean_ids = []
        for ean in ean_ids:
            if ean in lot_names or not ean:
                continue
            lot_names += ean
            lot_domain = [('product_id', '=', product_id), ('name', '=', ean)]
            lot_id = self.env['stock.production.lot'].search(lot_domain)
            if not lot_id:
                lot_vals = {'product_id': product_id, 'name': ean}
                lot_id = self.env['stock.production.lot'].create(lot_vals)
            line_domain = domain + ['|', ('prod_lot_id', '=', False), ('prod_lot_id', '=', lot_id.id)]
            line_id = sil.search(line_domain, limit=1)
            if not line_id:
                vals = {'product_id': product_id,
                        'location_id': location_id,
                        'inventory_id': inventory_id.id,
                        'prod_lot_id': lot_id.id}
                line_id = sil.create(vals)
                line_id._compute_theoretical_qty()
            else:
                if not line_id.prod_lot_id:
                    line_id.prod_lot_id = lot_id
            line_id.product_qty = 1
        inventory_id.product_id = pre_product
        inventory_id.filter = pre_filter
        values.update(
            active_product=product_id,
            active_location=location_id)
        values.pop('ean_ids')
        return self.env['stock.location'].get_apk_inventory(values)

    def post_inventory100(self):
        # The inventory is posted as a single step which means quants cannot be moved from an internal location to another using an inventory
        # as they will be moved to inventory loss, and other quants will be created to the encoded quant location. This is a normal behavior
        # as quants cannot be reuse from inventory location (users can still manually move the products before/after the inventory if they want).
        self.mapped('move_ids').filtered(lambda move: move.state != 'done')[:100]._action_done()