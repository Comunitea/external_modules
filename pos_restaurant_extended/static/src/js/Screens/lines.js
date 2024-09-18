/** @odoo-module **/

import Registries from 'point_of_sale.Registries';
import { Order, Orderline } from 'point_of_sale.models';
import { _t } from 'web.core';
import { Gui } from 'point_of_sale.Gui';

const PosExtOrder= (Order) =>
    class extends Order {

    roundToNearestMultipleOfFive(number) {
        number = parseFloat(number);
        var decimals = number - Math.floor(number)
        var divider = 5;

        if ((decimals *100) % divider == 0) {
            return number;
        }
        if (Math.floor(decimals*100) % divider == 0) {
            return number;
        }
        return (divider - (decimals *100) % divider)/100 + number;
    }
    
    add_product(product, options) {
        if(this.pos.doNotAllowRefundAndSales() &&
        this._isRefundAndSaleOrder() &&
        
        (!options.quantity || options.quantity > 0)) {
            Gui.showPopup('ErrorPopup', {
                title: _t('Refund and Sales not allowed'),
                body: _t('It is not allowed to mix refunds and sales')
            });
            return;
        }

        var extra = 0;
        var floor_str = 0;
        if (this.tableId){
            var table = this.pos.tables_by_id[this.tableId]
            if(table && table.floor){
                floor_str = table.floor.id.toString();
            }
        }
        var facilities = JSON.parse(this.pos.config.floor_facility_ids);
        $.each(facilities, function (key, val) {
            if(val.floor_id == floor_str) {
                extra = parseFloat(val.line_percentage)
            }
        });

        if(this._printed){
            // when adding product with a barcode while being in receipt screen
            this.pos.removeOrder(this);
            return this.pos.add_new_order().add_product(product, options);
        }
        this.assert_editable();
        options = options || {};
        var line = Orderline.create({}, {pos: this.pos, order: this, product: product});
        this.fix_tax_included_price(line);

        this.set_orderline_options(line, options);

        var to_merge_orderline;
        /* We want to add products always as new lines */
        // for (var i = 0; i < this.orderlines.length; i++) {
        //     if(this.orderlines.at(i).can_be_merged_with(line) && options.merge !== false){
        //         to_merge_orderline = this.orderlines.at(i);
        //     }
        // }
        if (to_merge_orderline){
            to_merge_orderline.merge(line);
            this.select_orderline(to_merge_orderline);
        } else {
            this.add_orderline(line);
            this.select_orderline(this.get_last_orderline());
        }

        if (options.draftPackLotLines) {
            this.selected_orderline.setPackLotLines({ ...options.draftPackLotLines, setQuantity: options.quantity === undefined });
        }

        var line_categ = line.product.pos_categ_id[0];
        var allow_categs = this.pos.config.service_level_categories;

        // REVISAR
        // if (allow_categs.includes(line_categ) && this.pos.config.service_level_default) {
        //     line.show_service_popup();
        // }

    }
    // REVISAR
    get_last_requested_service() {
        var last_requested_service = this.last_requested_service;
        return last_requested_service;
    }
    // REVISAR
    set_last_requested_service(value) {
        this.last_requested_service = value;
        // this.trigger('change', this);
    }
    
    set_pos_printed(value){
        this.pos_printed = value;
        // this.trigger('change', this);
    }

    export_as_JSON() {
        var json = super.export_as_JSON();
        json.pos_printed = this.pos_printed;
        json.last_requested_service = this.last_requested_service;
        return json;
    }
    
    init_from_JSON(json) {
        super.init_from_JSON(json);
        this.pos_printed = json.pos_printed;
        this.last_requested_service = json.last_requested_service;
    }
    
    // REVISAR
    has_only_cash_payment(){
        var has_only_cash = true;
        this.paymentlines.models.each(function(paymentline){
            if(!paymentline.payment_method.is_cash_count){
                has_only_cash = false;
            }
        });
        return has_only_cash;
    }

};

Registries.Model.extend('Order', PosExtOrder);

