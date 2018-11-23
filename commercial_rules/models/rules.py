# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models, _
from odoo.exceptions import UserError


DEBUG = True
PRODUCT_UOM_ID = 1

ATTRIBUTES = [
    # ('prod_net_price', 'Product NetPrice combination'),
    # ('tot_item_qty', 'Total Items Quantity'),
    # ('tot_weight', 'Total Weight'),
    # ('tot_item_qty', 'Total Items Quantity'),
    ('amount_untaxed', _('Untaxed Total')),
    ('amount_tax', 'Tax Amount'),
    ('amount_total', 'Total Amount'),
    ('product', 'Product Code in order'),
    ('prod_qty', 'Product Quantity combination'),
    ('prod_unit_price', 'Product UnitPrice combination'),
    ('prod_sub_total', 'Product SubTotal combination'),
    ('prod_discount', 'Product Discount combination'),
    ('prod_weight', 'Product Weight combination'),
    ('comp_sub_total', 'Compute sub total of products'),
    ('comp_sub_total_x', 'Compute sub total excluding products'),
    ('custom', 'Custom domain expression'),
    # ('pallet', 'Number of entire pallets'),
    # ('prod_pallet', 'Number pallets of product'),
    ('ship_address', 'Ship Address City'),
]

COMPARATORS = [
    ('==', _('equals')),
    ('!=', _('not equal to')),
    ('>', _('greater than')),
    ('>=', _('greater than or equal to')),
    ('<', _('less than')),
    ('<=', _('less than or equal to')),
    ('in', _('is in')),
    ('not in', _('is not in')),
]

ACTION_TYPES = [
    ('prod_disc_perc', _('Discount % on Product')),
    ('prod_disc_fix', _('Fixed amount on Product')),
    ('cart_disc_perc', _('Discount % on Sub Total')),
    ('cart_disc_fix', _('Fixed amount on Sub Total')),
    ('prod_x_get_y', _('Buy X get Y free')),
    ('buy_x_pay_y', _('Buy X pay Y')),
    ('prod_free', _('Get product for free')),
    # ('line_prod_disc_perc', _('New line discount, over order subtotal')),
    # ('line_discount_group_price', _('New line discount, over price unit')),
    # ('line_discount_mult_pallet', _('New line discount, multiply of pallet')),
]


