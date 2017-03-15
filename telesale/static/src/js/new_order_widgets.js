odoo.define('telesale.new_order_widgets', function (require) {
"use strict";

var core = require('web.core');
var Model = require('web.DataModel');
var _t = core._t;

var TsBaseWidget = require('telesale.TsBaseWidget');


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

        /*TODO NO SE PONE EL COLOR BIEN, YA QUE COJE UNA LISTA Y NO EL BOTON*/
        var identify = 'button#' + this.bo_id
        $('.select-order').removeClass('selected-order');
        $(identify).addClass('selected-order');
        $('.tab1').focus();
        if($('#partner').val()){
            $('#vua-button').click();
        }
    },
    closeOrder: function(event) {
        this.order.destroy();
    },
});

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
        this.$('#date_order').blur(_.bind(this.set_value, this, 'date_order'))
        this.$('#date_planned').blur(_.bind(this.set_value, this, 'date_planned'))
        this.$('#coment').blur(_.bind(this.set_value, this, 'coment'))
        this.$('#customer_comment').blur(_.bind(this.set_value, this, 'customer_comment'))

        // Autocomplete products and units from array of names
        this.$('#partner').autocomplete({
            source: this.ts_model.get('customer_names'),
        });
    },
    set_value: function(key) {
        var value = this.$('#' + key).val();;
        if (value == this.order_model.get('partner') ) {
            return;
         }
        this.order_model.set(key, value);
        this.perform_onchange(key, value);
    },
    perform_onchange: function(key, value) {
        var self=this;
        if (!value) {return;}
        if (key == "partner"){
            var partner_id = self.ts_model.db.partner_name_id[value];

            // Not partner found in backbone model
            if (!partner_id){
                var alert_msg = _t("Customer name '" + value + "' does not exist");
                alert(alert_msg);
                self.order_model.set('partner', "");
                self.refresh();
            }

            else {
                var partner_obj = self.ts_model.db.get_partner_by_id(partner_id);
              
                var do_onchange = true
                
                if (do_onchange){
                    var cus_name = self.ts_model.getComplexName(partner_obj);
                    self.order_model.set('partner', cus_name);
                    self.order_model.set('partner_code', partner_obj.ref ? partner_obj.ref : "");
                    
                    self.order_model.set('customer_comment', partner_obj.comment);
                    // TODO nan_partner_risk migrar a la 10
                    // self.order_model.set('limit_credit', self.ts_model.my_round(partner_obj.credit_limit,2));
                    // self.order_model.set('customer_debt', self.ts_model.my_round(partner_obj.credit,2));
                    var contact_obj = self.ts_model.db.get_partner_contact(partner_id); //If no contacts return itself
                    self.order_model.set('comercial', partner_obj.user_id ? partner_obj.user_id[1] : "");
                    self.order_model.set('contact_name', contact_obj.name);

                    self.refresh();
                    // TODO LO DE ABAJO YA VEREMOS
                    // $('#vua-button').click();
                    // if(self.order_model.get('orderLines').length == 0){
                    //     $('.add-line-button').click()
                    // }
                    // else{
                    //     self.$('#date_order').focus();
                    // }
                }
            }
        }
    },
    load_order_from_server: function(order_id){
        var self=this;
        this.open_order =  this.ts_model.get('selectedOrder')
        var loaded = self.ts_model.fetch('sale.order',
                                        ['supplier_id','contact_id','note','comercial','customer_comment','client_order_ref','name','partner_id','date_order','state','amount_total','date_invoice', 'date_planned', 'date_invoice'],
                                        [
                                            ['id', '=', order_id]
                                        ])
            .then(function(orders){
                var order = orders[0];
                self.order_fetch = order;
                return self.ts_model.fetch('sale.order.line',
                                            ['product_id','product_uom',
                                            'product_uom_qty',
                                            'product_uos',
                                            'product_uos_qty',
                                            'price_udv','price_unit',
                                            'price_subtotal','tax_id',
                                            'pvp_ref','current_pvp',
                                            'q_note', 'detail_note',
                                            'discount', 'tourism'],
                                            [
                                                ['order_id', '=', order_id],
                                             ]);
            }).then(function(order_lines){
                    self.ts_model.build_order(self.order_fetch, self.open_order, order_lines); //build de order model
                    self.ts_widget.new_order_screen.data_order_widget.refresh();
            })
        return loaded
    },
    refresh: function(){
        this.renderElement();
    },
});

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
        this.trigger('order_line_selected');
    },
    control_arrow_keys: function(){
      var self=this;
        this.$('.col-product_uos_qty').keydown(function(event){
          var keyCode = event.keyCode || event.which;
          if (keyCode == 40 || keyCode == 38) {  // KEY DOWWN (40) up (38)
            var selected_line = self.order.selected_orderline;
            if (selected_line){
                var n_line = selected_line.get('n_line');
                var idx =(keyCode == 40) ? n_line + 1 : n_line - 1;
                var next_line = self.order_widget.orderlinewidgets[idx - 1]
                if (next_line) {

                  self.order.selectLine(next_line.model);
                  next_line.$el.find('.col-product_uos_qty').focus();
                }
            }
          }
        });
        this.$('.col-price_udv').keydown(function(event){
          var keyCode = event.keyCode || event.which;
          if (keyCode == 40 || keyCode == 38) {  // KEY DOWWN (40) up (38)
            var selected_line = self.order.selected_orderline;
            if (selected_line){
                var n_line = selected_line.get('n_line');
                var idx =(keyCode == 40) ? n_line + 1 : n_line - 1;
                var next_line = self.order_widget.orderlinewidgets[idx - 1]
                if (next_line) {

                  self.order.selectLine(next_line.model);
                  next_line.$el.find('.col-price_udv').focus();
                }
            }
          }
        });
        this.$('.col-pvp').keydown(function(event){
          var keyCode = event.keyCode || event.which;
          if (keyCode == 40 || keyCode == 38) {  // KEY DOWWN (40) up (38)
            var selected_line = self.order.selected_orderline;
            if (selected_line){
                var n_line = selected_line.get('n_line');
                var idx =(keyCode == 40) ? n_line + 1 : n_line - 1;
                var next_line = self.order_widget.orderlinewidgets[idx - 1]
                if (next_line) {

                  self.order.selectLine(next_line.model);
                  next_line.$el.find('.col-pvp').focus();
                }
            }
          }
        });
        this.$('.col-discount').keydown(function(event){
          var keyCode = event.keyCode || event.which;
          if (keyCode == 40 || keyCode == 38) {  // KEY DOWWN (40) up (38)
            var selected_line = self.order.selected_orderline;
            if (selected_line){
                var n_line = selected_line.get('n_line');
                var idx =(keyCode == 40) ? n_line + 1 : n_line - 1;
                var next_line = self.order_widget.orderlinewidgets[idx - 1]
                if (next_line) {

                  self.order.selectLine(next_line.model);
                  next_line.$el.find('.col-discount').focus();
                }
            }
          }
        });
        // my_shift = false
        // this.$('.col-discount').keydown(function(event){
        //  var keyCode = event.keyCode || event.which;
        //   if (event.shiftKey){
        //       my_shift = true
        //   }
        //   if (keyCode == 9 && !my_shift){
        //       self.$('.col-total').focus()
        //       my_shift = false
        //    }
        // });
        // my_shift = false
        // this.$('.col-discount').keydown(function(event){
        //      var keyCode = event.keyCode || event.which;
        //      if (keyCode == 13){ //INTRO TAB
        //         //  Añadir nueva linea o cambiar el foco a la de abajo si la hubiera
        //          var selected_line = self.order.selected_orderline;
        //          if (selected_line){
        //              var n_line = selected_line.get('n_line');
        //              if (n_line == self.order_widget.orderlinewidgets.length){
        //                  $('.add-line-button').click()
        //              }
        //              else{
        //                  var next_line = self.order_widget.orderlinewidgets[n_line]
        //                  if(next_line){
        //                 //    self.order.selectLine(next_line.model);
        //                    next_line.$el.find('.col-code').focus();
        //                  }
        //              }
        //          }
        //      }
        // });
    },
    renderElement: function() {
        var self=this;
        this._super();
        this.$el.unbind()
        // this.$el.click(_.bind(this.click_handler, this));
        if(this.model.is_selected()){
            this.$('.col-nline').addClass('selected');
            // this.$el.addClass('selected');
        }
        // Si el campo se rellena con autocomplete se debe usar blur
        this.$('.col-code').blur(_.bind(this.set_value, this, 'code'));
        this.$('.col-code').focus(_.bind(this.click_handler, this, 'code'));

        this.$('.col-product').blur(_.bind(this.set_value, this, 'product'));
        this.$('.col-product').focus(_.bind(this.click_handler, this, 'product'));

        this.$('.col-product_uos_qty').change(_.bind(this.set_value, this, 'product_uos_qty'));
        this.$('.col-product_uos_qty').focus(_.bind(this.click_handler, this, 'product_uos_qty'));

        this.$('.col-product_uos').blur(_.bind(this.set_value, this, 'product_uos'));
        this.$('.col-product_uos').focus(_.bind(this.click_handler, this, 'product_uos'));

        this.$('.col-price_udv').change(_.bind(this.set_value, this, 'price_udv'));
        this.$('.col-price_udv').focus(_.bind(this.click_handler, this, 'price_udv'));

        this.$('.col-qty').change(_.bind(this.set_value, this, 'qty'));
        this.$('.col-qty').focus(_.bind(this.click_handler, this, 'qty'));

        this.$('.col-unit').blur(_.bind(this.set_value, this, 'unit'));
        this.$('.col-unit').focus(_.bind(this.click_handler, this, 'unit'));

        this.$('.col-qnote').blur(_.bind(this.set_value, this, 'qnote'));
        this.$('.col-qnote').focus(_.bind(this.click_handler, this, 'qnote'));

        this.$('.col-qty').change(_.bind(this.set_value, this, 'qty'));
        this.$('.col-qty').focus(_.bind(this.click_handler, this, 'qty'));

        this.$('.col-pvp').change(_.bind(this.set_value, this, 'pvp'));
        this.$('.col-pvp').focus(_.bind(this.click_handler, this, 'pvp'));

        this.$('.col-discount').blur(_.bind(this.set_value, this, 'discount'));
        this.$('.col-discount').focus(_.bind(this.click_handler, this, 'discount'));

        this.$('.col-total').change(_.bind(this.set_value, this, 'total'));
        this.$('.col-total').focus(_.bind(this.click_handler, this, 'total'));

        this.$('.col-detail').change(_.bind(this.set_value, this, 'detail'));
        this.$('.col-detail').focus(_.bind(this.click_handler, this, 'detail'));

        // Mapeo de teclas para moverse por la tabla con las flechas
        this.control_arrow_keys()
        // Creamos nueva linea al tabular la última columna de descuento

        if(this.model.get('product')){
            var uos = [];
            var product_id = this.ts_model.db.product_name_id[this.model.get('product')]
            var product_obj = this.ts_model.db.product_by_id[product_id]
            if(product_obj.base_use_sale){
                uos.push(product_obj.log_base_id[1]);
            }
            if(product_obj.unit_use_sale){
                uos.push(product_obj.log_unit_id[1]);
            }
            if(product_obj.box_use_sale){
                uos.push(product_obj.log_box_id[1]);
            }
            // self.$('.col-product_uos').autocomplete({
            //     source: uos
            // });
            for (unit in uos){
                dic = {
                    value: uos[unit],
                    text: uos[unit],
                }
                if (uos[unit] == self.model.get('product_uos')){
                    dic['selected'] =  "selected"
                }
                self.$('.col-product_uos').append($('<option>',dic))
            }
        }
       //autocomplete products and units from array of names
        var products_ref = this.ts_model.get('products_codes')

        this.$('.col-code').autocomplete({
            source: products_ref,
        });
        var product_names = this.ts_model.get('products_names')
        this.$('.col-product').autocomplete({
            source: product_names,
        });
        console.log("ACTUALIZADO LINEA PRODUCTOS")
        console.log(product_names)
        /*this.$('.col-unit').autocomplete({
            source:this.ts_model.get('units_names')
        });*/
        this.$('.col-qnote').autocomplete({
            source:this.ts_model.get('qnotes_names')
        });


    },
    set_value: function(key) {
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
    update_stock_product: function(product_id){
        var self=this;
        var domain = [['id', '=', product_id]]
        var loaded = self.ts_model.fetch('product.product',
                                        ['name','product_class','list_price','standard_price','default_code','uom_id', 'log_base_id', 'log_base_discount', 'log_unit_discount','log_box_discount', 'log_unit_id', 'log_box_id', 'base_use_sale', 'unit_use_sale', 'box_use_sale','virtual_stock_conservative','taxes_id', 'weight', 'kg_un', 'un_ca', 'ca_ma', 'ma_pa', 'max_discount', 'category_max_discount', 'product_tmpl_id','products_substitute_ids'],
                                        domain
                                        )
            .then(function(products){
                self.ts_model.db.add_products(products);
                // TODO FALTA REPETIR LO MISMO QUE EN EL MODELS???
            })
        return loaded
    },
    call_product_id_change: function(product_id){
        var self = this;
        $.when( self.update_stock_product(product_id) ).done(function(){
            var customer_id = self.ts_model.db.partner_name_id[self.order.get('partner')];
            var pricelist_id = (self.ts_model.db.get_partner_by_id(customer_id)).property_product_pricelist;
            var model = new Model("sale.order.line");
            // model.call("product_id_change_with_wh",[[],pricelist_id,product_id])
            model.call("ts_product_id_change", [product_id, customer_id])
            .then(function(result){
                var product_obj = self.ts_model.db.get_product_by_id(product_id);
                var uom_obj = self.ts_model.db.get_unit_by_id(product_obj.uom_id[0])
            
                self.model.set('code', product_obj.default_code || "");
                self.model.set('product', product_obj.name || "");
                self.model.set('taxes_ids', result.tax_id || []); //TODO poner impuestos de producto o vacio
                self.model.set('unit', self.model.ts_model.db.unit_by_id[result.product_uom].name);
                self.model.set('qty', result.product_uom_qty);
                self.model.set('pvp', self.ts_model.my_round( result.price_unit));
               
                // COMENTADO PARA QUE NO SAQUE EL AVISO SIEMPRE
                // if ( (1 > product_obj.virtual_stock_conservative) && (product_obj.product_class == "normal")){
                //     alert(_t("You want sale 1 " + " " + product_obj.uom_id[1] + " but only " +  product_obj.virtual_stock_conservative + " available."))
                //     var new_qty = (product_obj.virtual_stock_conservative < 0) ? 0.0 : product_obj.virtual_stock_conservative
                //     self.model.set('qty', new_qty);
                //     self.refresh();
                // }
                var subtotal = self.model.get('pvp') * self.model.get('qty') * (1 - self.model.get('discount') / 100.0)
                self.model.set('total', self.ts_model.my_round(subtotal || 0,2));
                self.refresh();
                self.$('.col-product_uos_qty').focus()
                self.$('.col-product_uos_qty').select()

            });
        })
        .fail(function(){
            // alert(_t("NOT WORKING"));
        })
    },
    perform_onchange: function(key) {
        var self=this;
        var value = this.$('.col-'+key).val();
        // if (!value) {
        //   return;
        //   alert(_t("Value mustn't be empty"));
        //   value = 1.0;
        // }

        switch (key) {
            case "code":
                // comprobar que clave está en el array
                var product_id = this.ts_model.db.product_code_id[value];
                if (!product_id){
                    alert(_t("Product code '" + value + "' does not exist"));
                    this.model.set('code', "");
                    this.model.set('product', "");
                    this.model.set('product_uos_qty', 0.0);
                    this.refresh('product_uos_qty');
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
                    this.refresh('product_uos_qty');
                    break;
                }
                this.call_product_id_change(product_id);
                break;

            // case "qty":
            //     var prod_name = this.$('.col-product').val();
            //     var product_id = this.ts_model.db.product_name_id[prod_name];
            //     if (!product_id){
            //         alert(_t("Product name '" + prod_name + "' does not exist"));
            //         this.model.set('qty', "1");
            //         this.refresh();
            //         break;
            //     }
            //     var uom_name = this.$('.col-unit').val();
            //     var uom_id = this.ts_model.db.unit_name_id[uom_name];
            //     if (!uom_id){
            //         alert(_t("Unit of measure '" + uom_name + "' does not exist"));
            //         this.model.set('qty', 1);
            //         this.refresh();
            //         break;
            //     }
            //     var product_obj = this.ts_model.db.get_product_by_id(product_id);
            //     if ( (value > product_obj.virtual_stock_conservative) && (product_obj.product_class == "normal")){
            //         alert(_t("You want sale " + value + " " + uom_name + " but only " +  product_obj.virtual_stock_conservative + " available."))
            //         var new_qty = (product_obj.virtual_stock_conservative < 0) ? 0.0 : product_obj.virtual_stock_conservative
            //         this.model.set('qty', new_qty);
            //         this.refresh();
            //         break;
            //     }
            //
            //     //change weight
            //     var weight =  this.model.get('weight')
            //     this.model.set('weight', self.ts_model.my_round(value * weight,2));
            //     this.refresh();
            //     break;

            case "product_uos_qty":
                var prod_name = this.$('.col-product').val();
                if(prod_name == ""){
                  alert(_t("Product is not selected"));
                }
                else{
                  if(!value){
                    alert(_t("Value mustn't be empty"));
                    value = 1.0;
                  }
                  else{
                    var uos_name = this.$('.col-product_uos').val();
                    conv = this.getUnitConversions(prod_name, value, uos_name)
                    log_unit = this.getUomLogisticUnit(prod_name)
                    this.model.set('product_uos_qty', self.ts_model.my_round(value, 4));
                    this.model.set('qty', self.ts_model.my_round(conv[log_unit], 4));
                    // Se calculan las cajas
                    var boxes = 0.0
                    var product_id = this.ts_model.db.product_name_id[prod_name];
                    var product_obj = this.ts_model.db.get_product_by_id(product_id);
                    if(value < product_obj.virtual_stock_conservative){
                        var uos_id = this.ts_model.db.unit_name_id[uos_name];
                        if(uos_id == product_obj.log_base_id[0]){
                            boxes = (value / product_obj.kg_un) / product_obj.un_ca
                        }
                        else if(uos_id == product_obj.log_unit_id[0]){
                            boxes = value / product_obj.un_ca
                        }
                        else if(uos_id == product_obj.log_box_id[0]){
                            boxes = value
                        }
                        this.model.set('boxes', self.ts_model.my_round(boxes, 4));
                        $('#stock-info').removeClass('warning-red');
                    }
                    else{
                        alert(_t("Value must be lower than Stock"));
                        $('#stock-info').addClass('warning-red');
                        this.refresh();
                    }
                  this.refresh('product_uos');
                  }
                }
                break;
            case "price_udv":
                var prod_name = this.$('.col-product').val();
                if(prod_name == ""){
                    alert(_t("Product is not selected"));
                }
                else{
                  if(!value){
                    alert(_t("Value mustn't be empty"));
                    value = 0.0;
                  }
                  else{
                    var uos_name = this.$('.col-product_uos').val();
                    var uom_pu = this.getUomUosPrices(prod_name, uos_name, 0, value)
                    this.model.set('price_udv', self.ts_model.my_round(value, 2));
                    this.model.set('pvp', self.ts_model.my_round(uom_pu, 2));
                    // this.refresh('pvp');
                  }
                }
                break;
            case "pvp":
                var prod_name = this.$('.col-product').val();
                if(prod_name == ""){
                  alert(_t("Product is not selected"));
                }
                else{
                  if(!value){
                    alert(_t("Value mustn't be empty"));
                    value = 0.0;
                  }
                  else{
                    var uos_name = this.$('.col-product_uos').val();
                    uos_pu = this.getUomUosPrices(prod_name, uos_name,  value)
                    this.model.set('price_udv', self.ts_model.my_round(uos_pu, 2));
                    this.model.set('pvp', self.ts_model.my_round(value, 2));
                    // this.refresh('discount');
                  }
                }
                break;

            // case "product_uos":
            //     this.model.set('product_uos', value);
            //     this.refresh();
            //     break;
            // case "unit":
            //     this.model.set('unit', value);
            //     this.refresh();
            //     break;
            // case "qnote":
            //     var qnote_id = this.ts_model.db.qnote_name_id[value]
            //     if (!qnote_id){
            //         alert(_t("Qnote name '" + value + "' does not exist"));
            //         this.model.set('qnote', "");
            //         this.refresh();
            //         break;
            //     }
            //     var qnote_obj = this.ts_model.db.get_qnote_by_id(qnote_id);
            //     this.model.set('qnote', qnote_obj.code);
            //     this.refresh();
            //     break;
            // case "detail":
            //     this.model.set('detail', value);
            //     this.refresh();
            //     break;
            case "discount":
                var prod_name = this.$('.col-product').val();
                if(prod_name == ""){
                  alert(_t("Product is not selected"))
                }
                else{
                  if(!value){
                    alert(_t("Value mustn't be empty"));
                    value = 0;
                  }
                  else{
                    this.model.set('discount', value);
                    if (this.model.get('n_line') == this.order_widget.orderlinewidgets.length){
                        this.refresh('code');
                    }
                  }
                }
                break;
        }
    },
    refresh: function(focus_key){
        var price = this.model.get("pvp")
        var qty = this.model.get("qty")
        var disc = this.model.get("discount")
        var subtotal = price * qty * (1 - (disc/ 100.0))
        this.model.set('total',subtotal);

        this.renderElement();
        //Añadir color rojo al descuento en caso de superar el máximo
        if(this.model.get('product')){
            var product_id = this.ts_model.db.product_name_id[this.model.get('product')]
            var product_obj = this.ts_model.db.product_by_id[product_id]
            var max_discount = 0.0

            if(product_obj.max_discount){
              max_discount = product_obj.max_discount
            }
            else{
              max_discount = product_obj.category_max_discount || 0.0
            }
            if (max_discount){
                if(disc > max_discount){
                  this.$('.col-discount').addClass('warning-red')
                }
            }
        }
        this.$('.col-'+ focus_key).focus()
        // this.trigger('order_line_refreshed');
    },
});