const PosExtOrderline = (Orderline) =>
    class extends Orderline {

        constructor(obj, options) {
            super(obj, options);
            var line_length = 0;
            this.position = this.position || 0;
        }

        // PROBABLEMENTE NO SE USE
        // can_be_merged_with: function(orderline){
        //     var extra = 0
        //     var floor_str = "0"
        //     if (this.order.table) {
        //         if (this.order.table.floor) {
        //             floor_str = this.order.table.floor.id.toString()
        //         }
        //     }

        //     var facilities = JSON.parse(this.pos.config.floor_facility_ids);

        //     $.each(facilities, function (key, val) {
        //         if(val.floor_id == floor_str) {
        //             extra = parseFloat(val.line_percentage)
        //         }
        //     });

        //     var price = parseFloat(round_di(this.price || 0, this.pos.dp['Product Price']).toFixed(this.pos.dp['Product Price']));
        //     var order_line_price = orderline.get_product().get_price(orderline.order.pricelist, this.get_quantity());
        //     order_line_price = orderline.compute_fixed_price(order_line_price);
        //     if( this.get_product().id !== orderline.get_product().id){    //only orderline of the same product can be merged
        //         return false;
        //     }else if(!this.get_unit() || !this.get_unit().is_pos_groupable){
        //         return false;
        //     }else if(this.get_discount() > 0){             // we don't merge discounted orderlines
        //         return false;
        //     }else if(!utils.float_is_zero(price - orderline.compute_fixed_price(orderline.get_product().get_price(orderline.order.pricelist, this.get_quantity()) * (1 + (extra/100))) - orderline.get_price_extra(), this.pos.currency.decimals)) {
        //         return false;
        //     }else if(this.product.tracking == 'lot' && (this.pos.picking_type.use_create_lots || this.pos.picking_type.use_existing_lots)) {
        //         return false;
        //     }else if (this.description !== orderline.description) {
        //         return false;
        //     }else{
        //         return true;
        //     }
        // },

        set_quantity(quantity, keep_price){
            if (!this.price_manually_set) {
                this.price_manually_set = true;
            }
            var res = super.set_quantity(quantity, keep_price);
            var extra = 0;
            var floor_str = 0;
            var tableId = this.order.tableId;
            if (tableId){
                var table = this.pos.tables_by_id[tableId]
                if(table && table.floor){
                    floor_str = table.floor.id.toString();
                }
            }
            var facilities = JSON.parse(this.pos.config.floor_facility_ids);
            $.each(facilities, function (key, val) {
                if(val.floor_id == floor_str) {
                    extra = parseFloat(val.line_percentage)
                }
            });
            // just like in sale.order changing the quantity will recompute the unit price
            if(! keep_price && ! (this.price_manually_set || this.price_automatically_set)){
                this.set_unit_price(this.product.get_price(this.order.pricelist, this.get_quantity(), this.get_price_extra()));
                this.order.fix_tax_included_price(this);
            }
            return res;
        }
        get_position(){
            return this.position;
        }
        set_position(value){
            this.position = value;
        }
        export_as_JSON() {
            var json = super.export_as_JSON();
            json.position = this.position;
            return json;
        }
        init_from_JSON(json) {
            super.init_from_JSON(json);
            this.position = json.position;
        }
        // REVISAR PROBABLEMENTE NO SE USE
        // apply_ms_data(data){
        //     if (typeof data.position !== 'undefined') {
        //         this.set_position(data.position);
        //     }
        // }

        // REVISAR
        // async show_service_popup(){
        //     var service_level = this.pos.config.service_level;
        //     var list = [];
        //     for (var n = 1; n <= service_level; n++) {
        //         list.push({ label: '#' + n,  item: n, id: n });
        //     }
        //     const { confirmed, payload: selectedService } = await Gui.showPopup(
        //         'SelectionPopup',
        //         {
        //             title: _t('Order'),
        //             list: list,
        //         }
        //     );
        //     if (confirmed) {
        //         this.set_position(parseInt(selectedService));
        //     }
        // }

        
    }

    Registries.Model.extend('Orderline', PosExtOrderline);