class PromotionsRules(models.Model):
    _name = "promos.rules"
    _order = 'sequence'

    # def count_coupon_use(self):
    #     '''
    #     This function count the number of sale orders(not in cancelled state)
    #     that are linked to a particular coupon.
    #     '''
    #     sales_obj = self.env['sale.order']
    #     num_cupons = 0
    #     for promotion_rule in self:
    #         if promotion_rule.coupon_code:
    #             # If there is uses per coupon defined check if its overused
    #             if promotion_rule.uses_per_coupon > -1:
    #                 domain = [
    #                     ('coupon_code', '=', promotion_rule.coupon_code),
    #                     ('state', '!=', 'cancel')
    #                 ]
    #                 num_cupons = len(sales_obj.search(domain))
    #         promotion_rule.update({'coupon_used': num_cupons})

    name = fields.Char('Rule Name', required=True)
    description = fields.Text('Description')
    active = fields.Boolean('Active', default=True)
    stop_further = fields.Boolean('Stop Checks',
                                  help="Stops further promotions being\
                                  checked")
    partner_categories = fields.Many2many('res.partner.category',
                                          'rule_partner_cat_rel',
                                          'category_id',
                                          'rule_id',
                                          copy=True,
                                          string="Partner Categories",
                                          help="Applicable to all if \
                                                none is selected")
    # coupon_code = fields.Char('Coupon Code')
    # uses_per_coupon = fields.Integer('Uses per Coupon')
    # uses_per_partner = fields.Integer('Uses per Partner')
    # coupon_used = fields.Integer('Number of Coupon Uses',
    #                              compute='count_coupon_use',
    #                              help='The number of times this coupon \
    #                                   has been used.')
    from_date = fields.Datetime('From Date')
    to_date = fields.Datetime('To Date')
    sequence = fields.Integer('Sequence', required=True)
    logic = fields.Selection([('and', 'All'), ('or', 'Any')],
                             string="Logic",
                             required=True,
                             default='and')
    expected_logic_result = fields.Selection([('True', 'True'),
                                             ('False', 'False')],
                                             string="Output",
                                             required=True,
                                             default='True')
    expressions = fields.One2many('promos.rules.conditions.exps',
                                  'promotion',
                                  copy=True,
                                  string='Expressions/Conditions')
    actions = fields.One2many('promos.rules.actions', 'promotion',
                              string="Actions",
                              copy=True)
    partner_ids = fields.Many2many('res.partner',
                                   'rule_partner_rel',
                                   'partner_id',
                                   'rule_id',
                                   domain=[('customer', '=', True)],
                                   string="Partner",
                                   help="Applicable to all if none is \
                                   selected")

    def promotion_date(self, str_date):
        """ Converts string date to date """
        import time
        try:
            return time.strptime(str_date, '%Y-%m-%d %H:%M:%S')
        except:
            try:
                return time.strptime(str_date, '%Y-%m-%d')
            except:
                return str_date

    def check_primary_conditions(self, order):
        """
        Checks the conditions for
            Coupon Code
            Validity Date
        """
        self.ensure_one()
        sales_obj = self.env['sale.order']
        # Check if the customer is in the specified partner cats
        if self.partner_categories:
            applicable_ids = [
                category.id for category in self.partner_categories
            ]
            partner_categories = [
                category.id for category in order.partner_id.category_id]
            if not set(applicable_ids).intersection(partner_categories):
                raise UserError("Not applicable to Partner Category")
        # if self.coupon_code:
        #     # If the codes don't match then this is not the promo
        #     if not order.coupon_code == self.coupon_code:
        #         raise UserError("Coupon codes do not match")
        #     # Calling count_coupon_use to check whether no. of
        #     # uses is greater than allowed uses.
        #     count = self.count_coupon_use
        #     if count > self.uses_per_coupon:
        #         raise UserError("Coupon is overused")
        #     # If a limitation exists on the usage per partner
        #     if self.uses_per_partner > -1:
        #         domain = [
        #             ('partner_id', '=', order.partner_id.id),
        #             ('coupon_code', '=', self.coupon_code),
        #             ('state', '<>', 'cancel')
        #         ]
        #         matching_objs = sales_obj.search(domain)
        #         if len(matching_objs) > self.uses_per_partner:
        #             raise UserError("Customer already used coupon")

        # If a start date has been specified
        if self.from_date and \
            not (self.promotion_date(
                order.date_order) >=
                self.promotion_date(self.from_date)):
            raise UserError("Order before start of promotion")

        # If an end date has been specified
        if self.to_date and \
            not (self.promotion_date(
                order.date_order) <=
                self.promotion_date(self.to_date)):
            raise UserError("Order after end of promotion")

        # All tests have succeeded
        return True

    def execute_actions(self, order):
        """
        """
        self.ensure_one()

        for action in self.actions:
            action.execute(order)
        return True

    def evaluate(self, order):
        """
        """
        self.ensure_one()

        self.check_primary_conditions(order)
        # Now to the rules checking
        expected_result = eval(self.expected_logic_result)
        logic = self.logic
        # Evaluate each expression
        for expression in self.expressions:
            result = 'Execution Failed'
            result = expression.evaluate(order)

            # For and logic, any False is completely false
            if (not (result == expected_result)) and (logic == 'and'):
                return False
            # For OR logic any True is completely True
            if (result == expected_result) and (logic == 'or'):
                return True
            # If stop_further is given, then execution stops  if the
            # condition was satisfied
            if (result == expected_result) and expression.stop_further:
                return True
        if logic == 'and':
            # If control comes here for and logic, then all conditions were
            # satisfied
            return True
        else:
            # if control comes here for OR logic, none were satisfied
            return False

    @api.model
    def _get_promotions_domain(self, order):
        """
        Obtengo domain del tipo A AND (B OR C) AND (D OR F) ....
        """
        categ_ids = []
        if order.partner_id.category_id:
            categ_ids = [x.id for x in order.partner_id.category_id]
        domain = ['&', '&', '&', '&',
                  ('active', '=', True),
                  '|',
                  ('partner_ids', '=', False),
                  ('partner_ids', 'in', [order.partner_id.id]),
                  '|',
                  ('partner_categories', '=', False),
                  ('partner_categories', 'in', categ_ids),
                  '|',
                  ('from_date', '=', False),
                  ('from_date', '<=', order.date_order),
                  '|',
                  ('to_date', '=', False),
                  ('to_date', '>=', order.date_order)]

        if categ_ids:
            domain += ['|', ('partner_categories', 'in', categ_ids),
                       ('partner_categories', '=', False)]
        else:
            domain += [('partner_categories', '=', False)]
        return domain

    @api.model
    def apply_promotions(self, order_id):
        """
        Get all active promiotions, evaluate it, and execute if evaluation
        is true
        """
        order = self.env['sale.order'].browse(order_id)
        domain = self._get_promotions_domain(order)
        active_promos = self.search(domain)
        for promotion_rule in active_promos:
            result = promotion_rule.evaluate(order)
            if result:
                promotion_rule.execute_actions(order)
                # If stop further is true stop here
                if promotion_rule.stop_further:
                    return True
        return True


