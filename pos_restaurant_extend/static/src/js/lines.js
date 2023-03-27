odoo.define('pos_restaurant_extend.lines', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    /* var screens = require('point_of_sale.screens'); */
    var utils = require('web.utils');
    var round_di = utils.round_decimals;
    var core = require('web.core');
    const { Gui } = require('point_of_sale.Gui');
    var QWeb = core.qweb;

    var _t   = core._t;

    var _super_order = models.Order.prototype;

    models.Order = models.Order.extend({
        initialize: function(attr, options) {
            _super_order.initialize.apply(this,arguments);
        },

        roundToNearestMultipleOfFive: function(number) {
            number = parseFloat(number);
            var decimals = number - Math.floor(number)
            var divider = 5;

            if ((decimals *100) % divider == 0) {
                return number;
            } else {
                if (Math.floor(decimals*100) % divider == 0) {
                    return number;
                }
                return (divider - (decimals *100) % divider)/100 + number;
            }
        },

        /* Overwritten because the function has no return */

        add_product: function(product, options){
            var extra = 0
            var floor_str = "0"
            if (this.table) {
                if (this.table.floor) {
                    floor_str = this.table.floor.id.toString()
                }
            }

            var facilities = JSON.parse(this.pos.config.floor_facility_ids);

            $.each(facilities, function (key, val) {
                if(val.floor_id == floor_str) {
                    extra = parseFloat(val.line_percentage)
                }
            });

            if(this._printed){
                this.destroy();
                return this.pos.get_order().add_product(product, options);
            }
            this.assert_editable();
            options = options || {};
            var line = new models.Orderline({}, {pos: this.pos, order: this, product: product});
            this.fix_tax_included_price(line);

            if(options.quantity !== undefined){
                line.set_quantity(options.quantity);
            }

            if (options.price_extra !== undefined){
                line.price_extra = options.price_extra;
                var new_price = line.product.get_price(this.pricelist, line.get_quantity(), options.price_extra) * (1 + (extra/100));
                if (extra != 0) {
                    new_price = this.roundToNearestMultipleOfFive(new_price);
                }
                line.set_unit_price(new_price);
                this.fix_tax_included_price(line);
            }

            if(options.price !== undefined){
                line.set_unit_price(options.price * (1 + (extra/100)));
                this.fix_tax_included_price(line);
            }

            if(options.lst_price !== undefined){
                line.set_lst_price(options.lst_price);
            }

            if(options.discount !== undefined){
                line.set_discount(options.discount);
            }

            if (options.description !== undefined){
                line.description += options.description;
            }

            if(options.extras !== undefined){
                for (var prop in options.extras) {
                    line[prop] = options.extras[prop];
                }
            }
            if (options.is_tip) {
                this.is_tipped = true;
                this.tip_amount = options.price;
            }

            var to_merge_orderline;
            /* We want to add products always as new lines */
            /* for (var i = 0; i < this.orderlines.length; i++) {
                if(this.orderlines.at(i).can_be_merged_with(line) && options.merge !== false){
                    to_merge_orderline = this.orderlines.at(i);
                }
            } */
            if (to_merge_orderline){
                to_merge_orderline.merge(line);
                this.select_orderline(to_merge_orderline);
            } else {
                this.orderlines.add(line);
                this.select_orderline(this.get_last_orderline());
            }

            if (options.draftPackLotLines) {
                this.selected_orderline.setPackLotLines(options.draftPackLotLines);
            }
            if (this.pos.config.iface_customer_facing_display) {
                this.pos.send_current_order_to_customer_facing_display();
            }

            var line_categ = line.product.pos_categ_id[0];
            var allow_categs = this.pos.config.service_level_categories;

            if (allow_categs.includes(line_categ) && this.pos.config.service_level_default) {
                line.show_service_popup();
            }
        },

        get_last_requested_service: function() {
            var last_requested_service = this.last_requested_service;
            return last_requested_service;
        },

        set_last_requested_service: function(value) {
            this.last_requested_service = value;
            this.trigger('change', this);
        },

        get_pos_printed: function() {
            var pos_printed = this.pos_printed;
            return pos_printed;
        },

        set_pos_printed: function(value) {
            this.pos_printed = value;
            this.trigger('change', this);
        },

        export_as_JSON: function() {
            var json = _super_order.export_as_JSON.apply(this,arguments);
            json.pos_printed = this.pos_printed;
            json.last_requested_service = this.last_requested_service;
            return json;
        },

        init_from_JSON: function(json) {
            _super_order.init_from_JSON.apply(this,arguments);
            this.pos_printed = json.pos_printed;
            this.last_requested_service = json.last_requested_service || 0;
        },

        has_only_cash_payment: function() {
            var has_only_cash_payment = true;
            if (this.paymentlines.models.length == 1 && this.paymentlines.models[0].payment_method.is_cash_count) {
                return true;
            } else {
                _.each(this.paymentlines.models, function (val, key) {
                    if(!val.payment_method.is_cash_count) {
                        has_only_cash_payment = false;
                    }
                });
                return has_only_cash_payment;
            }
        },

    })

    var _super_orderline = models.Orderline.prototype;

    models.Orderline = models.Orderline.extend({

        initialize: function(attr, options) {
            _super_orderline.initialize.call(this,attr,options);
            var line_length = 0;
            this.position = this.position || line_length;
        },

        /* Overwritten to add the extra cost */
        can_be_merged_with: function(orderline){
            var extra = 0
            var floor_str = "0"
            if (this.order.table) {
                if (this.order.table.floor) {
                    floor_str = this.order.table.floor.id.toString()
                }
            }

            var facilities = JSON.parse(this.pos.config.floor_facility_ids);

            $.each(facilities, function (key, val) {
                if(val.floor_id == floor_str) {
                    extra = parseFloat(val.line_percentage)
                }
            });

            var price = parseFloat(round_di(this.price || 0, this.pos.dp['Product Price']).toFixed(this.pos.dp['Product Price']));
            var order_line_price = orderline.get_product().get_price(orderline.order.pricelist, this.get_quantity());
            order_line_price = orderline.compute_fixed_price(order_line_price);
            if( this.get_product().id !== orderline.get_product().id){    //only orderline of the same product can be merged
                return false;
            }else if(!this.get_unit() || !this.get_unit().is_pos_groupable){
                return false;
            }else if(this.get_discount() > 0){             // we don't merge discounted orderlines
                return false;
            }else if(!utils.float_is_zero(price - orderline.compute_fixed_price(orderline.get_product().get_price(orderline.order.pricelist, this.get_quantity()) * (1 + (extra/100))) - orderline.get_price_extra(), this.pos.currency.decimals)) {
                return false;
            }else if(this.product.tracking == 'lot' && (this.pos.picking_type.use_create_lots || this.pos.picking_type.use_existing_lots)) {
                return false;
            }else if (this.description !== orderline.description) {
                return false;
            }else{
                return true;
            }
        },

        set_quantity: function(quantity, keep_price) {
            if (!this.price_manually_set) {
                this.price_manually_set = true;
            }
            _super_orderline.set_quantity.apply(this, arguments);
            var extra = 0
            var floor_str = "0"
            if (this.order.table) {
                if (this.order.table.floor) {
                    floor_str = this.order.table.floor.id.toString()
                }
            }

            var facilities = JSON.parse(this.pos.config.floor_facility_ids);

            $.each(facilities, function (key, val) {
                if(val.floor_id == floor_str) {
                    extra = parseFloat(val.line_percentage)
                }
            });

            if (!keep_price && !this.price_manually_set){
                this.set_unit_price(this.product.get_price(this.order.pricelist, this.get_quantity()) * (1 + (extra/100)));
                this.order.fix_tax_included_price(this);
            }
            this.trigger('change', this);
        },

        get_position: function() {
            var position = this.position;
            return position;
        },

        set_position: function(value) {
            this.position = value;
            this.trigger('change', this);
        },

        export_as_JSON: function() {
            var json = _super_orderline.export_as_JSON.apply(this,arguments);
            json.position = this.position;
            return json;
        },

        init_from_JSON: function(json) {
            _super_orderline.init_from_JSON.apply(this,arguments);
            this.position = json.position;
        },

        apply_ms_data: function(data) {
            if (typeof data.position !== "undefined") {
                this.set_position(data.position);
            }
            this.trigger('change', this);
        },

        show_service_popup: async function() {
            var service_level = this.pos.config.service_level;
            var list = [];
            for (var n = 1; n <= service_level; n++) {
                list.push({ label: '#' + n,  item: n, id: n });
            }

            const { confirmed, payload: selectedService } = await Gui.showPopup(
                'SelectionPopup',
                {
                    title: _t('Order'),
                    list: list,
                }
            );
            if (confirmed) {
                this.set_position(parseInt(selectedService));
            }
        },

    });

});
