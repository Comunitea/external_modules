odoo.define('telesale.models', function (require) {
"use strict";

var Backbone = window.Backbone;
var Model = require('web.DataModel');
var core = require('web.core');
var _t = core._t;

var exports = {};

exports.TsModel = Backbone.Model.extend({
    initialize: function(session, attributes) {
        Backbone.Model.prototype.initialize.call(this, attributes);
        var  self = this;
        this.session = session;  // openerp session
        this.ready = $.Deferred(); // used to notify the GUI that the PosModel has loaded all resources
        this.ts_widget = attributes.ts_widget;
        this.set({
            'currency': {symbol: $, position: 'after'},
            'shop':                 null,
            'user':                 null,
            'company':              null,
            'orders':               new exports.OrderCollection(),
            // 'products':             new exports.ProductCollection(),
            // 'sold_lines':           new exports.SoldLinesCollection(),
            'product_search_string': "",
            'products_names':            [], // Array of products names
            'products_codes':            [], // Array of products code
            'sust_products':            [], // Array of products sustitutes
            'taxes':                null,
            'ts_session':           null,
            'ts_config':            null,
            'units':                [], // Array of units
            'units_names':          [], // Array of units names
          
            'customer_names':          [], // Array of customer names
            'customer_codes':          [], // Array of customer refs
            'supplier_names':          [], // Array of supplier refs
            'pricelist':            null,
            'selectedOrder':        null,
            'nbr_pending_operations': 0,
            'visible_products': {},
            'call_id': false,
            'update_catalog': 'a',  //value to detect changes between a and b to update the catalog only when click in label
            'bo_id': 0 //it's a counter to assign to the buttons when you do click on '+'
        });
        $.when(this.load_server_data())
            .done(function(){
                self.ready.resolve();

            }).fail(function(){
                self.ready.reject();
            });
    },
    // helper function to load data from the server
    fetch: function(model, fields, domain, ctx){
        this._load_progress = (this._load_progress || 0) + 0.05;
        this.ts_widget.loading_message(_t('Loading')+' '+model,this._load_progress);
        return new Model(model).query(fields).filter(domain).context(ctx).all()
    },
    load_server_data: function(){
        var self=this;

        var loaded = self.fetch('res.users',['name','company_id'],[['id', '=', this.session.uid]])
            .then(function(users){
                self.set('user',users[0]);
                console.time('Test performance company');
                return self.fetch('res.company',
                [
                    'currency_id',
                    'email',
                    'website',
                    'company_registry',
                    'vat',
                    'name',
                    'phone',
                    'partner_id',
                    'min_limit',
                    'min_margin',
                ],
                [['id','=',users[0].company_id[0]]]);
                })
        return loaded;
    }
});

//**************************** PRODUCTS AND PRODUCT COLLECTION****************************************************
exports.Product = Backbone.Model.extend({
});

exports.ProductCollection = Backbone.Collection.extend({
    model: exports.Product,
});

// **************************** ORDER LINE AND ORDER LINE COLLECTION***********************************************
exports.Orderline = Backbone.Model.extend({
    defaults: {
        n_line: '',
        code: '',
        product: '',
        unit: '',
        qnote: '',
        detail: '',
        qty: 1,
        pvp: 0,
        pvp_ref: 0, //in order to change the discount
        total: 0,
        product_uos: '',
        product_uos_qty: 0,
        price_uos_qty: 0,
        price_udv: 0,
        //to calc totals
        discount: 0,
        specific_discount: 0,
        weight: 0,
        margin: 0,
        taxes_ids: [],
        temperature: 0,
        tourism: false,
    },
    initialize: function(options){
        this.ts_model = options.ts_model;
        this.order = options.order;

        this.selected = false;
    },

    set_selected: function(selected){
        this.selected = selected;
    },
    is_selected: function(){
        return this.selected;
    },
    check: function(){
        var res = true
        if ( this.get('product') == "" ) {
           res = false;
        }
        return res
    },
    get_product: function(){
        var product_obj = false
        if (this.check()){
            var product_name = this.get('product');
            var product_id = this.ts_model.db.product_name_id[product_name];
            var product_obj = this.ts_model.db.product_by_id[product_id]
        }
        return product_obj;
    },
    export_as_JSON: function() {
        var product_id = this.ts_model.db.product_name_id[this.get('product')];
        var uom_id = this.ts_model.db.unit_name_id[this.get('unit')];
        var uos_id = this.ts_model.db.unit_name_id[this.get('product_uos')];
        var qnote_id = this.ts_model.db.qnote_name_id[this.get('qnote')];
        return {
            qty: this.get('qty'),
            product_uom: uom_id,
            product_uos_qty: this.get('product_uos_qty'),
            product_uos: uos_id,
            price_unit: this.get('pvp'),
            price_udv: this.get('price_udv'),
            product_id:  product_id,
            qnote: qnote_id,
            tax_ids: this.get('taxes_ids'),
            pvp_ref: this.get('pvp_ref'),
            detail_note: this.get('detail') || "",
            discount: this.get('discount') || 0.0,
            tourism: this.get('tourism') || false
        };
    },
    get_price_without_tax: function(){
        return this.get_all_prices().priceWithoutTax;
    },
    get_price_with_tax: function(){
        return this.get_all_prices().priceWithTax;
    },
    get_tax: function(){
        return this.get_all_prices().tax;
    },
    get_all_prices: function(){
        var self = this;
        // var base = round_dc(this.get('qty') * this.get('pvp') * (1 - (this.get('discount') / 100.0)), 2);
        var base = this.get('qty') * this.get('pvp') * (1 - (this.get('discount') / 100.0));
        var totalTax = base;
        var totalNoTax = base;
        var taxtotal = 0;
        var product =  this.get_product();

        if (product){

            var taxes_ids = self.get('taxes_ids')
            var taxes =  self.ts_model.get('taxes');
            var tmp;
                // var taxtotal;
                // var totalTax;
            _.each(taxes_ids, function(el) {
                var tax = _.detect(taxes, function(t) {return t.id === el;});

                if (tax.price_include) {
                    if (tax.type === "percent") {
                        tmp =  base - base / (1 + tax.amount);
                    } else if (tax.type === "fixed") {
                        tmp = tax.amount * self.get('qty');
                    } else {
                        throw "This type of tax is not supported by the telesale system: " + tax.type;
                    }
                    // tmp = round_dc(tmp,2);
                    taxtotal += tmp;
                    totalNoTax -= tmp;
                } else {
                    if (tax.type === "percent") {
                        tmp = tax.amount * base;
                    } else if (tax.type === "fixed") {
                        tmp = tax.amount * self.get('qty');
                    } else {
                        throw "This type of tax is not supported by the telesale system: " + tax.type;
                    }
                    // tmp = round_dc(tmp,2);
                    taxtotal += tmp;
                    totalTax += tmp;
                }
            });
        }
        return {
            "priceWithTax": my_round(totalTax,2),
            "priceWithoutTax": my_round(totalNoTax,2),
            "tax": my_round(taxtotal,2),
        };
    },
    // update_pvp: function(){
    //     // No se tiene en cuenta descuento
    //     var self = this;
    //     var customer_id = this.ts_model.db.partner_name_id[this.order.get('partner')];
    //     var pricelist_id = (this.ts_model.db.get_partner_by_id(customer_id)).property_product_pricelist;
    //     var model = new instance.web.Model("product.pricelist");
    //     var product_id = this.ts_model.db.product_name_id[this.get('product')];
    //     var loaded = model.call("ts_get_product_pvp",[product_id,pricelist_id])
    //     .then(function(result){
    //         if (result[0])
    //             self.set('pvp', result[0])
    //             self.set('total', my_round(self.get('qty') * result[0]),2);
    //     })
    //     return loaded;
    // }

});
exports.OrderlineCollection = Backbone.Collection.extend({
    model: exports.Orderline,
});


// **************************** ORDER AND ORDER COLLECTION***********************************************
var counter = 0;
exports.Order = Backbone.Model.extend({
    initialize: function(attributes){
        Backbone.Model.prototype.initialize.apply(this, arguments);
        this.set({
            creationDate:   new Date(),
            orderLines:     new exports.OrderlineCollection(),
            name:           this.generateUniqueId(),
            //order #toppart values
            num_order: this.generateNumOrder(),
            partner_code: '',
            partner: '',
            supplier: '',
            customer_comment: '',
            client_order_ref: '',
            contact_name: '',
            date_order: this.getStrDate(),
            date_invoice: this.getStrDatePlanned(),
            date_planned: this.getStrDatePlanned(),
            limit_credit: (0),
            customer_debt: (0),
            //order #bottompart values
            total_boxes: (0),
            total_weight: (0),
            total_discount: (0),
            total_discount_per: (0).toFixed(2)+" %",
            total_margin_per: (0).toFixed(2)+" %",
            total: (0),
            total_base: (0),
            total_iva: (0),
            total_margin: (0),
            total_fresh: (0),
            selected_line: null,
            //to pas the button action to the server
            action_button: null,
            //to check save confirm cancel butons
            erp_id: false,
            erp_state: false,
            state:"draft",
            comercial: '',
            coment: '',
            set_promotion: false // if true in the server we create a promotion, and recover again the order
        });

        this.ts_model =     attributes.ts_model;
        this.selected_orderline = undefined;
        this.screen_data = {};  // see ScreenSelector
        return this;
    },
    generateNumOrder: function(){
        counter += 1;
        return "TStmp"+counter

    },
    getStrDate: function() {
        var date = new Date();
        var day = date.getDate();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        if (month < 10) month = "0" + month;
        if (day < 10) day = "0" + day;

        var today = year + "-" + month + "-" + day;
        return today;
    },
     getStrDatePlanned: function() {
        var date = new Date();
        var day = date.getDate();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        if (month < 10) month = "0" + month;
        if (day < 10) day = "0" + day;

        var today = year + "-" + month + "-" + day;
        return today;
    },
    dateToStr: function(date) {
        var day = date.getDate();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        if (month < 10) month = "0" + month;
        if (day < 10) day = "0" + day;

        var today = year + "-" + month + "-" + day;
        return today;
    },
    generateUniqueId: function() {
        return new Date().getTime();
    },
    addLine: function() {
        var line = new exports.Orderline({ts_model: this.ts_model, order:this})
        this.get('orderLines').add(line);
        return line
    },
    getSelectedLine: function(){
        var order_lines = this.get('orderLines').models;
        var res = false
        for (key in order_lines){
            var line = order_lines[key];
            if (line.is_selected())
                res = line;
        }
        return res
    },
    removeLine: function(){
        var index = 0;
        (this.get('orderLines')).each(_.bind( function(item) {
            if ( item.is_selected() ){
                this.get('orderLines').remove(item)
                index = item.get('n_line') - 1;
            }
        }, this));
        if ( !$.isEmptyObject( this.get('orderLines')) ){
             if (index > 0)
                index = index - 1;
            var new_line = this.get('orderLines').models[index]
            this.selectLine(new_line);
        }

    },
    selectLine: function(line){
        if(line){
            if (line !== this.selected_orderline){
                if(this.selected_orderline) {
                    this.selected_orderline.set_selected(false);
                }
                this.selected_orderline = line;
                this.set('selected_line',   this.selected_orderline );
                this.selected_orderline.set_selected(true);
            }
        }
        else{
          this.selected_orderline = undefined;
        }
    },
    getLastOrderline: function(){
        return this.get('orderLines').at(this.get('orderLines').length -1);
    },
    check: function(){
        var res = true
        if ( this.get("partner") == "" ){
            alert(_t("Partner can not be empty."));
            res = false
        }
        if ( this.get("orderLines").length == 0 ){
            alert(_t("Order lines can not be empty."));
            res = false;
        } else{
            (this.get('orderLines')).each(_.bind( function(item) {
                if ( !item.check() ){
                    alert(_t("Product can not be empty"));
                    res = false;
                }
            }, this));
        }
        return res
    },
    exportAsJSON: function() {
        var orderLines;
        orderLines = [];
        (this.get('orderLines')).each(_.bind( function(item) {
            return orderLines.push(item.export_as_JSON());
        }, this));
        return {
            lines: orderLines,
            name: this.get('num_order'),
            partner_id: this.ts_model.db.partner_name_id[this.get('partner')],
            action_button: this.get('action_button'),
            erp_id: this.get('erp_id'),
            erp_state: this.get('erp_state'),
            date_invoice: this.get('date_invoice'),
            date_order: this.get('date_order'),
            date_planned: this.get('date_planned'),
            note: this.get('coment'),
            customer_comment: this.get('customer_comment'),
            client_order_ref: this.get('client_order_ref'),
            supplier_id : this.ts_model.db.supplier_from_name_to_id[this.get('supplier')],
            set_promotion: this.get('set_promotion')
        };
    },
    get_last_line_by: function(period, client_id){
      var model = new instance.web.Model('sale.order.line');
      var cache_sold_lines = self.ts_model.db.cache_sold_lines[client_id]
      if (cache_sold_lines && period == 'year'){
          self.ts_model.get('sold_lines').reset(cache_sold_lines)
      }
      else{
          var loaded = model.call("get_last_lines_by",[period, client_id],{context:new instance.web.CompoundContext()})
              .then(function(order_lines){
                      if (!order_lines){
                        order_lines = []
                      }
                        // self.add_lines_to_current_order(order_lines);
                      if(period == 'year'){
                          self.ts_model.db.cache_sold_lines[client_id] = order_lines;
                      }
                      self.ts_model.get('sold_lines').reset(order_lines)
              });
            return loaded
      }
    },
    add_lines_to_current_order: function(order_lines, fromsoldprodhistory){
        this.get('orderLines').unbind();  //unbind to render all the lines once, then in OrderWideget we bind again
        if(this.selected_orderline && this.selected_orderline.get('code') == "" && this.selected_orderline.get('product') == "" ){
          $('.remove-line-button').click()
        }
        for (key in order_lines){
            var line = order_lines[key];
            var prod_obj = this.ts_model.db.get_product_by_id(line.product_id[0]);
            if  (!prod_obj){
              alert(_t('This product can not be loaded, becouse is not registerd'))
              return
            }
            current_olines = this.get('orderLines').models
            // var product_exist = false;
            for (key2 in current_olines){
                var o_line = current_olines[key2];
                var line_product_id =  this.ts_model.db.product_name_id[o_line.get('product')];

                // if (line_product_id == prod_obj.id)
                //     product_exist = true;
            }

            // if (!product_exist){
            var l_qty = line.product_uom_qty
            if(fromsoldprodhistory){
              l_qty = 1.0;
            }
            var line_vals = {ts_model: this.ts_model, order:this,
                             code:prod_obj.default_code || "" ,
                             product:prod_obj.name,
                             unit:prod_obj.uom_id[1] || line.product_uom[1], //current product unit
                             qty:my_round(l_qty), //order line qty
                             pvp: my_round(line.current_pvp ? line.current_pvp : 0, 2), //current pvp
//                                 total: my_round(line.current_pvp ? (line.product_uom_qty * line.current_pvp) * (1 - line.discount /100) : 0 ,2),
                             total: my_round(line.product_uom_qty * line.price_unit * (1 - line.discount /100)),
                             discount: my_round( line.discount || 0.0, 2 ),
                             weight: my_round(line.product_uom_qty * prod_obj.weight,2),
                             margin: my_round(( (line.current_pvp != 0 && prod_obj.product_class == "normal") ? ( (line.current_pvp - prod_obj.standard_price) / line.current_pvp)  : 0 ), 2),
                             taxes_ids: line.tax_id || product_obj.taxes_id || [],
                             pvp_ref: line.current_pvp ? line.current_pvp : 0, //#TODO CUIDADO PUEDE NO ESTAR BIEN
                             qnote: line['q_note'][1] || "",
                             detail: line["detail_note"] || "",
                             product_uos: line['product_uos'][1] || "",
                             product_uos_qty: line['product_uos_qty'] || 0.0,
                             price_udv: line['price_udv'] || 0.0,
                             tourism: line['tourism'] ? line[tourism][0]
                              : false
                            }
            var line = new exports.Orderline(line_vals);
            this.get('orderLines').add(line);
            // }
            // else{
            //   alert(_t("This product is already in the order"));
            // }
        }
        $('.col-code').focus(); //si no, al añadir línea desde resumen de pedidos, no existe foco y si añade más líneas da error
    },
    deleteProductLine: function(id_line){
      var self=this;
      // self.get('orderLines')
    },
    addProductLine: function(product_id){
        var self=this;
        // var customer_id = this.ts_model.db.partner_name_id[this.get('partner')];
        if($('#partner').val()){
            if(this.selected_orderline && this.selected_orderline.get('code') == "" && this.selected_orderline.get('product') == "" ){
              $('.remove-line-button').click()
            }
            $('.add-line-button').click()
            var added_line = self.ts_model.get('selectedOrder').getLastOrderline();
            var lines_widgets = self.ts_model.ts_widget.new_order_screen.order_widget.orderlinewidgets
            lines_widgets[lines_widgets.length - 1].call_product_id_change(product_id)
        }
        else{
            alert(_t('Please select a customer before adding a order line'));
        }
        // if (customer_id){
        //     var kwargs = {context: new instance.web.CompoundContext({}),
        //                   partner_id: customer_id,
        //                  }
        //     var pricelist_id = (this.ts_model.db.get_partner_by_id(customer_id)).property_product_pricelist;
        //     var model = new instance.web.Model("sale.order.line");
        //     model.call("product_id_change_with_wh",[[],pricelist_id,product_id],kwargs)
        //         .then(function(result){
        //             var product_obj = self.ts_model.db.get_product_by_id(product_id);
        //             var line_vals = {ts_model: self.ts_model, order:self,
        //                  code:product_obj.default_code || "" ,
        //                  product:product_obj.name,
        //                  product_uos_qty:1,
        //                  product_uos:product_obj.uom_id[1],
        //                  product_uos:(result.value.product_uos) ? self.model.ts_model.db.unit_by_id[result.value.product_uos].name : product_obj.uom_id[1]);
        //                  price_udv: my_round(result.value.price_unit || 0, 2),
        //                  unit:product_obj.uom_id[1],
        //                  qty:1,
        //                  pvp: my_round(result.value.price_unit || 0,2), //TODO poner impuestos de producto o vacio
        //                  total: my_round(result.value.price_unit || 0,2), //TODO poner impuestos de producto o vacio
        //                  discount: 0,
        //                  weight: product_obj.weight || 0.0,
        //                  margin: my_round( (result.value.price_unit != 0 && product_obj.product_class == "normal") ? ( (result.value.price_unit - product_obj.standard_price) / result.value.price_unit) : 0 , 2),
        //                  taxes_ids: result.value.tax_id || [],
        //                  pvp_ref: my_round(result.value.price_unit || 0,2), //TODO poner impuestos de producto o vacio
        //                 }
        //             var line = new exports.Orderline(line_vals);
        //             line.call_product_id_change(product_obj.id)
        //             self.get('orderLines').add(line);
        //         });
        // }
        // else{
        //     alert(_t("No Customer defined in current order"));
        // }

        // var pricelist_id = (this.ts_model.db.get_partner_by_id(partner_id)).property_product_pricelist;
    },

});

exports.OrderCollection = Backbone.Collection.extend({
    model: exports.Order,
});


return exports; 

});