class PromotionsRulesConditionsExprs(models.Model):
    "Expressions for conditions"
    _name = 'promos.rules.conditions.exps'
    _order = "sequence"
    _rec_name = 'serialised_expr'

    sequence = fields.Integer('Sequence')
    attribute = fields.Selection(ATTRIBUTES, 'Attribute', size=50,
                                 required=True)
    comparator = fields.Selection(COMPARATORS, 'Comparator',
                                  required=True, default='==')
    value = fields.Char('Value', default='0.00')
    serialised_expr = fields.Char('Expression')
    promotion = fields.Many2one('promos.rules', 'Promotion')
    stop_further = fields.Boolean('Stop further checks')

    @api.onchange('attribute')
    def on_change_attribute(self):
        """
        Set the value field to the format if nothing is there
        """
        # If attribute is not there then return.
        # Will this case be there?
        if not self.attribute:
            return
        # If value is not null or one of the defaults
        if self.value not in [
            False,
            "'product_code'",
            "'product_code',0.00",
            "['product_code','product_code2']|0.00",
            "0.00",
        ]:
            return {}
        # Case 1
        if self.attribute == 'product':
            self.value = "'product_code'"
        # Case 2
        if self.attribute in ['prod_qty',
                              'prod_unit_price',
                              'prod_sub_total',
                              'prod_discount',
                              'prod_weight',
                              'prod_net_price']:
            self.value = "'product_code',0.00"
        # Case 3
        if self.attribute in ['comp_sub_total',
                              'comp_sub_total_x']:
            self.value = "['product_code','product_code2']|0.00"
        # Case 4
        if self.attribute in ['amount_untaxed', 'amount_tax', 'amount_total']:
            self.value = "0.00"

        # Case 5
        # if self.attribute in ['pallet']:
        #     self.value = "0.00"

        # Case 6
        if self.attribute in ['ship_address']:
            self.value = "'city_name'"

        # Case 7
        # if self.attribute in ['prod_pallet']:
        #     self.value = "'product_code',0.00"

        return {}

    def validate(self, vals):
        """
        Checks the validity
        """
        numerical_comparators = ['==', '!=', '<=', '<', '>', '>=']
        iterator_comparators = ['in', 'not in']
        attribute = vals['attribute']
        comparator = vals['comparator']
        value = vals['value']
        # Mismatch 1:
        if attribute in ['amount_untaxed',
                         'amount_tax',
                         'amount_total',
                         'prod_qty',
                         'prod_unit_price',
                         'prod_sub_total',
                         'prod_discount',
                         'prod_weight',
                         'prod_net_price',
                         'comp_sub_total',
                         'comp_sub_total_x',
                        #  'pallet'
                         ] and comparator not in numerical_comparators:
            raise UserError("Only %s can be used with %s"
                            % (",".join(numerical_comparators), attribute))
        # Mismatch 2:
        if attribute == 'product' and comparator not in iterator_comparators:
            raise UserError("Only %s can be used with Product Code"
                            % ",".join(iterator_comparators))
        # Mismatch 3:
        if attribute in ['prod_qty',
                         'prod_unit_price',
                         'prod_sub_total',
                         'prod_discount',
                         'prod_weight',
                         'prod_net_price',
                        #  'prod_pallet',
                         ]:
            if len(value.split(",")) != 2:
                raise UserError("Value for %s combination is invalid\n"
                                "Eg for right format is `'PC312',120.50`"
                                % attribute)
            product_code, quantity = value.split(",")
            if not (type(eval(product_code)) == str and
                    type(eval(quantity)) in [int, float]):
                raise UserError("Value for %s combination is invalid\n"
                                "Eg for right format is `'PC312',120.50`"
                                % attribute)
        # Mismatch 4:
        if attribute in ['comp_sub_total',
                         'comp_sub_total_x']:
            if len(value.split(",")) != 2:
                raise UserError(
                    "Value for computed subtotal combination is invalid\n"
                    "Eg for right format is `['code1,code2',..]|120.50`")
            product_codes_iter, quantity = value.split("|")
            if not (type(eval(product_codes_iter)) in [tuple, list] and
                    type(eval(quantity)) in [int, float]):
                raise UserError(
                    "Value for computed subtotal combination is invalid\n"
                    "Eg for right format is `['code1,code2',..]|120.50`")

        # Mismarch 5_
        if attribute == 'ship_address' and comparator != '==':
            raise UserError("Only comparator '==' is allowed for this \
                             attribute")

        # After all validations say True
        return True

    def serialise(self, attribute, comparator, value):
        """
        Constructs an expression from the entered values
        which can be quickly evaluated
        @param attribute: attribute of promo expression
        @param comparator: Comparator used in promo expression.
        @param value: value according which attribute will be compared
        """

        res = "order.%s %s %s" % (attribute, comparator, value)

        if attribute == 'custom':
            return value
        if attribute == 'product':
            return '%s %s products' % (value,
                                       comparator)
        if attribute in ['prod_qty',
                         'prod_unit_price',
                         'prod_sub_total',
                         'prod_discount',
                         'prod_weight',
                         'prod_net_price',
                         ]:
            product_code, quantity = value.split(",")
            res = '(%s in products) and (%s["%s"] %s %s)' \
                  % (product_code, attribute, eval(product_code),
                     comparator, quantity)
        if attribute == 'comp_sub_total':
            product_codes_iter, value = value.split("|")
            res = """sum(
                [prod_sub_total.get(prod_code,0) for prod_code in %s]
                ) %s %s""" % (eval(product_codes_iter), comparator, value)
        if attribute == 'comp_sub_total_x':
            product_codes_iter, value = value.split("|")
            res = """(sum(prod_sub_total.values()) - sum(
                [prod_sub_total.get(prod_code,0) for prod_code in %s]
                )) %s %s""" % (eval(product_codes_iter), comparator, value)
        # if attribute == 'pallet':
        #     res = """sum(prod_pallet.values()) %s %s""" % (comparator, value)
        if attribute == 'ship_address':
            res = """order.partner_shipping_id.city == %s""" % value
        # if attribute == 'prod_pallet':
        #     product_code, qty = value.split(',')
        #     res = """prod_pallet.get(%s, 0.0) %s %s""" %\
        #         (product_code, comparator, qty)
        return res

    def evaluate(self, order, **kwargs):
        """
        Evaluates the expression in given environment
        @param cr: Database cr
        @param uid: ID of uid
        @param expression: Browse record of expression
        @param order: Browse Record of sale order
        @param context: Context(no direct use).
        @return: True if evaluation succeeded
        """
        products = []   # List of product Codes
        prod_qty = {}   # Dict of product_code:quantity
        # prod_pallet = {}   # Dict of product_code:number_of_pallets
        prod_unit_price = {}
        prod_sub_total = {}
        prod_discount = {}
        prod_weight = {}
        # prod_net_price = {}
        prod_lines = {}

        for line in order.order_line.\
                filtered(lambda l: not l.product_id.no_promo):
            if line.product_id:
                product_code = line.product_id.code
                products.append(product_code)
                prod_lines[product_code] = line.product_id
                prod_qty[product_code] = \
                    prod_qty.get(product_code, 0.00) + line.product_uom_qty
                prod_unit_price[product_code] = \
                    prod_unit_price.get(product_code, 0.00) + line.price_unit
                prod_sub_total[product_code] = \
                    prod_sub_total.get(product_code, 0.00) + \
                    line.price_subtotal
                prod_discount[product_code] = \
                    prod_discount.get(product_code, 0.00) + line.discount
                prod_weight[product_code] = \
                    prod_weight.get(product_code, 0.00) + \
                    line.product_id.weight

                # Get number of entire pallets
                # entire_pallets = 0
                # packing = line.product_id.packaging_ids and \
                #     line.product_id.packaging_ids[0] or False
                # if packing and packing.ul_type == 'pallet' and packing.qty:
                #     entire_pallets = line.product_uom_qty // packing.qty

                # prod_pallet[product_code] = \
                #     prod_pallet.get(product_code, 0.00) + entire_pallets
        return eval(self.serialised_expr)

    @api.model
    def create(self, vals):
        """
        Serialise before save
        @param cr: Database cr
        @param uid: ID of uid
        @param vals: Values of current record.
        @param context: Context(no direct use).
        """
        self.validate(vals)
        vals['serialised_expr'] = self.serialise(vals['attribute'],
                                                 vals['comparator'],
                                                 vals['value'])
        return super(PromotionsRulesConditionsExprs, self).create(vals)

    def write(self, vals):
        """
        Serialise before Write
        @param cr: Database cr
        @param uid: ID of uid
        @param ids: ID of current record.
        @param vals: Values of current record.
        @param context: Context(no direct use).
        """
        # Validate before save

        old_vals = self.read(['attribute', 'comparator', 'value'])[0]
        old_vals.update(vals)
        'id' in old_vals and old_vals.pop('id')
        self.validate(old_vals)

        # Only value may have changed and client gives only value
        vals = old_vals
        vals['serialised_expr'] = self.serialise(vals['attribute'],
                                                 vals['comparator'],
                                                 vals['value'])
        return super(PromotionsRulesConditionsExprs, self).write(vals)


