odoo.define('telesale.ProductCatalog', function (require) {
"use strict";

var TsBaseWidget = require('telesale.TsBaseWidget');
var models = require('telesale.models');
var Model = require('web.DataModel');
var core = require('web.core');
var _t = core._t;


var ProductLineWidget = TsBaseWidget.extend({
    template:'Product-Line-Widget',
    init: function(parent, options){
        this._super(parent,options);
        this.product = options.product;
        this.line_cid = "";
    },

    show_product_info: function() {
        var product_id = this.product.id
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
    get_line_cid_related: function(product){
        var line_cid = "";
        var product_id = product.id;
        var product_id = product.id;
        var order_lines = this.ts_model.get('selectedOrder').get('orderLines').models;
        for (var key in order_lines){
            var line_model = order_lines[key];
            var product_name = line_model.get('product')
            var line_product_id = this.ts_model.db.product_name_id[product_name]
            if (line_product_id && line_product_id == product.id)
                line_cid = line_model.cid;
        }
        return line_cid;

    },
    get_line_model_by_cid: function(line_cid){
        var current_order = this.ts_model.get('selectedOrder');
        var line_model = current_order.get('orderLines').get({cid: line_cid}); 
        return line_model;
    },
    update_product: function(product){
        var updated_product = product;
        var line_cid = this.get_line_cid_related(product);
        updated_product['line_cid'] = line_cid;
        var taxes_str = product.tax_ids.map(String).join();
        updated_product['taxes'] = taxes_str;
        if (line_cid){
            var line_model = this.get_line_model_by_cid(line_cid);
            if (line_model){
                updated_product['qty'] = line_model.get('qty') || 0.0;
                updated_product['price'] = line_model.get('pvp') || 0.0;
            }
        }
        return updated_product
    },
    get_product_obj: function(){
        var product = this.product;
        return this.update_product(product);
    },
    control_arrow_keys: function(){
        var self=this;
        this.$('.add-qty').keydown(function(event){
            var keyCode = event.keyCode || event.which;
            if (keyCode == 40) {  // KEY DOWWN
                event.preventDefault();
                ($(this).parent().parent().next().find('.add-qty')).select();

            }
            if (keyCode == 38){ // KEY UP
                event.preventDefault();
                $(this).parent().parent().prev().find('.add-qty').select();
            }
            // else if (keyCode == 37){  // KEY LEFT
            //      $(this).parent().parent().find('.add-price').select();
            // }
            // else if (keyCode == 39){ // KEY RIGHT
            //     $(this).parent().parent().find('.add-price').select();
            // }
        });

        this.$('.add-price').keydown(function(event){
            var keyCode = event.keyCode || event.which;
            if (keyCode == 40) {  // KEY DOWWN (40) 
                event.preventDefault();
                $(this).parent().parent().next().find('.add-price').select();

            }
            else if (keyCode == 38){  //KEY UP
                event.preventDefault();
                $(this).parent().parent().prev().find('.add-price').select();
            }
            // else if (keyCode == 37){  //KEY LEFT
            //      $(this).parent().parent().find('.add-qty').select();
            // }
            //  else if (keyCode == 39){  //KEY LEFT
            //     $(this).parent().parent().find('.add-qty').select();
            // }
        });
    },
    renderElement: function() {
        var self=this;
        this._super();
        this.$('.show-product').click(_.bind(this.show_product_info, this));
        this.control_arrow_keys();
    },
});

var ProductCatalogWidget = TsBaseWidget.extend({
    template:'Product-Catalog-Widget',
    
    init: function(parent, options) {
        var self = this;
        this._super(parent,options);
        this.catalog_products = [];
        this.last_search = "";
        this.page = 1;
        this.result_str = "";
    },

    load_products_from_server: function(product_name, offset){
        var self=this;
        var model = new Model("product.product");
        // Wee need the partner to ger the product price from server.
        var current_order = this.ts_model.get('selectedOrder');
        var partner_id = this.ts_model.db.partner_name_id[current_order.get('partner')];
        var pricelist_id = this.ts_model.db.pricelist_name_id[current_order.get('pricelist')];
        var loaded = model.call("ts_search_products", [product_name, partner_id, pricelist_id, offset])
        .then(function(result){
            self.catalog_products = result['products'];
            self.result_str = result['result_str']
        });
        return loaded;

    },

    searchProducts: function(mode){
        var self=this;
        var product_name = this.$('#search-product').val()
        this.last_search = product_name
        var offset = (this.page - 1) * 100;

        $.when(this.load_products_from_server(product_name, offset))
        .done(function(){
            self.renderElement();
            self.$('#search-product').val(self.last_search)
        })
    },

    get_line_vals: function(line){
        var qty = this.ts_model.my_str2float( $(line).find('#add-qty').val() );
        var price = this.ts_model.my_str2float( $(line).find('#add-price').val() );
        var tax_ids = [];
        var taxes_str =  line.getAttribute('taxes') || ""
        if (taxes_str) {
            var tax_split = taxes_str.split(',');
            var tax_ids = tax_split.map(function(x) { return parseInt(x); });
        }

        var vals = {
            'qty': qty,
            'price': price,
            'discount': 0.0,
            'taxes_ids': tax_ids,
        }
        return vals
    },
    //hook
    get_create_line_vals: function(product_id, catalog_vals, mode){
        return {}
    },
    // Get an order line by grid cell cid
    get_line_model_by_cid: function(line_cid){
        var current_order = this.ts_model.get('selectedOrder');
        var line_model = current_order.get('orderLines').get({cid: line_cid}); 
        return line_model;
    },
    catalog_add_product(product_id, catalog_vals){
        // Create new line, overwrited in telesale_manage_variants
        var added_line = this.ts_widget.new_order_screen.order_widget.create_line_from_vals(product_id, catalog_vals)
        return added_line;
    },

    catalog_update_product(line_cid, line_vals){
        var line_model = this.get_line_model_by_cid(line_cid);
        if (line_model){
            line_model.set('qty', line_vals.qty || 1.0);
            line_model.set('pvp', line_vals.price || 0.0);
        }
    },

    delete_if_empty_line: function(){
        //If selected line is an empty line delete it.
        var order =  this.ts_model.get('selectedOrder')
        var selected_orderline = order.getSelectedLine();
        if(selected_orderline && selected_orderline.get('product') == "" ){
            $('.remove-line-button').click()
        }
    },

    addAllProducts: function(){
        var self=this;
        var order =  this.ts_model.get('selectedOrder')
        var partner_id = this.ts_model.db.partner_name_id[order.get('partner')]
        if (!partner_id){
            alert(_t('Please select a customer before adding a order line'));
            $('#partner').focus();
            return;
        }

        this.delete_if_empty_line();

        this.$('.catalog-line').each(function(i, line){
            var line_vals = self.get_line_vals(line);
            if (!line_vals.qty){
                return  // Continue to next iteration
            }

            var product_id = parseInt( line.getAttribute('product-id') );
            var line_cid = line.getAttribute('line-cid');

            if (line_cid == ""){
                self.catalog_add_product(product_id, line_vals);
            }
            else{
                 self.catalog_update_product(line_cid, line_vals);
            }
        });
    },
    check_float(input_field){
        var value = $(input_field).val();
        if (isNaN(value)){
            alert(value + _t("is not a valid number"));
            $(input_field).val("0.00")
            $(input_field).focus();
            $(input_field).select();
        }
    },
    // Load Grid From server
    call_product_uom_change: function(input_field){
        self=this;
        self.aux_field = input_field
        var model = new Model("sale.order.line")
        var current_order = this.ts_model.get('selectedOrder');
        var partner_id = this.ts_model.db.partner_name_id[current_order.get('partner')];
        var pricelist_id = this.ts_model.db.pricelist_name_id[current_order.get('pricelist')];
        var qty = parseFloat($(input_field).val());
        var product_id = parseInt($(input_field).parent().parent()[0].getAttribute('product-id'))
        return model.call("ts_product_uom_change", [product_id, partner_id, pricelist_id, qty])
        .then(function(result){
            var input_field = self.aux_field
            $(input_field).parent().next().children()[0].value = result.price_unit.toFixed(2);
        });
        return
    },
    bind_onchange_events: function(){
        // this.$('.add-qty').unbind();
        // this.$('.add-price').unbind();
        // this.$('.add-discount').unbind();

        var self=this;
        this.$('.add-qty').bind('change', function(event){
             self.check_float(this);
             self.call_product_uom_change(this);
        });
        this.$('.add-price').bind('change', function(event){
             self.check_float(this);
        });

        this.$('#search-product').keydown(function(event){
            var keyCode = event.keyCode || event.which;
            if (keyCode == 13) {  // key enter pressed
               self.$('#search-product-button').click();
            }
        });
    },

    renderElement: function () {
        var self = this;
        this._super();
        this.$('#search-product-button').click(function (){ 
            self.page = 1;
            self.searchProducts('init') 
        });
        this.$('#search-product-prev').click(function (){
            if (self.page > 1) 
                self.page = self.page - 1;
            self.searchProducts('prev') 
        });
        this.$('#search-product-next').click(function (){ 
            self.page = self.page + 1;
            self.searchProducts('next') 
        });
        this.$('#add-alll-button').click(function (){ self.addAllProducts(); self.ts_model.ts_widget.new_order_screen.order_widget.renderElement(); $('button#button_no').click(); });
        var $lines_contennt = this.$('.productlines');
        for (var key in this.catalog_products){
            var product_obj = self.catalog_products[key];
            var product_line = new ProductLineWidget(self, {product: product_obj})
            product_line.appendTo($lines_contennt);
        }
        this.bind_onchange_events();
    },
});

return {
    ProductCatalogWidget: ProductCatalogWidget,
    ProductLineWidget: ProductLineWidget
}
});
