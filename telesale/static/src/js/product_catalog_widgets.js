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
    // add_product_to_order: function() {
    //     var product_id = this.product.id
    //     var add_qty = this.$('#add-qty').val();

    //     if (isNaN(add_qty)){
    //         alert(_t(add_qty + " is not a valid number"));
    //         add_qty = 0.0
    //     }
    //     if (product_id){
    //         var current_order= this.ts_model.get('selectedOrder')
    //         add_qty = this.ts_model.my_round(add_qty,2);
    //         current_order.addProductLine(product_id, add_qty);
    //     }
    // },
    // Get cid from product line
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
    renderElement: function() {
        var self=this;
        this._super();
        this.$('.show-product').click(_.bind(this.show_product_info, this));
    },
});

var ProductCatalogWidget = TsBaseWidget.extend({
    template:'Product-Catalog-Widget',
    
    init: function(parent, options) {
        var self = this;
        this._super(parent,options);
        this.catalog_products = [];
    },

    load_products_from_server: function(product_name){
        var self=this;
        var model = new Model("product.product");
        // Wee need the partner to ger the product price from server.
        var current_order = this.ts_model.get('selectedOrder');
        var partner_id = this.ts_model.db.partner_name_id[current_order.get('partner')];
        var pricelist_id = this.ts_model.db.pricelist_name_id[current_order.get('pricelist')];
        var loaded = model.call("ts_search_products", [product_name, partner_id, pricelist_id])
        .then(function(result){
            self.catalog_products = result;
        });
        return loaded;

    },

    searchProducts: function(){
        var self=this;
        var product_name = this.$('#search-product').val()
        $.when(this.load_products_from_server(product_name))
        .done(function(){
            self.renderElement();
            self.$('search-product').val(product_name);
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

    addAllProducts: function(){
        var self=this;
        var order =  this.ts_model.get('selectedOrder')
        var partner_id = this.ts_model.db.partner_name_id[order.get('partner')]
        if (!partner_id){
            alert(_t('Please select a customer before adding a order line'));
            $('#partner').focus();
            return;
        }

        //If selected line is an empty line delete it.
        var selected_orderline = order.getSelectedLine();
        if(selected_orderline && selected_orderline.get('product') == "" ){
            $('.remove-line-button').click()
        }

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
    bind_onchange_events: function(){
        this.$('.add-qty').unbind();
        this.$('.add-price').unbind();
        this.$('.add-discount').unbind();

        var self=this;
        this.$('.add-qty').bind('change', function(event){
             self.check_float(this);
        });
        this.$('.add-price').bind('change', function(event){
             self.check_float(this);
        });
        // this.$('.add-discount').bind('change', function(event){
        //      self.check_float(this);
        // });
    },

    renderElement: function () {
        var self = this;
        this._super();
        this.$('#search-product-button').click(function (){ self.searchProducts() });
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
