/* Copyright 2018 Tecnativa - David Vidal
   License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define('commercial_rules_pos.models', function (require) {
    'use strict';

    var models = require('point_of_sale.models');

    // Loading commercial rules
    models.load_models({
        model: 'promos.rules',
        fields: ['name', 'expressions', 'actions', 'stop_further', 'from_date', 'to_date', 'logic', 'expected_logic_result', 'partner_categories', 'partner_ids'],
        loaded: function(self, rules){
            self.rules_by_id = {};

            _.each(rules, function(rule){
                rule.condition_objs = [];
                rule.action_objs = [];
                self.rules_by_id[rule.id] = rule
            });
        },
    });

     // Loading expressions
     models.load_models({
        model: 'promos.rules.conditions.exps',
        fields: ['sequence', 'attribute', 'comparator', 'value', 'serialised_expr', 'promotion', 'stop_further', 'serialised_pos'],
        loaded: function(self, conditions){
            self.conditions_by_id = {};

            _.each(conditions, function(cond){
                self.conditions_by_id[cond.id] = cond
                var rule = self.rules_by_id[cond.promotion[0]];
                rule.condition_objs.push(cond)
            });
        },
    });

    // Loading actions
    models.load_models({
        model: 'promos.rules.actions',
        fields: ['sequence', 'action_type', 'product_code', 'arguments', 'promotion'],
        loaded: function(self, actions){
            self.actions_by_id = {};

            _.each(actions, function(act){
                self.actions_by_id[act.id] = act
                var rule = self.rules_by_id[act.promotion[0]];
                rule.action_objs.push(act)
            });
        },
    });


    var _order_super = models.Order.prototype;
    models.Order = models.Order.extend({
        is_rule_applicable: function(rule){
            // TODO Mirar fechas, mirar categorías, mirar rango fecha
            console.log("*****is_rule_applicable*******")
            return true;
        },
        check_primary_conditions: function(rule){
            //  Comprobar condiciones, quizá tengo que devolver algo para que
            // se interrumpa la ejecución
            console.log("*****check_primary_conditions*******")
            return true;
        },
        evaluate_condition: function(condition){
            console.log("*****evaluate_condition*******")
            var products = [];
            var prod_qty = {};
            var prod_pallet = {};
            var prod_unit_price = {};
            var prod_sub_total = {};
            var prod_discount = {};
            var prod_weight = {};
            var prod_lines = {};

            var lines = this.get_orderlines();
            var line;
            var product_code;
            for (var i = 0; i < lines.length; i++) {
                line = lines[i]
                // TODO añadir no_promo al producto
                // if (! line.get_product().no_promo) {
                //     continue
                // }

                // TODO, el original usa el campo code
                product_code = line.get_product().default_code;
                products.push(product_code);;
                prod_lines[product_code] = line.get_product();

                if (!(product_code in prod_qty))
                    prod_qty[product_code] = 0.00;
                prod_qty[product_code] += line.get_quantity();

                if (!(product_code in prod_unit_price))
                    prod_unit_price[product_code] = 0.00;
                prod_unit_price[product_code] += line.get_unit_price();

                if (!(product_code in prod_sub_total))
                    prod_sub_total[product_code] = 0.00;
                prod_sub_total[product_code] += line.get_base_price();

                if (!(product_code in prod_discount))
                    prod_discount[product_code] = 0.00;
                prod_discount[product_code] += line.get_discount();

                // TODO: Traerse peso
                // if (!product_code in prod_weight)
                //     prod_weight[product_code] = 0.00;
                // prod_weight[product_code] += line.get_weight();

                // TODO Pallets
            }
            return eval(condition.serialised_pos);
        },
        evaluate_rule: function(rule){
            // Lógica condiciones
            console.log("*****evaluate_rule*******")
            var validated = this.check_primary_conditions(rule)

            var expected_result = (rule.expected_logic_result == 'True') ? true : false;
            var logic = rule.logic
            if (!validated)
                return false;
            
            var condition, result;
            for (var i = 0; i < rule.condition_objs.length; i++) {
                condition = rule.condition_objs[i];
                result = this.evaluate_condition(condition);

                if ( !(result == expected_result) && (logic == 'and') ){
                    return false
                }
                if ( (result == expected_result) && (logic == 'or') ){
                    return true
                }
                if ( !(result == expected_result) && (expression.stop_further) ){
                    return true
                }
            }
            if (logic == 'and')
                return true
            else
                return false
            return true;
        },
        execute_actions: function(rule){
            for (var i = 0; i < rule.action_objs.length; i++) {
                var action = rule.action_objs[i];
                
                var fn = eval('this.action_' + action.action_type)
                if (fn)
                    fn.call(this, action)
            }
        },
        clear_existing_promotion_lines: function(){
            var lines = this.get_orderlines();
            var line;
            for (var i = 0; i < lines.length; i++) {
                line = lines[i]
                if (line.promotion_line)
                    this.remove_orderline(line)
                if (line.old_discount)
                    line.set_discount(line.old_discount)
            }
        },
        apply_commercial_rules: function(){
            this.clear_existing_promotion_lines()
           
            var no_promo_applied = true;
            for (var rule_id in this.pos.rules_by_id){
                var rule = this.pos.rules_by_id[rule_id];
                console.log(rule)

                if ( !this.is_rule_applicable(rule) ) 
                    continue;
                
                var result = this.evaluate_rule(rule)

                if (result) {
                    this.execute_actions(rule);
                    no_promo_applied = false;

                    if (rule.stop_further)
                        break;
                }
            }
            if (no_promo_applied){
                alert("No promotion founded to apply.")
            }
        },
        // ********************************************************************
        // ************************ ACTION METHODS ****************************
        // ********************************************************************
        action_prod_disc_perc: function(action){
            // Action for: 'Discount % on Product'
            var lines = this.get_orderlines();
            var code = eval(action.product_code);
            var discount = eval(action.arguments);
            var line;
            var product;
            var old_discount;
            for (var i = 0; i < lines.length; i++) {
                line = lines[i]
                product = line.get_product();
                // TODO añadir no_promo al producto
                // if (! product.no_promo) {
                //     continue
                // }
                if (product.default_code == code){
                    var old_discount = line.discount
                    line.set_discount(discount)
                    line.old_discount = old_discount
                }

            }
        },
        action_prod_disc_fix: function(action){
            // Action for: Fixed amount on Product
            console.log('action_prod_free')
            var product_code = eval(action.product_code)
            var products = this.pos.db.search_product_in_category(0, product_code)

            if (products.length > 0){
                var price = eval(action.arguments)
                this.add_product(products[0], {
                    price: -price,
                    quantity: 1,
                    discount: 0.00,
                    merge: false,
                    extras: {promotion_line: true}
                });
            }
        },
        action_cart_disc_perc: function(action){
            // Action for 'Discount % on subtotal'
            console.log('#########action_cart_disc_perc#########');
            var products = this.pos.db.search_product_in_category(0, 'Discount')

            if (products.length > 0){
                var disc_product = products[0]
                var price = (this.get_subtotal() * (eval(action.arguments) / 100))
                this.add_product(disc_product, {
                    price: -price,
                    quantity: 1,
                    discount: 0.00,
                    merge: false,
                    extras: {promotion_line: true}
            });
            console.log(this.get_last_orderline());
            }
            
        },
        action_cart_disc_fix: function(action){
            // Action fort 'Fixed amount on Sub Total'
            var products = this.pos.db.search_product_in_category(0, 'Discount')

            if (products.length > 0){
                var disc_product = products[0]
                var price = eval(action.arguments)
                this.add_product(disc_product, {
                    price: -price,
                    quantity: 1,
                    discount: 0.00,
                    merge: false,
                    extras: {promotion_line: true}
            });
            console.log(this.get_last_orderline());
            }
        },
        action_prod_x_get_y: function(action){
            var lines = this.get_orderlines();
            var line;
            var product_code;
            var prod_qty = {};
            for (var i = 0; i < lines.length; i++) {
                line = lines[i]
                // TODO añadir no_promo al producto
                // if (! line.get_product().no_promo) {
                //     continue
                // }
                // TODO, el original usa el campo code
                product_code = line.get_product().default_code;
                if (!(product_code in prod_qty))
                    prod_qty[product_code] = 0.00;
                prod_qty[product_code] += line.get_quantity();
            }
            var product_x_code = eval(action.product_code.split(',')[0])
            var product_y_code = eval(action.product_code.split(',')[1])

            var products = this.pos.db.search_product_in_category(0, product_y_code)
            var product = false
            if (products.length > 0)
                var product = products[0]
            
            if (!product)
                return false;
            var qty_x = eval(action.arguments.split(',')[0])
            var qty_y = eval(action.arguments.split(',')[1])

            if (product_x_code in prod_qty){
                var qty_x_in_cart = prod_qty[product_x_code];
                var tot_free_y = 0;
                if (qty_x_in_cart > 0 && qty_x > 0){
                    var factor = Math.floor((qty_x_in_cart / qty_x))
                    tot_free_y = factor * qty_y
                }
                if (tot_free_y){
                    this.add_product(product, {
                        price: 0.00,
                        quantity: tot_free_y,
                        discount: 0.00,
                        merge: false,
                        extras: {promotion_line: true}
                    });
                }
            }
        },
        action_buy_x_pay_y: function(action){
            var lines = this.get_orderlines();
            var line;
            var product_code;
            var prod_qty = {};
            var prod_lines = {};
            for (var i = 0; i < lines.length; i++) {
                line = lines[i]
                // TODO añadir no_promo al producto
                // if (! line.get_product().no_promo) {
                //     continue
                // }
                // TODO, el original usa el campo code
                product_code = line.get_product().default_code;
                if (!(product_code in prod_qty))
                    prod_qty[product_code] = 0.00;
                prod_qty[product_code] += line.get_quantity();

                if (!(product_code in prod_lines))
                    prod_lines[product_code] = [];
                prod_lines[product_code].push(line);
            }
            var product_code = eval(action.product_code)

            var products = this.pos.db.search_product_in_category(0, product_code)
            var product = false
            if (products.length > 0)
                var product = products[0]
            
            if (!product)
                return false;
            var qty_x = eval(action.arguments.split(',')[0])
            var qty_y = eval(action.arguments.split(',')[1])

            if (product_code in prod_qty){
                var qty_x_in_cart = prod_qty[product_code];
                var tot_free_y = 0;
                if (qty_x_in_cart > 0 && qty_x > 0){
                    var factor = Math.floor((qty_x_in_cart / qty_x))
                    tot_free_y = factor * qty_y
                }
                if (tot_free_y){
                    this.add_product(product, {
                        price: 0.00,
                        quantity: tot_free_y,
                        discount: 0.00,
                        merge: false,
                        extras: {promotion_line: true}
                    });
                
                    for (var i = 0; i < prod_lines[product_code].length; i++) {
                        line = prod_lines[product_code][i]
                        if (line.get_quantity() > tot_free_y)
                            line.set_quantity( (line.get_quantity() - tot_free_y) )
                    }
                    
                }
            }
        },
        action_prod_free: function(action){
            // Action for: Get Product for free
            console.log('action_prod_free')
            var product_code = eval(action.product_code)
            var products = this.pos.db.search_product_in_category(0, product_code)

            if (products.length > 0){
                var qty = eval(action.arguments)
                this.add_product(products[0], {
                    price: 0.00,
                    quantity: qty,
                    discount: 0.00,
                    merge: false,
                    extras: {promotion_line: true}
                });
            }
        },
    });
   
});
