# Copyright 2018 GRAP - Sylvain LE GAL
# Copyright 2018 Tecnativa S.L. - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class PromotionsRulesConditionsExprs(models.Model):
    _inherit = 'promos.rules.conditions.exps'

    serialised_pos = fields.Char('Expression POS')

    def serialise_pos(self, attribute, comparator, value):
        """        
        Compute serialised_pos field whitch will be evaluated in javascript
        in the PoS.
        """
        res = "this.%s %s %s" % (attribute, comparator, value)
        if attribute == 'amount_untaxed':
            res = "this.get_subtotal() %s %s" % (comparator, value)
        if attribute == 'custom':
            return value
        if attribute == 'product':
            return 'products.includes(%s)' % (value)
        if attribute in ['prod_qty',
                         'prod_unit_price',
                         'prod_sub_total',
                         'prod_discount',
                         'prod_weight',
                         'prod_net_price',
                         ]:
            product_code, quantity = value.split(",")
            res = '(products.includes("%s")) && (%s["%s"] %s %s)' \
                  % (eval(product_code), attribute, eval(product_code),
                     comparator, quantity)
        
        # TODO CON LAS FUNCIONES REDUCE Y MAP SE HARÁ BIEN
        # if attribute == 'comp_sub_total':
        #     product_codes_iter, value = value.split("|")
        #     res = """sum(
        #         [prod_sub_total.get(prod_code,0) for prod_code in %s]
        #         ) %s %s""" % (eval(product_codes_iter), comparator, value)
        # if attribute == 'comp_sub_total_x':
        #     product_codes_iter, value = value.split("|")
        #     res = """(sum(prod_sub_total.values()) - sum(
        #         [prod_sub_total.get(prod_code,0) for prod_code in %s]
        #         )) %s %s""" % (eval(product_codes_iter), comparator, value)

        # if attribute == 'ship_address':
        #     res = """order.partner_shipping_id.city == %s""" % value
        # if attribute == 'pallet':
        #     res = """sum(prod_pallet.values()) %s %s""" % (comparator, value)
        # if attribute == 'prod_pallet':
        #     product_code, qty = value.split(',')
        #     res = """prod_pallet.get(%s, 0.0) %s %s""" %\
        #         (product_code, comparator, qty)
        return res

    @api.model
    def create(self, vals):
        """
        Compute serialised_pos field
        """
        vals['serialised_pos'] = self.serialise_pos(vals['attribute'],
                                                    vals['comparator'],
                                                    vals['value'])
        return super(PromotionsRulesConditionsExprs, self).create(vals)

    def write(self, vals):
        """
        Compute serialised_pos field
        """
        # Validate before save
        old_vals = self.read(['attribute', 'comparator', 'value'])[0]
        old_vals.update(vals)
        'id' in old_vals and old_vals.pop('id')
        self.validate(old_vals)

        # Only value may have changed and client gives only value
        vals = old_vals
        vals['serialised_pos'] = self.serialise_pos(vals['attribute'],
                                                    vals['comparator'],
                                                    vals['value'])
        return super(PromotionsRulesConditionsExprs, self).write(vals)