class PromotionsRulesActions(models.Model):
    _name = 'promos.rules.actions'
    _rec_name = 'action_type'

    sequence = fields.Integer('Sequence', required=True)
    action_type = fields.Selection(ACTION_TYPES, 'Action', required=True)
    product_code = fields.Char('Product Code')
    arguments = fields.Char('Arguments')
    promotion = fields.Many2one('promos.rules', 'Promotion')

    @api.onchange('action_type')
    def on_change(self):

        """
        Sets the arguments as templates according to action_type
        @param cr: Database cr
        @param uid: ID of uid
        @param ids: ID of current record
        @param action_type: type of action to be taken
        @product_code: Product on which action will be taken.
                (Only in cases when attribute in expression is product.)
        @param arguments: Values that will be used in implementing of actions
        @param context: Context(no direct use).
        """
        if not self.action_type:
            return
        if self.arguments not in [False, "0.00", "1,1"] and \
                self.product_code in ["'product_code'", "'product_code_of_y'"
                                      "'product_code_x'", "'product_code_y'"]:
                return {}
        if self.action_type in ['prod_disc_perc', 'prod_disc_fix', 'prod_free']:
            self.product_code = "'product_code'"
            self.arguments = "0.00"
        if self.action_type in ['cart_disc_perc', 'cart_disc_fix']:
            self.product_code = False
            self.arguments = "0.00"
        if self.action_type in ['prod_x_get_y']:
            self.product_code = "'product_code_x','product_code_y'"
            self.arguments = "qty_x, qty_y"
        if self.action_type in ['buy_x_pay_y']:
            self.product_code = "'product_code'"
            self.arguments = "qty_x, qty_y"
        # Finally if nothing works
        return

    def create_line(self, vals):
        return self.env['sale.order.line'].create(vals)

    def action_prod_disc_perc(self, order):
        """
        Action for 'Discount % on Product'
        """
        for order_line in order.order_line.\
                filtered(lambda l: not l.product_id.no_promo):
            if order_line.product_id.code == eval(self.product_code):
                return order_line.\
                    write({'discount': eval(self.arguments),
                           'old_discount': order_line.discount})

    def action_prod_disc_fix(self, order):
        """
        Action for 'Fixed amount on Product'
        """
        # order_line_obj = self.pool.get('sale.order.line')
        product_obj = self.env['product.product']
        line_name = '%s on %s' % (self.promotion.name,
                                  eval(self.product_code))
        domain = [('default_code', '=', eval(self.product_code))]
        product = product_obj.search(domain, limit=1)
        if not product:
            raise UserError("No product with the product code")
        args = {
            'order_id': order.id,
            'name': line_name,
            'promotion_line': True,
            'price_unit': -eval(self.arguments),
            'product_uom_qty': 1,
            'product_uom': product.uom_id.id,
            'product_id': product.id
        }
        self.create_line(args)
        return True

    def action_cart_disc_perc(self, order):
        """
        Discount % on Sub Total
        """
        args = {
            'order_id': order.id,
            'name': self.promotion.name,
            'price_unit': -(order.amount_untaxed * eval(self.arguments) /
                            100),
            'product_uom_qty': 1,
            'promotion_line': True,
            'product_uom': PRODUCT_UOM_ID,
            'product_id': self.env.ref('commercial_rules.product_discount').id
        }
        self.create_line(args)
        return True

    def action_cart_disc_fix(self, order):
        """
        Fixed amount on Sub Total
        """
        if self.action_type == 'cart_disc_fix':
            args = {
                'order_id': order.id,
                'name': self.promotion.name,
                'price_unit': -eval(self.arguments),
                'product_uom_qty': 1,
                'promotion_line': True,
                'product_uom': PRODUCT_UOM_ID,
                'product_id': self.env.ref
                ('commercial_rules.product_discount').id
            }
            self.create_line(args)
            return True

    def create_y_line(self, order, quantity, product_id):
        """
        Create new order line for product
        """
        product_obj = self.env['product.product']
        product_y = product_obj.browse(product_id)
        vals = {
            'order_id': order.id,
            'product_id': product_y.id,
            'name': '[%s]%s (%s)' % (product_y.default_code,
                                     product_y.name,
                                     self.promotion.name),
            'price_unit': 0.00, 'promotion_line': True,
            'product_uom_qty': quantity,
            'product_uom': product_y.uom_id.id
        }
        self.create_line(vals)
        return True

    def action_prod_x_get_y(self, order):
        """
        Buy X get Y free
        """
        product_obj = self.env['product.product']

        prod_qty = {}
        # Get Product
        product_x_code, product_y_code = \
            [eval(code) for code in self.product_code.split(",")]
        product = product_obj.search([('default_code', '=',
                                      product_y_code)])
        if not product:
            raise UserError("No product with the code for Y")
        if len(product) > 1:
            raise UserError("Many products with same code")
        # get Quantity
        qty_x, qty_y = [eval(arg) for arg in self.arguments.split(",")]
        # Build a dictionary of product_code to quantity
        for order_line in order.order_line.\
                filtered(lambda l: not l.product_id.no_promo):
            if order_line.product_id:
                product_code = order_line.product_id.default_code
                prod_qty[product_code] = \
                    prod_qty.\
                    get(product_code, 0.00) + order_line.product_uom_qty
        # Total number of free units of y to give
        qty_y_in_cart = prod_qty.get(product_y_code, 0)
        # if product_x_code == product_y_code:
        #     diff_x_y = qty_y - qty_x
        # else:
        #     tot_free_y = int(qty_y_in_cart / qty_x) * qty_y
        qty_x_in_cart = prod_qty.get(product_x_code, 0)
        tot_free_y = 0
        if qty_x_in_cart and qty_x:
            factor = int(qty_x_in_cart / qty_x)
            tot_free_y = factor * qty_y

        if not tot_free_y:
            return True
        return self.create_y_line(order, tot_free_y, product.id)
    
    def action_buy_x_pay_y(self, order):
        """
        Buy X pay Y
        """
        product_obj = self.env['product.product']

        prod_qty = {}
        prod_lines = {}
        # Get Product
        product_code = eval(self.product_code)
        qty_x, qty_y = [eval(arg) for arg in self.arguments.split(",")]
        product = product_obj.search([('default_code', '=',
                                      product_code)])
        if not product:
            raise UserError("No product with the code for Y")
        if len(product) > 1:
            raise UserError("Many products with same code")
        # get Quantity
        # Build a dictionary of product_code to quantity
        for order_line in order.order_line.\
                filtered(lambda l: not l.product_id.no_promo):
            if order_line.product_id:
                product_code = order_line.product_id.default_code
                prod_qty[product_code] = \
                    prod_qty.\
                    get(product_code, 0.00) + order_line.product_uom_qty
                
                if product_code not in prod_lines:
                    prod_lines[product_code] = self.env['sale.order.line']
                prod_lines[product_code] += order_line

        qty_x_in_cart = prod_qty.get(product_code, 0)
        tot_free_y = 0
        if qty_x_in_cart and qty_x:
            factor = int(qty_x_in_cart / qty_x)
            tot_free_y = factor * qty_y

        if not tot_free_y:
            return True
        
        for l in prod_lines[product_code]:
            if l.product_uom_qty > tot_free_y:
                l.write({'product_uom_qty': l.product_uom_qty - tot_free_y})
                break
        return self.create_y_line(order, tot_free_y, product.id)
    
    def action_prod_free(self, order):
        """
        Action for: Get Product for free
        """
        product_obj = self.env['product.product']
        # Get Product
        product_code = eval(self.product_code)
        product = product_obj.search([('default_code', '=',
                                      product_code)])
        if not product:
            raise UserError(_("No product with the code % s") % product_code)
        
        qty = eval(self.arguments)

        return self.create_y_line(order, qty, product.id)

    # def action_line_prod_disc_perc(self, order):
    #     """
    #     Crea una nueva linea de cantidad 1 y precio_unitario el descuento
    #     sobre el subtotal del pedido
    #     """
    #     line_name = self.promotion.name

    #     prod_id = self.env.ref('commercial_rules.product_discount').id
    #     for order_line in order.order_line.\
    #             filtered(lambda l: not l.product_id.no_promo):
    #         if not self.product_code or \
    #                 order_line.product_id.code == eval(self.product_code):
    #             disc = eval(self.arguments)
    #             args = {
    #                 'order_id': order.id,
    #                 'name': line_name,
    #                 'price_unit': -(order.amount_untaxed * disc / 100),
    #                 'product_uom_qty': 1,
    #                 'promotion_line': True,
    #                 'product_uom': order_line.product_uom.id,
    #                 'product_id': prod_id,
    #                 'tax_id': [(6, 0, [x.id for x in order_line.tax_id])]
    #             }
    #             self.create_line(args)
    #         return True

    # def _create_lines_groped_by_price(self, order, selected_lines):
    #     """
    #     Crea lineas de descuento agrupandolas por precio, con decuento sobre
    #     precio unitario, y agrupándolas por cantidad.
    #     """
    #     group_dic = {}  # Agrupar lineas del mismo precio y producto
    #     prod_id = self.env.ref('commercial_rules.product_discount').id
    #     for line in selected_lines:
    #         key = line.price_unit
    #         if key not in group_dic:
    #             group_dic[key] = [0.0, []]
    #         group_dic[key][0] += line.product_uom_qty
    #         group_dic[key][1] += line

    #     line_name = self.promotion.name
    #     for price in group_dic:
    #         qty = group_dic[price][0]
    #         lines = group_dic[price][1]
    #         disc = eval(self.arguments)
    #         taxes = set()
    #         for l in lines:
    #             for t in l.tax_id:
    #                 taxes.add(t.id)
    #         taxes = list(set(taxes))
    #         args = {
    #             'order_id': order.id,
    #             'name': line_name,
    #             'price_unit': -(price * disc / 100),
    #             'product_uom_qty': qty,
    #             'promotion_line': True,
    #             'product_uom': lines[0].product_uom.id,
    #             'product_id': prod_id,
    #             'tax_id': [(6, 0, taxes)],
    #             'orig_line_ids': [(6, 0, [x.id for x in lines])]
    #         }
    #         self.create_line(args)
    #     return

    # def action_line_discount_group_price(self, order):
    #     """
    #     Crea una linea descuento con el descuento aplicado al precio unitario
    #     y la cantadid será la suma de las lineas implicadas. Se crea una linea
    #     descuento a mayores por cada linea implicada con un precio diferente
    #     """

    #     selected_lines = []
    #     restrict_codes = False
    #     if self.product_code:
    #         restrict_codes = self.product_code.replace("'", '').split(',')
    #     for line in order.order_line.\
    #             filtered(lambda l: not l.product_id.no_promo):
    #         if restrict_codes and line.product_id.code not in restrict_codes:
    #             continue
    #         selected_lines += line
    #     self._create_lines_groped_by_price(order, selected_lines)
    #     return

    # def action_line_discount_mult_pallet(self, order):
    #     """
    #     Crea una linea descuento por cada linea que cumpla que hay un número
    #     de pallets, múltiplo de 1.
    #     """
    #     selected_lines = []
    #     for line in order.order_line.\
    #             filtered(lambda l: not l.product_id.no_promo):
    #         packing = line.product_id.packaging_ids \
    #             and line.product_id.packaging_ids[0] or False
    #         num_pallets = 0.0
    #         if packing and packing.ul_type == 'pallet' and packing.qty:
    #             num_pallets = line.product_uom_qty / packing.qty
    #         if not num_pallets or num_pallets % 1 != 0:
    #             continue

    #         selected_lines += line
    #     self._create_lines_groped_by_price(order, selected_lines)
    #     return

    def execute(self, order):
        """
        Executes the action into the order
        """
        method_name = 'action_' + self.action_type
        return getattr(self, method_name).__call__(order)

    def validate(self, vals):
        """
        Validates if the values are coherent with
        attribute
        """
        if vals['action_type'] in ['prod_disc_perc', 'prod_disc_fix']:
            if not vals.get('product_code', False) or not \
                    type(eval(vals['product_code'])) == str:
                raise UserError("Invalid product code\n Has to be \
                                'product_code'")
            if not type(eval(vals['arguments'])) in [int, float]:
                raise UserError("Argument has to be numeric. eg: 10.00")

        if vals['action_type'] in ['cart_disc_perc', 'cart_disc_fix']:
            if vals['product_code']:
                raise UserError("Product code is not used in cart actions")
            if not type(eval(vals['arguments'])) in [int, float]:
                raise UserError("Argument has to be numeric. eg: 10.00")

        if vals['action_type'] in ['prod_x_get_y', ]:
            try:
                code_1, code_2 = vals['product_code'].split(",")
                assert (type(eval(code_1)) == str)
                assert (type(eval(code_2)) == str)
            except:
                raise UserError("Product codes have to be of form \
                                'product_x','product_y'")
            try:
                qty_1, qty_2 = vals['arguments'].split(',')
                assert (type(eval(qty_1)) in [int])
                assert (type(eval(qty_2)) in [int])
            except:
                raise UserError("Argument has to be qty of x,y eg.`1, 1`")

        return True

    @api.model
    def create(self, vals):
        """
        Validate before save
        """

        self.validate(vals)
        return super(PromotionsRulesActions, self).create(vals)

    def write(self, vals):
        """
        Validate before Write
        """
        old_vals = self.read(['action_type', 'product_code',
                              'arguments'])[0]
        old_vals.update(vals)
        'id' in old_vals and old_vals.pop('id')
        self.validate(old_vals)

        # only value may have changed and client gives only value
        vals = old_vals
        return super(PromotionsRulesActions, self).write(vals)