var OrderWidget = TsBaseWidget.extend({
        template:'Order-Widget',
        init: function(parent, options) {
            this._super(parent,options);
            this.ts_model.bind('change:selectedOrder', this.change_selected_order, this);
            this.bind_orderline_events();
            this.orderlinewidgets = [];
        },
        check_customer_get_id: function(){
            var client_name = this.ts_model.get('selectedOrder').get('partner')
            var client_id = this.ts_model.db.partner_name_id[client_name];
            if (!client_id){
                // alert(_t('No customer defined'));
                return false
            }
            else{
                return client_id
            }
        },
        change_selected_order: function() {
            this.currentOrderLines.unbind();
            this.bind_orderline_events();
            this.renderElement();
        },
        bind_orderline_events: function() {
            this.currentOrderLines = (this.ts_model.get('selectedOrder')).get('orderLines');
            this.currentOrderLines.bind('add', this.renderElement, this);
            this.currentOrderLines.bind('remove', this.renderElement, this);
        },
        show_client: function(){//"SIGIENTE LINEA"
            var client_id = this.check_customer_get_id()
            if (client_id){
                context = new instance.web.CompoundContext()
                var pop = new instance.web.form.FormOpenPopup(this);
                pop.show_element('res.partner',client_id,context,
                    {target:'new',
                     title: "Ver Cliente",
                     readonly: true,
               })

            }
            else{
              alert(_t('You must select a customer'));
            }
        },
        show_product: function(product_id){
            if (product_id){
                context = new instance.web.CompoundContext()
                var pop = new instance.web.form.FormOpenPopup(this);
                pop.show_element('product.product',product_id,context,
                    {target:'new',
                     title: "Ver Producto",
                     readonly: true,
               })
            }
        },
        renderElement: function () {
            var self = this;
            this._super();
            // #  Habría que hacer unbind??
            this.$('.add-line-button').click(function(){
                var order =  self.ts_model.get('selectedOrder')
                var partner_id = self.ts_model.db.partner_name_id[order.get('partner')]
                if (!partner_id){
                    alert(_t('Please select a customer before adding a order line'));
                    $('#partner').focus();
                }else{
                    self.ts_model.get('selectedOrder').addLine();
                    var added_line = self.ts_model.get('selectedOrder').getLastOrderline();
                    self.ts_model.get('selectedOrder').selectLine(added_line);
                    self.orderlinewidgets[self.orderlinewidgets.length - 1].$el.find('.col-code').focus(); //set focus on line when we add one
                }
            });
            this.$('.remove-line-button').click(function(){
                self.ts_model.get('selectedOrder').removeLine();
                var selected_line = self.ts_model.get('selectedOrder').getSelectedLine();
                if (selected_line){
                    n_line = selected_line.get('n_line')
                    self.orderlinewidgets[n_line-1].$el.find('.col-code').focus();
                }

            });
            this.$('#ult-button').click(function(){
                var client_id = self.check_customer_get_id();
                if (client_id){
                    $.when(self.ts_model.get('selectedOrder').get_last_line_by('ult', client_id))
                        .done(function(){
                            // self.bind_orderline_events(); //in get_last_order_lines we unbid add event of currentOrderLines to render faster
                            // self.renderElement();
                            // self.ts_widget.new_order_screen.totals_order_widget.changeTotals();
                        })
                        .fail(function(){
                            alert(_t("NOT WORKING"));
                        })
                }
            });
            this.$('#vua-button').click(function(){
                var client_id = self.check_customer_get_id();
                if (client_id){
                    $.when(self.ts_model.get('selectedOrder').get_last_line_by('year', client_id))
                        .done(function(){
                            // self.bind_orderline_events(); //in get_last_line_by we unbid add event of currentOrderLines to render faster
                            // self.renderElement();
                            // self.ts_widget.new_order_screen.totals_order_widget.changeTotals();

                        })
                        .fail(function(){
                            alert(_t("NOT WORKING"));
                        })
                }
            });
            this.$('#so-button').click(function(){
                var client_id = self.check_customer_get_id();
                if (client_id){
                    $.when(self.ts_model.get('selectedOrder').get_last_line_by('3month', client_id))
                        .done(function(){
                            // self.bind_orderline_events(); //in get_last_line_by we unbid add event of currentOrderLines to render faster
                            // self.renderElement();
                            // self.ts_widget.new_order_screen.totals_order_widget.changeTotals();
                        })
                        .fail(function(){
                            alert(_t("NOT WORKING"));
                        })
                }
            });
            this.$('#promo-button').click(function(){
//                var current_order = self.ts_model.get('selectedOrder')
//                current_order.set('set_promotion', true)
//                self.ts_widget.new_order_screen.totals_order_widget.saveCurrentOrder()
//                $.when( self.ts_model.ready2 )
//                .done(function(){
//                var loaded = self.ts_model.fetch('sale.order',
//                                                ['id', 'name'],
//                                                [
//                                                    ['chanel', '=', 'telesale']
//                                                ])
//                    .then(function(orders){
//                        if (orders[0]) {
//                        var my_id = orders[0].id
//                        $.when( self.load_order_from_server(my_id) )
//                        .done(function(){
//                        });
//
//                      }
//                    });
//                 });
            alert("Esta funcionalidad está desabilitada. Las promociones se aplicarán cuando confirmes el pedido")
            });
             this.$('#sust-button').click(function(){
                var current_order = self.ts_model.get('selectedOrder')
                var selected_line = current_order.selected_orderline;
                if (!selected_line){
                    alert(_t("You must select a product line."));
                }else{
                    var product_id = self.ts_model.db.product_name_id[selected_line.get('product')];
                    if (!product_id){
                        alert(_t("This line has not a product defined."));
                    }
                    else{
                        var product_obj = self.ts_model.db.get_product_by_id(product_id);
                        if ($.isEmptyObject(product_obj.products_substitute_ids))
                            alert(_t("This product have not substitutes"));
                        else{
                            self.ts_model.set('sust_products', []);
                            for (key in product_obj.products_substitute_ids){
                                var sust_id = product_obj.products_substitute_ids[key];
                                var sust_obj = self.ts_model.db.get_product_by_tmp_id(sust_id);
                                self.ts_model.get('sust_products').push(sust_obj)
                            }
                            self.ts_widget.screen_selector.show_popup('product_sust_popup', false);
                        }
                    }
                }

            });
            this.$('#info-button').click(function(){
                var current_order = self.ts_model.get('selectedOrder')
                var selected_line = current_order.selected_orderline;
                if (!selected_line){
                    alert(("You must select a product line."));
                }else{
                    var product_id = self.ts_model.db.product_name_id[selected_line.get('product')];
                    if (!product_id){
                        alert(_t("This line has not a product defined."));
                    }
                    else{
                        self.show_product(product_id)
                    }
                }
            });
            this.$('#show-client').click(function(){

                self.show_client();
            });
            for(var i = 0, len = this.orderlinewidgets.length; i < len; i++){
                this.orderlinewidgets[i].destroy();
            }
            this.orderlinewidgets = [];

            var $content = this.$('.orderlines');
            // var $content = this.$('#effective-append'); #TODO NO CREO QUE SEA POSIBLE POR LO DE ELIMINAR
            var nline = 1
            this.currentOrderLines.each(_.bind( function(orderLine) {
                orderLine.set('n_line', nline++);
                var line = new OrderlineWidget(this, {
                    model: orderLine,
                    order: this.ts_model.get('selectedOrder'),
                });
                // line.on('order_line_selected', self, self.order_line_selected);
                // line.on('order_line_refreshed', self, self.order_line_refreshed);
                line.appendTo($content);
                self.orderlinewidgets.push(line);
            }, this));

        },
        order_line_selected: function(){
        },
        order_line_refreshed: function(){
        },
        load_order_from_server: function(order_id){
            var self=this;
          //  if (!flag){
              //  this.ts_model.get('orders').add(new models.Order({ ts_model: self.ts_model}));
            //}
            this.open_order =  this.ts_model.get('selectedOrder')
            var loaded = self.ts_model.fetch('sale.order',
                                            ['supplier_id','contact_id','note','comercial','customer_comment','client_order_ref','name','partner_id','date_order','state','amount_total','date_invoice', 'date_planned', 'date_invoice'],
                                            [
                                                ['id', '=', order_id]
                                            ])
                .then(function(orders){
                    var order = orders[0];
                    self.order_fetch = order;
                    return self.ts_model.fetch('sale.order.line',
                                                ['product_id','product_uom','product_uom_qty','product_uos', 'product_uos_qty','price_udv','price_unit','price_subtotal','tax_id','pvp_ref','current_pvp', 'q_note', 'detail_note', 'discount'],
                                                [
                                                    ['order_id', '=', order_id],
                                                 ]);
                }).then(function(order_lines){
                        self.ts_model.build_order(self.order_fetch, self.open_order, order_lines); //build de order model
                        self.ts_widget.new_order_screen.data_order_widget.refresh();
                })
            return loaded
        },
    });   

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
            this.selected_line.unbind('change:weight');
            this.selected_line.unbind('change:boxes');
            this.selected_line.bind('change:total', this.changeTotals, this);
            this.selected_line.bind('change:weight', this.changeTotals, this);
            this.selected_line.bind('change:boxes', this.changeTotals, this);
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
        },
        changeTotals: function(){
            var self = this;
            // TODO A VEER
            // this.base = 0;
            // this.discount = 0;
            // this.margin = 0;
            // this.weight = 0;
            // this.iva = 0;
            // this.total = 0;
            // this.pvp_ref = 0;
            // this.sum_cost = 0;
            // this.sum_box = 0;
            // this.sum_fresh = 0;
            // (this.currentOrderLines).each(_.bind( function(line) {
            //     var product_id = self.ts_model.db.product_name_id[line.get('product')]
            //     if (product_id){
            //         var product_obj = self.ts_model.db.get_product_by_id(product_id)
            //         // if (product_obj.product_class == 'normal'){
            //           self.sum_cost += product_obj.standard_price * line.get('qty');
            //           self.sum_box += line.get('boxes');
            //           self.weight += line.get('weight');
            //         //   self.discount += line.get('pvp_ref') != 0 ? (line.get('pvp_ref') - line.get('pvp')) * line.get('qty') : 0;
            //           self.discount += line.get('qty') * line.get('pvp') * (line.get('discount') / 100)
            //           var price_disc = line.get('pvp') * (1 - (line.get('discount') / 100))
            //           self.margin += (price_disc -  product_obj.standard_price) * line.get('qty');
            //           self.pvp_ref += line.get('pvp_ref') * line.get('qty');
            //           self.base += line.get_price_without_tax('total');
            //           self.iva += line.get_tax();
            //           // self.total += line.get_price_with_tax();
            //           // self.margin += (line.get('pvp') - product_obj.standard_price) * line.get('qty');
            //         // }
            //         // else{
            //         //     self.sum_fresh += line.get_price_without_tax('total');
            //         // }

            //     }
            // }, this));
            // self.total += self.ts_model.my_round(self.base, 2) + self.ts_model.my_round(self.iva, 2);
            // self.base = self.ts_model.my_round(self.base, 2);
            // this.order_model.set('total_base',self.base);
            // this.order_model.set('total_iva', self.iva);
            // this.order_model.set('total', self.total);
            // this.order_model.set('total_weight', self.weight);
            // this.order_model.set('total_discount', self.discount);
            // var discount_per = (0) + "%";
            // // if (self.pvp_ref != 0){
            // //     var discount_num = (self.discount/self.pvp_ref) * 100 ;
            // //     if (discount_num < 0)
            // //         var discount_per = "+" + self.ts_model.my_round( discount_num * (-1) , 2).toFixed(2) + "%";
            // //     else
            // //         var discount_per = self.ts_model.my_round( discount_num , 2).toFixed(2) + "%";
            // // }
            // if (self.base != 0){
            //   // Le volvemos a sumamos el descuento porque la base viene sin el
            //     var discount_num = (self.discount/(self.base + self.discount) ) * 100 ;
            //     if (discount_num < 0)
            //         var discount_per = "+" +  discount_num * (-1)  + "%";
            //     else
            //         var discount_per =  discount_num.toFixed(2)  + "%";
            // }
            // this.order_model.set('total_discount_per', discount_per);
            // this.order_model.set('total_margin', self.margin);
            // var margin_per = (0) + "%";
            // var margin_per_num = 0
            // if (self.base != 0) {
            //     margin_per_num = ((self.base - self.sum_cost) / self.base) * 100
            //     margin_per = self.ts_model.my_round(margin_per_num, 2).toFixed(2) + "%"
            // }
            // this.order_model.set('total_margin_per', margin_per);
            // this.order_model.set('total_boxes', self.sum_box); //integer
            // this.order_model.set('total_fresh', self.sum_fresh);

            // var min_limit = this.ts_model.get('company').min_limit
            // var min_margin = this.ts_model.get('company').min_margin
            // this.renderElement();
            // if (margin_per_num < min_margin)
            //    this.$('#total_margin').addClass('warning-red');
            // else
            //    $('#total_margin').removeClass('warning-red');
            // if (self.total < min_limit)
            //     $('#total_order').addClass('warning-red');
            // else
            //    $('#total_order').removeClass('warning-red');
        },
        // confirmCurrentOrder: function() {
        //     var currentOrder = this.order_model;
        //     //currentOrder.set('action_button', 'confirm')
        //     currentOrder.set('action_button', 'confirm_background')
        //     // if ( (currentOrder.get('erp_state')) && (currentOrder.get('erp_state') != 'draft') ){
        //     //     alert(_t('You cant confirm an order which state is diferent than draft.'));
        //     // }
        //     // else  if (currentOrder.get('limit_credit')*1 != 0 && currentOrder.get('customer_debt')*1 + currentOrder.get('total')*1 > currentOrder.get('limit_credit')*1){
        //     if (currentOrder.get('limit_credit')*1 != 0 && currentOrder.get('customer_debt')*1 + currentOrder.get('total')*1 > currentOrder.get('limit_credit')*1){
        //             alert(_t('You cant confirm this order because you are exceeding customer limit credit. Please save as draft'));
        //     }
        //    else if ( currentOrder.check() ){
        //         var partner_id = this.ts_model.db.partner_name_id[currentOrder.get('partner')]
        //         delete this.ts_model.db.cache_sold_lines[partner_id];
        //         this.ts_model.push_order(currentOrder.exportAsJSON());
        //     }
        // },
        confirmCurrentOrder: function() {
          var self = this;
            var currentOrder = this.order_model;
            currentOrder.set('set_promotion', true)  // Aplicar promociones al confirmar
            self.saveCurrentOrder()
            $.when( self.ts_model.ready2 )
            .done(function(){
                var loaded = self.ts_model.fetch('sale.order',
                                                ['id', 'name'],
                                                [
                                                    ['chanel', '=', 'telesale']
                                                ])
                    .then(function(orders){
                       console.log('Entro')
                        if (orders[0]) {
                          // var my_id = orders[0].id
                          (new instance.web.Model('sale.order')).call('confirm_order_background',[orders[0].id],{context:new instance.web.CompoundContext()})
                              .fail(function(unused, event){
                                  //don't show error popup if it fails
                                  console.error('Failed confirm order: ',orders[0].name);
                              })
                              .done(function(){
                                    console.log('Confirmado en segundo plano Yeeeeeah');
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
        saveCurrentOrder: function() {
            var currentOrder = this.order_model;
            currentOrder.set('action_button', 'save')
            // if ( (currentOrder.get('erp_state')) && (currentOrder.get('erp_state') != 'draft') ){
            //     alert(_t('You cant save as draft an order which state is diferent than draft.'));
            // }
            // else if ( currentOrder.check() ){
            if ( currentOrder.check() ){
//                this.ts_model.push_order(currentOrder.exportAsJSON());
//               NO HACEMOS QUE PASE POR EL FLUJO DE LA BOLITA ROJA, ESTÁ DESABILITADA
                this.ts_model._flush2(currentOrder.exportAsJSON());
            }
        },

});

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
        this.mark = "";
        this.unit_weight = "";
        this.min_price = "";
        this.margin = "";
        this.discount = "";
        this.max_discount = "";
        this.n_line = "";
        this.class = "";
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
    },
    calcProductInfo: function () {
        var self = this;
        this.selected_line = this.ts_model.get('selectedOrder').get('selected_line');
        if (!this.selected_line.get("product")){
            this.set_default_values();
            this.renderElement();
        }
        // this.selected_line.unbind('change:discount');
        this.selected_line.unbind('change:product');
        // this.selected_line.unbind('change:margin');
        // this.selected_line.bind('change:discount', this.change_discount, this);
        this.selected_line.bind('change:product', this.change_product, this);
        // this.selected_line.bind('change:margin', this.change_margin, this);
        this.selected_line.trigger('change:product');
        // if (this.selected_line){
        //     this.change_discount();
        //     this.change_margin();
        // }

    },
    change_product: function(){
        var self = this;
        // TODO A VER QUE PASA
        // var line_product = this.selected_line.get("product")
        // self.n_line = self.selected_line.get('n_line') + " / " + self.ts_model.get('selectedOrder').get('orderLines').length;
        // if (line_product != ""){
        //     var product_id = this.ts_model.db.product_name_id[line_product]
        //     var partner_name = this.ts_model.get('selectedOrder').get('partner');
        //     var partner_id = this.ts_model.db.partner_name_id[partner_name];
        //     if (product_id && partner_id){
        //         var product_obj = this.ts_model.db.get_product_by_id(product_id)
        //         var partner_obj = this.ts_model.db.get_partner_by_id(partner_id)
        //         var pricelist_id = partner_obj.property_product_pricelist
        //         var model = Model('product.product');
        //         model.call("get_product_info",[product_id,partner_id,pricelist_id],{context:new instance.web.CompoundContext()})
        //             .then(function(result){
        //                 self.stock = self.ts_model.my_round(result.stock,2).toFixed(2);
        //                 self.date = result.last_date != "-" ? self.ts_model.localFormatDate(result.last_date.split(" ")[0]) : "-";
        //                 self.qty = self.ts_model.my_round(result.last_qty,4).toFixed(4);
        //                 self.price = self.ts_model.my_round(result.last_price,2).toFixed(2);
        //                 self.min_price = self.ts_model.my_round(result.min_price,2).toFixed(2);
        //                 self.mark = result.product_mark;
        //                 self.class = result.product_class;
        //                 self.max_discount = self.ts_model.my_round(result.max_discount,2).toFixed(2) + "%";
        //                 self.unit_weight = self.ts_model.my_round(result.weight_unit,2).toFixed(2);
        //                 self.renderElement();
        //             });
        //     }
        //     else{
        //         this.set_default_values();
        //         this.renderElement();
        //     }
        // }
    },
    // change_discount: function(){
    //     var discount = this.selected_line.get('discount');
    //     discount = discount * 100
    //     var discount_str = ""
    //     //check type?
    //     if (discount < 0){
    //         discount = discount * (-1); //remove negative sign
    //         discount_str = "+" + discount.toFixed(2) + "%";
    //     }else{
    //         discount_str = discount.toFixed(2) + "%";
    //     }
    //     this.discount = discount_str
    //     this.renderElement();
    // },
    // change_margin: function(){
    //     var margin = this.selected_line.get('margin');
    //     margin = margin * 100
    //     this.margin = margin.toFixed(2) + "%";
    //     this.renderElement();
    // },
});


var SoldProductLineWidget = TsBaseWidget.extend({
    template:'Sold-Product-Line-Widget',
    init: function(parent, options){
        this._super(parent,options);
        this.sold_line = options.sold_line;
    },

    renderElement: function() {
        var self=this;
        this._super();
        // this.$('#add-line').off("click").click(_.bind(this.add_line_to_order, this));
        this.$('#add-line').off("click").click(_.bind(this.add_product_to_order, this));

    },
    // add_line_to_order: function() {
    //     var self=this;
    //     self.ts_model.get('selectedOrder').add_lines_to_current_order([self.sold_line], true)
    //     //in get_last_order_lines we unbid add event of currentOrderLines to render faster
    //     self.ts_widget.new_order_screen.order_widget.bind_orderline_events();
    //     self.ts_widget.new_order_screen.order_widget.renderElement()
    //     self.ts_widget.new_order_screen.totals_order_widget.changeTotals();
    //
    // },
    add_product_to_order: function() {
        // this.ts_model.get('orders').add(new models.Order({ ts_model: self.ts_model, contact_name: 'aaa' }));
        var self=this;
        var product_id = this.sold_line.product_id[0]
        if (product_id){
            var current_order= this.ts_model.get('selectedOrder')
            current_order.addProductLine(product_id);
            // this.ts_widget.screen_selector.set_current_screen('new_order');
            // $('button#button_no').click();
            // current_order.selectLine(current_order.get('orderLines').last());
        }
    },
});

var SoldProductWidget = TsBaseWidget.extend({
    template:'Sold-Product-Widget',
    init: function(parent, options){
        var self = this;
        this._super(parent,options);
        // TODO ???
        // this.ts_model.get('sold_lines').bind('reset', function(){
            self.renderElement();
        // });
        this.line_widgets = [];
    },

    renderElement: function() {
        var self=this;
        this._super();
        // free subwidgets  memory from previous renders
        // todo lenght undefined
        // for(var i = 0, len = this.line_widgets.length; i < len; i++){
        //     this.line_widgets[i].destroy();
        // }
        this.line_widgets = [];
        // TODO sold lines tiene ahora objetos con info de producto
        // var sold_lines = this.ts_model.get("sold_lines").models || []

        var $lines_content = this.$('.soldproductlines');
        // TODO
        // for (var i=0, len = sold_lines.length; i < len; i++){
        //     var line_obj = sold_lines[i].attributes;
        //     var sold_line = new SoldProductLineWidget(self, {sold_line: line_obj})
        //     this.line_widgets.push(sold_line)
        //     sold_line.appendTo($lines_content)
        // }
    },
});
    return {
        OrderButtonWidget: OrderButtonWidget,
        DataOrderWidget: DataOrderWidget,
        OrderlineWidget: OrderlineWidget,
        OrderWidget: OrderWidget,
        TotalsOrderWidget: TotalsOrderWidget,
        ProductInfoOrderWidget: ProductInfoOrderWidget,
        SoldProductWidget: SoldProductWidget
    }; 

});


