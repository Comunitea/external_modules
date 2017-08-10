odoo.define('telesale.new_order_widgets', function (require) {
"use strict";

var core = require('web.core');
var Model = require('web.DataModel');
var models = require('telesale.models');
var _t = core._t;

var TsBaseWidget = require('telesale.TsBaseWidget');



// **************************************************************************************************************************
// ************************************************ORDER BUTTON WIDGET*******************************************************
// **************************************************************************************************************************
var OrderButtonWidget = TsBaseWidget.extend({
    template:'Order-Button-Widget',
    init: function(parentautocomplete, options) {

        this._super(parent,options);
        var self = this;
        this.order = options.order;
        this.bo_id = this.ts_model.get('bo_id');
        this.order.bind('destroy',function(){ self.destroy(); });
        this.ts_model.bind('change:selectedOrder', _.bind( function(ts_model) {
           self.selectedOrder = ts_model.get('selectedOrder');
            self.selectedOrder.bind('change:partner', function(){ self.renderElement(); });
            if (self.order === self.selectedOrder) {
                self.setButtonSelected();
            }
        }, this));
    },
    renderElement:function(){
        this._super();
        this.$('button.select-order').off('click').click(_.bind(this.selectOrder, this));
        this.$('button.close-order').off('click').click(_.bind(this.closeOrder, this));
        if (this.order === this.selectedOrder) {
                this.setButtonSelected();
            }
    },
    selectOrder: function(event) {
        this.ts_model.set({
            selectedOrder: this.order
        });
    },
    setButtonSelected: function() {
        var identify = 'button#' + this.bo_id
        $('.select-order').removeClass('selected-order');
        $(identify).addClass('selected-order');
        // $('.tab1').focus();
        var value = $('#partner').val()
        var partner_id = this.ts_model.db.partner_name_id[value];
        if(partner_id){
            $('#vua-button').click();
        }
    },
    closeOrder: function(event) {
        this.order.destroy();
    },
});



// **************************************************************************************************************************
// ************************************************DATA ORDER WIDGET*********************************************************
// **************************************************************************************************************************
var DataOrderWidget = TsBaseWidget.extend({
    template:'Data-Order-Widget',
    init: function(parent, options) {
        this._super(parent,options);
        this.ts_model.bind('change:selectedOrder', this.change_selected_order, this);
        this.order_model = this.ts_model.get('selectedOrder');
    },
    change_selected_order: function() {
        this.renderElement();
    },
    renderElement: function () {
        var self = this;
        this.order_model = this.ts_model.get('selectedOrder');
        this._super();
        this.$('#partner').blur(_.bind(this.set_value, this, 'partner'))
        this.$('#shipp_addr').blur(_.bind(this.set_value, this, 'shipp_addr'))
        this.$('#date_order').blur(_.bind(this.set_value, this, 'date_order'))
        this.$('#requested_date').blur(_.bind(this.set_value, this, 'requested_date'))
        this.$('#coment').blur(_.bind(this.set_value, this, 'coment'))
        this.$('#client_order_ref').blur(_.bind(this.set_value, this, 'client_order_ref'))
        this.$('#observations').blur(_.bind(this.set_value, this, 'observations'))
        this.$('#pricelist').blur(_.bind(this.set_value, this, 'pricelist'))

        var array_names = self.ts_model.get('customer_names');
        // Autocomplete products and units from array of names
        this.$('#partner').autocomplete({
            source: function(request, response) {
                var results = $.ui.autocomplete.filter(array_names, request.term);
                response(results.slice(0, 20));
            }
        });
        this.$('#partner').keydown(function(e){
            if( e.keyCode != $.ui.keyCode.ENTER ) return; 

            e.keyCode = $.ui.keyCode.DOWN;
            $(this).trigger(e);

            e.keyCode = $.ui.keyCode.TAB;
            $(this).trigger(e);
    
            return false;
        });

        this.$('#shipp_addr').autocomplete({
            source: function(request, response) {
                var results = $.ui.autocomplete.filter(array_names, request.term);
                response(results.slice(0, 20));
            }
        });
        this.$('#shipp_addr').keydown(function(e){
            if( e.keyCode != $.ui.keyCode.ENTER ) return; 

            e.keyCode = $.ui.keyCode.DOWN;
            $(this).trigger(e);

            e.keyCode = $.ui.keyCode.TAB;
            $(this).trigger(e);
    
            return false;
        });

        // Pricelist autocomplete
        var pricelist_names = self.ts_model.get('pricelist_names');
        // Autocomplete products and units from array of names
        this.$('#pricelist').autocomplete({
            source: function(request, response) {
                var results = $.ui.autocomplete.filter(pricelist_names, request.term);
                response(results.slice(0, 20));
            }
        });
        this.$('#pricelist').keydown(function(e){
            if( e.keyCode != $.ui.keyCode.ENTER ) return; 

            e.keyCode = $.ui.keyCode.DOWN;
            $(this).trigger(e);

            e.keyCode = $.ui.keyCode.TAB;
            $(this).trigger(e);
    
            return false;
        });
    },
    set_value: function(key) {
        var value = this.$('#' + key).val();
        if (value == this.order_model.get('partner') ) {
            return;
         }
        this.order_model.set(key, value);
        this.perform_onchange(key, value);
    },

    // FULL OVERWRITED IN MODULE JIM TELESALE
    perform_onchange: function(key, value) {
        var self=this;
        if (!value) {return;}
        if (key == "partner"){
            var partner_id = self.ts_model.db.partner_name_id[value];

            // Not partner found in backbone model
            if (value && !partner_id){
                var alert_msg = _t("Customer name '" + value + "' does not exist");
                alert(alert_msg);
                self.order_model.set('partner', "");
                self.refresh();
                self.$('#partner').focus();
            }
            else {
                var partner_obj = self.ts_model.db.get_partner_by_id(partner_id);
                var model = new Model("sale.order");
                model.call("ts_onchange_partner_id", [partner_id])
                .then(function(result){

                    var cus_name = self.ts_model.getComplexName(partner_obj);
                    self.order_model.set('partner', cus_name);
                    self.order_model.set('partner_code', partner_obj.ref ? partner_obj.ref : "");
                    
                    self.order_model.set('observations', partner_obj.comment);
                    // TODO nan_partner_risk migrar a la 10
                    // self.order_model.set('limit_credit', self.ts_model.my_round(partner_obj.credit_limit,2));
                    // self.order_model.set('customer_debt', self.ts_model.my_round(partner_obj.credit,2));

                    self.order_model.set('comercial', partner_obj.user_id ? partner_obj.user_id[1] : "");
                    var partner_shipp_obj = self.ts_model.db.get_partner_by_id(result.partner_shipping_id);
                    var shipp_addr =self.ts_model.getComplexName(partner_shipp_obj);
                    self.order_model.set('shipp_addr', shipp_addr);
                    var pricelist_obj = self.ts_model.db.pricelist_by_id[result.pricelist_id];
                    if (pricelist_obj){
                        self.order_model.set('pricelist', pricelist_obj.name);
                    }

                    self.refresh();
                     // New line and VUA button when chang
                    // Only do it when partner is setted
                    if (self.order_model.get('partner')){
                        $('#vua-button').click();
                    }
                    if(self.order_model.get('orderLines').length == 0){
                        $('.add-line-button').click()
                    }
                    else{
                        self.$('#date_order').focus();
                    }
                });
            }
        }
        else if (key == "pricelist"){
            var pricelist_id = self.ts_model.db.pricelist_name_id[value];

            // Not partner found in backbone model
            if (!pricelist_id){
                var alert_msg = _t("Pricelist name '" + value + "' does not exist");
                alert(alert_msg);
                self.order_model.set('pricelist', "");
                self.refresh();
                self.$('#pricelist').focus();
            }
        }
    },
    refresh: function(){
        this.renderElement();
    },
});



// **************************************************************************************************************************
// ************************************************ORDER LINE WIDGET*********************************************************
// **************************************************************************************************************************
var OrderlineWidget = TsBaseWidget.extend({
    template: 'Order-line-Widget',
    init: function(parent, options) {
        this._super(parent,options);
        this.order_widget = parent
        this.model = options.model;
        this.order = options.order;

        this.model.bind('change_line', this.refresh, this); //#TODO entra demasiadas veces por la parte esta
    },
    click_handler: function(key) {
        var selector = '.col-' + key
        this.order.selectLine(this.model);
        this.$(selector).unbind('focus')
        this.$(selector).focus()
        this.$(selector).select()
        this.$(selector).focus(_.bind(this.click_handler, this, key));
    },
    control_arrow_keys: function(){
      var self=this;
        this.$('.col-pvp').keydown(function(event){
          var keyCode = event.keyCode || event.which;
          if (keyCode == 40) {  // KEY DOWWN (40) 
                event.preventDefault();
                $(this).parent().parent().next().find('.col-pvp').select();

            }
            else if (keyCode == 38){  //KEY UP
                event.preventDefault();
                $(this).parent().parent().prev().find('.col-pvp').select();
            }
        });
        this.$('.col-discount').keydown(function(event){
          var keyCode = event.keyCode || event.which;
          if (keyCode == 40) {  // KEY DOWWN (40) 
                event.preventDefault();
                $(this).parent().parent().next().find('.col-discount').select();

            }
            else if (keyCode == 38){  //KEY UP
                event.preventDefault();
                $(this).parent().parent().prev().find('.col-discount').select();
            }
        });

        this.$('.col-qty').keydown(function(event){
            var keyCode = event.keyCode || event.which;
            if (keyCode == 40) {  // KEY DOWWN (40) 
                event.preventDefault();
                $(this).parent().parent().next().find('.col-qty').select();

            }
            else if (keyCode == 38){  //KEY UP
                event.preventDefault();
                $(this).parent().parent().prev().find('.col-qty').select();
            }
        });
    },
    set_input_handlers: function() {
        // Si el campo se rellena con autocomplete se debe usar blur
        // this.$('.col-code').blur(_.bind(this.set_value, this, 'code'));
        // this.$('.col-code').focus(_.bind(this.click_handler, this, 'code'));

        this.$('.col-product').blur(_.bind(this.set_value, this, 'product'));
        this.$('.col-product').focus(_.bind(this.click_handler, this, 'product'));

       
        this.$('.col-qty').change(_.bind(this.set_value, this, 'qty'));
        this.$('.col-qty').focus(_.bind(this.click_handler, this, 'qty'));

        this.$('.col-product_uom').blur(_.bind(this.set_value, this, 'unit'));
        this.$('.col-product_uom').focus(_.bind(this.click_handler, this, 'unit'));

        this.$('.col-pvp').change(_.bind(this.set_value, this, 'pvp'));
        this.$('.col-pvp').focus(_.bind(this.click_handler, this, 'pvp'));

        this.$('.col-discount').blur(_.bind(this.set_value, this, 'discount'));
        this.$('.col-discount').focus(_.bind(this.click_handler, this, 'discount'));

        this.$('.col-total').change(_.bind(this.set_value, this, 'total'));
        this.$('.col-total').focus(_.bind(this.click_handler, this, 'total'));
    },
    load_input_fields: function() {
        // Cargo todas las unidades en la linea
        for (var unit in this.ts_model.db.unit_name_id){
            var dic = { value: unit,
                        text: unit}
             if (unit == this.model.get('unit')){
                    dic['selected'] =  "selected"
            }
            this.$('.col-product_uom').append($('<option>', dic))
        }
        var product_names = this.ts_model.get('products_names')
        this.$('.col-product').autocomplete({
            source: function(request, response) {
                var results = $.ui.autocomplete.filter(product_names, request.term);
                response(results.slice(0, 20));
            }
        });
        this.$('.col-product').keydown(function(e){
            if( e.keyCode != $.ui.keyCode.ENTER ) return; 

            e.keyCode = $.ui.keyCode.DOWN;
            $(this).trigger(e);

            e.keyCode = $.ui.keyCode.TAB;
            $(this).trigger(e);
    
            return false;
        });
    },
    set_value: function(key) {
        var self = this;
        var value = this.$('.col-'+key).val();
        var set=true;
        if (key == 'qty' || key == 'pvp' || key == 'total' || key == 'discount' ){
            if (isNaN(value)){
                this.$('.col-'+key).val(this.model.get(key));
                alert(_t(value + " is not a valid number"));
                set=false;
            }
            else
                value = self.ts_model.my_round(value,2);
        }
        if (set){
            if ( this.model.get(key) != value || key == "discount"){
            // if ( this.model.get(key) != value){
                this.model.set(key, value);
                this.perform_onchange(key);
            }
        }
    },
    // OVERWRITED IN JIM TELESALE
    call_product_id_change: function(product_id, add_qty){
        var self = this;

        if (!add_qty){
            add_qty = 1.0
        }
        var customer_id = self.ts_model.db.partner_name_id[self.order.get('partner')];
        var pricelist_id = self.ts_model.db.pricelist_name_id[self.order.get('pricelist')];
        var model = new Model("sale.order.line");
        return model.call("ts_product_id_change", [product_id, customer_id, pricelist_id])
        .then(function(result){
            var product_obj = self.ts_model.db.get_product_by_id(product_id);
            self.model.set('code', product_obj.default_code || "");
            self.model.set('product', product_obj.display_name || "");
            self.model.set('taxes_ids', result.tax_id || []); //TODO poner impuestos de producto o vacio
            self.model.set('unit', self.model.ts_model.db.unit_by_id[result.product_uom].name);
            self.model.set('qty', add_qty);
            self.model.set('discount', 0.0);
            self.model.set('standard_price', result.standard_price || 0.0);
            self.model.set('pvp', self.ts_model.my_round( result.price_unit));
           
            var subtotal = self.model.get('pvp') * self.model.get('qty') * (1 - self.model.get('discount') / 100.0)
            self.model.set('total', self.ts_model.my_round(subtotal || 0,2));
            self.refresh('qty');
            self.$('.col-qty').select();
        });
    },
    call_product_uom_change: function(product_id, qty){
        var self = this;
        var customer_id = self.ts_model.db.partner_name_id[self.order.get('partner')];
        var pricelist_id = self.ts_model.db.pricelist_name_id[self.order.get('pricelist')];
        var model = new Model("sale.order.line");
        return model.call("ts_product_uom_change", [product_id, customer_id, pricelist_id, qty])
        .then(function(result){
            self.model.set('pvp', self.ts_model.my_round(result.price_unit));
            var subtotal = self.model.get('pvp') * self.model.get('qty') * (1 - self.model.get('discount') / 100.0)
            self.model.set('total', self.ts_model.my_round(subtotal || 0,2));
            self.refresh('pvp');
            self.$('.col-pvp').select();
        });
    },
    perform_onchange: function(key) {
        var self=this;
        var value = this.$('.col-'+key).val();
        switch (key) {
            case "code":
                // comprobar que clave está en el array
                var product_id = this.ts_model.db.product_code_id[value];
                if (!product_id){
                    alert(_t("Product code '" + value + "' does not exist"));
                    this.model.set('code', "");
                    this.model.set('product', "");
                    this.model.set('product_uos_qty', 0.0);
                    this.refresh('qty');
                    break;
                }
                this.call_product_id_change(product_id);

                break;
            case "product":
                // comprobar que clave está en el array
                var self = this;
                var product_id = this.ts_model.db.product_name_id[value];
                if (!product_id){
                    alert(_t("Product name '" + value + "' does not exist"));
                    this.model.set('code', "");
                    this.model.set('product', "");
                    this.model.set('product_uos_qty', 0.0);
                    this.refresh('qty');
                    break;
                }
                this.call_product_id_change(product_id);
                break;
            case "qty":
            // TODO CALL CHECK FLOAT
            var qty = parseFloat(value)
                this.refresh('unit');
                this.$('.col-unit').focus()
                var product_name = this.model.get('product')
                if (product_name){
                    var product_id = this.ts_model.db.product_name_id[product_name];
                    this.call_product_uom_change(product_id, qty);
                }
                break;
            case "unit":
                this.refresh('pvp');
                break;
            case "pvp":
                this.refresh('discount');
                break;
            case "discount":
                this.refresh('code');
                break;
        }
    },
    refresh: function(focus_key){
        this.renderElement();
        this.$('.col-'+ focus_key).focus()
    },
    renderElement: function() {
        this.model.update_line_values();
        var self=this;
        this._super();
        this.$el.unbind()

        // Set color n_line selected NOT WORKING
        if(this.model.is_selected()){
            this.$('.col-nline').addClass('selected');
        }
        // Set handlers for the line input fields
        this.set_input_handlers();
        // Mapeo de teclas para moverse por la tabla con las flechas
        // Creamos nueva linea al tabular la última columna de descuento
        this.control_arrow_keys()
        // Set autocompletes of product and unit field
        this.load_input_fields();
    },
});



// **************************************************************************************************************************
// ************************************************ORDER WIDGET**************************************************************
// **************************************************************************************************************************

var OrderWidget = TsBaseWidget.extend({
        template:'Order-Widget',
        events: {
            'click .add-line-button': 'button_add_line',
            'click .remove-line-button': 'button_remove_line',
            'click  #ult-button': 'button_ult',
            'click  #vua-button': 'button_vua',
            'click  #so-button': 'button_so',
            'click  #promo-button': 'button_promo',
            'click  #info-button': 'button_info',
            'click  #show-client': 'button_show_client',
            // 'click  #filter-client': 'button_filter_client',
        },
        init: function(parent, options) {
            this._super(parent,options);
            this.ts_model.bind('change:selectedOrder', this.change_selected_order, this);
            this.bind_orderline_events();
            this.orderlinewidgets = [];
        },
        change_selected_order: function() {
            // Called when cahange selectedOrder, 
            // Unbind current order linds and bind the new ones. 
            this.currentOrderLines.unbind();
            this.bind_orderline_events();
            this.renderElement();
        },
        bind_orderline_events: function() {
            // Called when cahange selectedOrder, 
            // Get SelectedOrder orderlines from model, and bind add and remove lines events
            // When we renderElement, we recalculate the orderlines
            this.currentOrderLines = (this.ts_model.get('selectedOrder')).get('orderLines');
            this.currentOrderLines.bind('add', this.renderElement, this);
            this.currentOrderLines.bind('remove', this.renderElement, this);
        },
        show_product: function(product_id){
            // Shows Product form view in a PopUp
            if (product_id){
                this.do_action({
                    type: 'ir.actions.act_window',
                    res_model: "product.product",
                    res_id: product_id,
                    views: [[false, 'form']],
                    target: 'new',
                    context: {},
                });
            }
        },
        button_add_line: function(){
            // click add line event function
            var order =  this.ts_model.get('selectedOrder')
            var partner_id = this.ts_model.db.partner_name_id[order.get('partner')]
            if (!partner_id){
                alert(_t('Please select a customer before adding a order line'));
                $('#partner').focus();
            }else{
                this.ts_model.get('selectedOrder').addLine();
                var added_line = this.ts_model.get('selectedOrder').getLastOrderline();
                this.ts_model.get('selectedOrder').selectLine(added_line);
                this.orderlinewidgets[this.orderlinewidgets.length - 1].$('.col-product').focus(); //set focus on line when we add one
            }
        },
        button_remove_line: function(){
            this.ts_model.get('selectedOrder').removeLine();
            var selected_line = this.ts_model.get('selectedOrder').getSelectedLine();
            if (selected_line){
                var n_line = selected_line.get('n_line')
                this.orderlinewidgets[n_line-1].$('.col-product').focus();
            }
        },
        button_ult: function(){
            // Get last line sold.
            var self=this;
            var client_id = this.check_customer_get_id();
            if (client_id){
                $.when(self.ts_model.get('selectedOrder').get_last_line_by('ult', client_id))
                .done(function(){
                })
                .fail(function(){
                    alert(_t("NOT WORKING"));
                })
            }
        },
        button_vua: function(){
            var self=this;
            var client_id = this.check_customer_get_id();
            if (client_id){
                $.when(self.ts_model.get('selectedOrder').get_last_line_by('year', client_id))
                .done(function(){
                })
                .fail(function(){
                    alert(_t("NOT WORKING"));
                })
            }
        },
       button_so: function(){
            var self = this;
            var client_id = this.check_customer_get_id();
            if (client_id){
            $.when(self.ts_model.get('selectedOrder').get_last_line_by('3month', client_id))
            .done(function(){
            })
            .fail(function(){
                alert(_t("NOT WORKING"));
            })
            }
        },
        button_promo: function(){
           var self = this;
           var current_order = this.ts_model.get('selectedOrder')
           current_order.set('set_promotion', true)
           this.ts_widget.new_order_screen.totals_order_widget.saveCurrentOrder()
           $.when( self.ts_model.ready2 )
           .done(function(){
           var loaded = self.ts_model.fetch('sale.order',
                                           ['id', 'name'],
                                           [
                                               ['chanel', '=', 'telesale']
                                           ])
               .then(function(orders){
                   if (orders[0]) {
                   var my_id = orders[0].id
                   $.when( self.ts_widget.new_order_screen.order_widget.load_order_from_server(my_id) )
                   .done(function(){
                   });

                 }
               });
            });
            
        },
        button_info: function(){
            var current_order = this.ts_model.get('selectedOrder')
            var selected_line = current_order.selected_orderline;
            if (!selected_line){
                alert(("You must select a product line."));
            }else{
                var product_id = this.ts_model.db.product_name_id[selected_line.get('product')];
                if (!product_id){
                    alert(_t("This line has not a product defined."));
                }
                else{
                    this.show_product(product_id)
                }
            }
            
        },
        button_show_client: function(){
            // var win = window.open('', '_blank');
            var client_id = this.check_customer_get_id()
            if (client_id){
                this.do_action({
                    type: 'ir.actions.act_window',
                    res_model: "res.partner",
                    res_id: client_id,
                    views: [[false, 'form']],
                    target: 'new',
                    context: {},
                });
            }
            else{
              alert(_t('You must select a customer'));
            }
        },
        check_customer_get_id: function(){
            var client_name = this.ts_model.get('selectedOrder').get('partner')
            var client_id = this.ts_model.db.partner_name_id[client_name];
            if (!client_id){
                alert(_t('No customer defined'));
                return false
            }
            else{
                return client_id
            }
        },
        
        get_order_fields: function(){
        // Called when load an order from server
            return ['partner_shipping_id','note','comercial','client_order_ref','name',
                    'partner_id','date_order','state','amount_total','requested_date', 'pricelist_id', 'observations']

        },
        get_line_fields: function(){
        // Called when load the order lines from server
            var line_fields = ['product_id','product_uom','product_uom_qty','price_unit',
                               'tax_id', 'price_subtotal', 'discount', 'standard_price'];
            return line_fields;

        },
        load_order_from_server: function(order_id, flag){
            // Gets and order_id from server, and shows it.
            var self=this;
            if (!flag){
                this.ts_model.get('orders').add(new models.Order({ ts_model: self.ts_model}));
            }
            this.open_order =  this.ts_model.get('selectedOrder')
            var order_fields = this.get_order_fields();
            var loaded = self.ts_model.fetch('sale.order', order_fields, [['id', '=', order_id]])
            .then(function(orders){
                var order = orders[0];
                self.order_fetch = order;
                var line_fields = self.get_line_fields();
                return self.ts_model.fetch('sale.order.line', line_fields, [['order_id', '=', order_id]]);
            }).then(function(order_lines){
                if (flag =='add_lines'){
                    self.open_order.add_lines_to_current_order(order_lines);
                    self.ts_widget.new_order_screen.data_order_widget.refresh();
                    self.ts_widget.new_order_screen.order_widget.change_selected_order()
                    self.ts_widget.new_order_screen.totals_order_widget.changeTotals();
                }else{
                    self.ts_model.build_order(self.order_fetch, self.open_order, order_lines); //build de order model
                    self.ts_widget.new_order_screen.data_order_widget.refresh();
                }
                self.renderElement();
            })
            return loaded
        },

        // Creates a line with product and unit seted
        create_line_empty: function(product_id){
            var current_order= this.ts_model.get('selectedOrder');
            var added_line = current_order.addLine();
            var product_obj = this.ts_model.db.get_product_by_id(product_id)
            var product_name = product_obj.display_name;
            added_line.set('product', product_name);
            var uom_obj = self.ts_model.db.get_unit_by_id(product_obj.uom_id)
            added_line.set('unit', uom_obj.name);
            return added_line;
        },

        create_line_from_vals: function(product_id, line_vals){
            var added_line = this.create_line_empty(product_id);
            var prod_obj = this.ts_model.db.get_product_by_id(product_id);
            added_line.set('qty', line_vals.qty || 1.0);
            added_line.set('pvp', line_vals.price || 0.0);
            added_line.set('discount', line_vals.discount || 0.0);
            added_line.set('taxes_ids', line_vals.tax_ids || []); 
            added_line.update_line_values();
            return
        },
        // Get lines from model and render it
        renderLines: function(options){
            var self = this;

            // Destroy line widgets
            for(var i = 0, len = this.orderlinewidgets.length; i < len; i++){
                this.orderlinewidgets[i].destroy();
            }
            this.orderlinewidgets = [];

            var $content = this.$('.orderlines');
            var nline = 1
            this.currentOrderLines.each(_.bind( function(orderLine) {
                orderLine.set('n_line', nline++);
                var line = new OrderlineWidget(this, {
                    model: orderLine,
                    order: this.ts_model.get('selectedOrder'),
                });
                line.appendTo($content);
                self.orderlinewidgets.push(line);
            }, this));
        },
        // Delete lines widgets and read models to get the news ones.
        renderElement: function () {
            // Events linked in dict events
            var self = this;
            this._super();

            // Get lines from model and render it
            self.renderLines();

        },
    });   



// **************************************************************************************************************************
// *********************************************** PRODUCT INFO ORDER WIDGET ************************************************
// **************************************************************************************************************************
var ProductInfoOrderWidget = TsBaseWidget.extend({
    template:'ProductInfo-Order-Widget',
    init: function(parent, options) {
        this._super(parent,options);
        this.ts_model.bind('change:selectedOrder', this.change_selected_order, this);
        this.order_model = this.ts_model.get('selectedOrder');
        this.selected_line = undefined;
        this.bind_selectedline_events();
        this.set_default_values();
    },
    set_default_values: function(){
        this.stock = "";
        this.date = "";
        this.qty = "";
        this.price = ""; 
        this.n_line = "";
    },
    bind_selectedline_events: function(){
        this.order_model = this.ts_model.get('selectedOrder');
        this.order_model.bind('change:selected_line', this.calcProductInfo, this);
    },
    change_selected_order: function() {
        this.order_model.unbind('change:selected_line');
        this.bind_selectedline_events()
        this.set_default_values();
        this.renderElement();
    },
    renderElement: function () {
        var self = this;
        this.order_model = this.ts_model.get('selectedOrder');
        this._super();
        if(this.stock <= 0){
          this.$('#stock-info').addClass('warning-red')
        }
        $('.product-info-table').click(function (){ self.showHistory() });
    },
    showHistory: function(){
       this.ts_widget.screen_selector.show_popup('filter_customer_popup', this.selected_line);
    },
    calcProductInfo: function () {
        var self = this;
        this.selected_line = this.ts_model.get('selectedOrder').get('selected_line');
        if (!this.selected_line.get("product")){
            this.set_default_values();
            this.renderElement();
        }
        this.selected_line.unbind('change:product');
        this.selected_line.bind('change:product', this.change_product, this);
        this.selected_line.trigger('change:product');

    },
    change_product: function(){
        var self = this;
        // TODO A VER QUE PASA
        var line_product = this.selected_line.get("product")
        self.n_line = self.selected_line.get('n_line') + " / " + self.ts_model.get('selectedOrder').get('orderLines').length;
        if (line_product != ""){
            var product_id = this.ts_model.db.product_name_id[line_product]
            var partner_name = this.ts_model.get('selectedOrder').get('partner');
            var partner_id = this.ts_model.db.partner_name_id[partner_name];
            if (product_id && partner_id){
                var model = new Model('product.product');
                model.call("get_product_info",[product_id,partner_id])
                    .then(function(result){
                        self.stock = self.ts_model.my_round(result.stock,2).toFixed(2);
                        self.date = result.last_date != "-" ? self.ts_model.localFormatDate(result.last_date.split(" ")[0]) : "-";
                        self.qty = self.ts_model.my_round(result.last_qty,4).toFixed(2);
                        self.price = self.ts_model.my_round(result.last_price,2).toFixed(2);
                        self.renderElement();
                    });
            }
            else{
                this.set_default_values();
                this.renderElement();
            }
        }
    },
});



// **************************************************************************************************************************
// ****************************************** SOLD PRODUCT WIDGET ***********************************************************
// **************************************************************************************************************************
var SoldProductLineWidget = TsBaseWidget.extend({
    template:'Sold-Product-Line-Widget',
    init: function(parent, options){
        this._super(parent,options);
        this.sold_line = options.sold_line;
    },

    renderElement: function() {
        var self=this;
        this._super();
        this.$('#add-line').off("click").click(_.bind(this.add_product_to_order, this));

    },
    add_product_to_order: function() {
        var self=this;
        var product_id = this.sold_line.product_id[0]
        if (product_id){
            var current_order= this.ts_model.get('selectedOrder')
            current_order.addProductLine(product_id);
        }
    },
});

var SoldProductWidget = TsBaseWidget.extend({
    template:'Sold-Product-Widget',
    init: function(parent, options){
        var self = this;
        this._super(parent,options);
        // TODO ???
        this.ts_model.get('sold_lines').bind('reset', function(){
            self.renderElement();
        });
        this.line_widgets = [];
    },

    renderElement: function() {
        var self=this;
        this._super();
        // free subwidgets  memory from previous renders
        for(var i = 0, len = this.line_widgets.length; i < len; i++){
            this.line_widgets[i].destroy();
        }
        this.line_widgets = [];
        // sold lines tiene ahora objetos con info de producto
        var sold_lines = this.ts_model.get("sold_lines").models || []

        var $lines_content = this.$('.soldproductlines');
        for (var i=0, len = sold_lines.length; i < len; i++){
            var line_obj = sold_lines[i].attributes;
            var sold_line = new SoldProductLineWidget(self, {sold_line: line_obj})
            this.line_widgets.push(sold_line)
            sold_line.appendTo($lines_content)
        }
    },
});



// **************************************************************************************************************************
// *********************************************** TOTALS ORDER WIDGET ******************************************************
// **************************************************************************************************************************
var TotalsOrderWidget = TsBaseWidget.extend({
        template:'Totals-Order-Widget',
        init: function(parent, options) {
            this._super(parent,options);
            this.ts_model.bind('change:selectedOrder', this.change_selected_order, this);
            this.bind_orderline_events();
        },
        bind_orderline_events: function() {
            this.order_model = this.ts_model.get('selectedOrder');
            this.order_model.bind('change:selected_line', this.bind_selectedline_events, this);

            this.currentOrderLines = (this.ts_model.get('selectedOrder')).get('orderLines');
            this.currentOrderLines.bind('add', this.changeTotals, this);
            this.currentOrderLines.bind('remove', this.changeTotals, this);
        },
        bind_selectedline_events: function () {
            var self = this;

            this.selected_line = this.ts_model.get('selectedOrder').get('selected_line');
            this.selected_line.unbind('change:total');
            this.selected_line.bind('change:total', this.changeTotals, this);
        },
        change_selected_order: function() {
            this.order_model.unbind('change:selected_line');
            this.currentOrderLines.unbind();
            this.bind_orderline_events();
            this.renderElement();
        },
        renderElement: function () {
            var self = this;

            this.order_model = this.ts_model.get('selectedOrder');
            this._super();

            this.$('.confirm-button').click(function (){ self.confirmCurrentOrder() });
            this.$('.cancel-button').click(function (){ self.cancelCurrentOrder() });
            this.$('.save-button').click(function (){ self.saveCurrentOrder() });
            this.$('.print-button').click(function (){ self.printCurrentOrder() });
        },
        changeTotals: function(){
            var self = this;
            this.base = 0;
            this.discount = 0;
            this.margin = 0;
            this.weight = 0;
            this.iva = 0;
            this.total = 0;

            this.sum_cost = 0;

            (this.currentOrderLines).each(_.bind( function(line) {
                self.sum_cost += line.get('standard_price') * line.get('qty');
                self.discount += line.get('qty') * line.get('pvp') * (line.get('discount') / 100)
                var price_disc = line.get('pvp') * (1 - (line.get('discount') / 100))
                self.margin += (price_disc -  line.get('standard_price')) * line.get('qty');
                self.base += line.get_price_without_tax('total');
                self.iva += line.get_tax();

            }, this));
            self.total += self.ts_model.my_round(self.base, 2) + self.ts_model.my_round(self.iva, 2);
            self.base = self.ts_model.my_round(self.base, 2);
            this.order_model.set('total_base',self.base);
            this.order_model.set('total_iva', self.iva);
            this.order_model.set('total', self.total);
            this.order_model.set('total_discount', self.discount);
            var discount_per = (0) + "%";
            if (self.base != 0){
              // Le volvemos a sumamar el descuento porque la base viene sin el
                var discount_num = (self.discount/(self.base + self.discount) ) * 100 ;
                if (discount_num < 0)
                    var discount_per = "+" +  discount_num * (-1)  + "%";
                else
                    var discount_per =  discount_num.toFixed(2)  + "%";
            }
            this.order_model.set('total_discount_per', discount_per);
            this.order_model.set('total_margin', self.margin);
            var margin_per = (0) + "%";
            var margin_per_num = 0
            if (self.base != 0) {
                margin_per_num = ((self.base - self.sum_cost) / self.base) * 100
                margin_per = self.ts_model.my_round(margin_per_num, 2).toFixed(2) + "%"
            }
            this.order_model.set('total_margin_per', margin_per);
            this.renderElement();
        },
        confirmCurrentOrder: function() {
          var self = this;
            var currentOrder = this.order_model;
            self.saveCurrentOrder()
            $.when( self.ts_model.ready2 )
            .done(function(){
                var loaded = self.ts_model.fetch('sale.order',
                                                ['id', 'name'],
                                                [
                                                    ['chanel', '=', 'telesale']
                                                ])
                    .then(function(orders){
                        if (orders[0]) {
                          // var my_id = orders[0].id
                          (new Model('sale.order')).call('confirm_order_from_ui',[orders[0].id])
                              .fail(function(unused, event){
                                  //don't show error popup if it fails
                                  console.error('Failed confirm order: ',orders[0].name);
                              })
                              .done(function(){
                              });

                        }
                    });
             });
        },
        cancelCurrentOrder: function() {
            var currentOrder = this.order_model;
            currentOrder.set('action_button', 'cancel')
            if ( (currentOrder.get('erp_state')) && (currentOrder.get('erp_state') != 'draft') ||  !currentOrder.get('erp_id')){
                alert(_t('You cant cancel an order which state is diferent than draft.'));
            }
            else if ( currentOrder.check() ){
                this.ts_model.cancel_order(currentOrder.get('erp_id'));
            }
        },
        button_promo: function(){
           var self = this;
           var current_order = this.ts_model.get('selectedOrder')
           current_order.set('set_promotion', true)
           this.ts_widget.new_order_screen.totals_order_widget.saveCurrentOrder()
           $.when( self.ts_model.ready2 )
           .done(function(){
           var loaded = self.ts_model.fetch('sale.order',
                                           ['id', 'name'],
                                           [
                                               ['chanel', '=', 'telesale']
                                           ])
               .then(function(orders){
                   if (orders[0]) {
                   var my_id = orders[0].id
                   $.when( self.ts_widget.new_order_screen.order_widget.load_order_from_server(my_id) )
                   .done(function(){
                   });

                 }
               });
            });
            
        },
        printCurrentOrder: function() {
            var self = this;
            var current_order = this.ts_model.get('selectedOrder')
            this.ts_widget.new_order_screen.totals_order_widget.saveCurrentOrder()
            $.when( self.ts_model.ready2 )
            .done(function(){
            var loaded = self.ts_model.fetch('sale.order',
                                           ['id', 'name'],
                                           [
                                               ['chanel', '=', 'telesale']
                                           ])
               .then(function(orders){
                   if (orders[0]) {
                   var my_id = orders[0].id
                   $.when( self.ts_widget.new_order_screen.order_widget.load_order_from_server(my_id) )
                   .done(function(){
                        var currentOrder = self.ts_model.get('selectedOrder')
                        self.do_action({
                             context: {'active_ids': [currentOrder.get('erp_id')]},
                             data: null,
                             name: 'Quotation / Order',
                             report_file: 'sale.report_saleorder',
                             report_name: 'sale.report_saleorder',
                             report_type: 'qweb-pdf',
                             type: 'ir.actions.report.xml'
                        });
                   });

                 }
               });
            });
        },
        saveCurrentOrder: function() {
            var currentOrder = this.order_model;
            currentOrder.set('action_button', 'save')
            if ( (currentOrder.get('erp_state')) && (currentOrder.get('erp_state') != 'draft') ){
                alert(_t('You cant save as draft an order which state is diferent than draft.'));
            }
            else if ( currentOrder.check() ){
                this.ts_model._flush2(currentOrder.exportAsJSON());
            }
        },

});

    return {
        OrderButtonWidget: OrderButtonWidget,
        DataOrderWidget: DataOrderWidget,
        OrderlineWidget: OrderlineWidget,
        OrderWidget: OrderWidget,
        TotalsOrderWidget: TotalsOrderWidget,
        ProductInfoOrderWidget: ProductInfoOrderWidget,
        SoldProductWidget: SoldProductWidget,
        SoldProductLineWidget: SoldProductLineWidget,

    }; 
});


