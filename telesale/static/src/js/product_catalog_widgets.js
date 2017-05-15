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
    add_product_to_order: function() {
        var product_id = this.product.id
        var add_qty = this.$('#add-qty').val();

        if (isNaN(add_qty)){
            alert(_t(add_qty + " is not a valid number"));
            add_qty = 0.0
        }
        if (product_id){
            var current_order= this.ts_model.get('selectedOrder')
            add_qty = this.ts_model.my_round(add_qty,2);
            current_order.addProductLine(product_id, add_qty);
        }
    },
    renderElement: function() {
        // debugger;
        var self=this;
        this._super();
        this.$('.show-product').click(_.bind(this.show_product_info, this));
        this.$('.add-product').click(_.bind(this.add_product_to_order, this));
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
        var loaded = model.call("ts_search_products", [product_name])
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

    renderElement: function () {
        var self = this;
        this._super();
        this.$('#search-product-button').click(function (){ self.searchProducts() });
        var $lines_contennt = this.$('.productlines');
        for (var key in this.catalog_products){
            var product_obj = self.catalog_products[key];
            var product_line = new ProductLineWidget(self, {product: product_obj})
            product_line.appendTo($lines_contennt);
        }
    },
});

return {
    ProductCatalogWidget: ProductCatalogWidget,
    ProductLineWidget: ProductLineWidget
}
});
