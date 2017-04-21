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
            add_qty = 1.0
        }
        if (product_id){
            var current_order= this.ts_model.get('selectedOrder')
            add_qty = this.ts_model.my_round(add_qty,2);
            current_order.addProductLine(product_id, add_qty);
            // $('button#button_no').click();
        }
    },
    renderElement: function() {
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
        /*this.ts_model.get('products').bind('reset', function(){
            self.renderElement();
        });*/
        this.ts_model.bind('change:update_catalog', function(){
            self.renderElement();
        });
        this.ts_model.bind('change:selectedOrder', this.change_selected_order, this);
        this.order_model = this.ts_model.get('selectedOrder');
        this.line_widgets = [];
    },

    change_selected_order: function() {
        console.log('Se dispara el cambio de pedido seleccionado')
        this.order_model.unbind('change:partner');
        this.order_model = this.ts_model.get('selectedOrder');
    },
    renderElement: function () {
        var self = this;
        this._super();
        // free subwidgets  memory from previous renders
        for(var i = 0, len = this.line_widgets.length; i < len; i++){
            this.line_widgets[i].destroy();
        }
        // TODO DESCOMENTAR
        this.line_widgets = [];
        var products = this.ts_model.get("products").models || [];
        var my_len = products.length;
        if (my_len > 20){
            my_len = 20
        }
        for (var i = 0, len = my_len; i < len; i++){
            var product_obj = products[i].attributes;
            var product_line = new ProductLineWidget(self, {product: product_obj})
            this.line_widgets.push(product_line);
            product_line.appendTo(self.$('.productlines'));
        }
    },
});

return {
    ProductCatalogWidget: ProductCatalogWidget,
    ProductLineWidget: ProductLineWidget
}
});
