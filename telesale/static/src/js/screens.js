odoo.define('telesale.Screens', function (require) {
"use strict";

var TsBaseWidget = require('telesale.TsBaseWidget');
var NewOrder = require('telesale.new_order_widgets');
var CustomerList = require('telesale.CustomerList');
var OrderHistory = require('telesale.OrderHistory');
// CMNT MIG: No se usda en Jim
// var SaleHistory = require('telesale.SaleHistory');

var ProductCatalog = require('telesale.ProductCatalog');
var models = require('telesale.models');
var core = require('web.core');
var _t = core._t;

var exports = {}

exports.ScreenSelector = core.Class.extend({
    init: function(options){
        // options is a dict with screens instances passed in build_widgets in TsWidget
        this.screen_set = options.screen_set || {};
        this.popup_set = options.popup_set || {};
        this.default_client_screen = options.default_client_screen;
        this.current_screen = null;
        this.current_popup = null;
        for(var screen_name in this.screen_set){
            this.screen_set[screen_name].hide();
        }
        // Esto ya no funcona en v14
        // Lo sustituyo por el hide
        // for(var popup_name in this.popup_set){
        //     this.popup_set[popup_name].hide();
        // }
    },
    set_current_screen: function(screen_name){
        var new_screen = this.screen_set[screen_name];
        if(!new_screen){
            console.error("ERROR: set_current_screen("+screen_name+") : screen not found");
        }
        if (this.current_screen){
            this.current_screen.hide();
        }
        this.current_screen = new_screen;
        this.current_screen.show();
        },
    set_default_screen: function(){
        this.set_current_screen(this.default_client_screen);
     },
    show_popup: function(name, extra_data){
        if(this.current_popup){
            this.close_popup();
        }
        this.current_popup = this.popup_set[name];
        if (name=="create_reserve_popup"){
            // extra data will be the reserve line widget
            this.current_popup.show(extra_data);
        }
        if (name=="finish_call_popup"){
            // extra data will be the call line widget
            this.current_popup.show(extra_data);
        }
        else{
            this.current_popup.show(extra_data);
        }
        this.current_screen.show();
    },
    close_popup: function(){
        if(this.current_popup){
            this.current_popup.close();
            this.current_popup.hide();
            this.current_popup = null;
        }
    }

});

var ScreenWidget = TsBaseWidget.extend({
    init: function(parent,options){
        this._super(parent,options);
        this.hidden = false;
    },
    show: function(){
        var self = this;
        this.hidden = false;
        if(this.$el){
            this.$el.show();
        }
    },
    hide: function(){
        this.hidden = true;
        if (this.$el){
            this.$el.hide();
        }
    },
    renderElement: function(){
        // we need this because some screens re-render themselves when they are hidden
        // (due to some events, or magic, or both...) we must make sure they remain hidden.
        this._super();
        if(this.hidden){
            if(this.$el){
                this.$el.hide();
            }
        }
    },
});
exports.ScreenWidget = ScreenWidget;

exports.PopUpWidget = TsBaseWidget.extend({
    show: function(){
        if(this.$el){
            this.$el.show();
        }
    },
    close: function(){
    },
    hide: function(){
        if(this.$el){
            this.$el.hide();
        }
    },
});

exports.OrderScreenWidget = ScreenWidget.extend({
    template: 'Order-Screen-Widget',
    init: function(parent,options){
        this._super(parent,options)
        document.title = "Televenta"
    },
    start: function(){
        var self = this;
        this.$('.neworder-button').click(function(){
            self.ts_model.add_new_order();
        });

        this.$('.removeorder-button').click(function(){
            var r = confirm(_t("Sure you want close this order?"));
            if (r)
                self.ts_model.get('selectedOrder').destroy();
        });

        //when a new order is created, add an order button widget.
        this.ts_model.get('orders').bind('add', function(new_order){
            var new_order_button = new NewOrder.OrderButtonWidget(null, {
                order: new_order,
                ts_model: self.ts_model
            });
            new_order_button.appendTo(self.$('#orders'));
            new_order_button.selectOrder();
            var counter = this.ts_model.get('bo_id');
            counter = counter + 1;
            this.ts_model.set('bo_id', counter);
        }, self);



        // Also creates first order when is loaded for dirst time
        this.ts_model.get('orders').add(new models.Order({ ts_model: self.ts_model }));
        this.order_widget= new NewOrder.OrderWidget(this, {});
        this.order_widget.replace(this.$('#placeholder-order-widget'));
        //top part
        this.data_order_widget = new NewOrder.DataOrderWidget(this, {});
        this.data_order_widget.replace(this.$('#placeholder-toppart'));
        //bottom part
        this.totals_order_widget = new NewOrder.TotalsOrderWidget(this, {});
        this.totals_order_widget.replace(this.$('#placeholder-bottompart'));
        //right part
        this.productinfo_order_widget = new NewOrder.ProductInfoOrderWidget(this, {});
        this.productinfo_order_widget.replace(this.$('#placeholder-bottompart-left'));
        this.sold_product_line_widget = new NewOrder.SoldProductWidget(this, {});
        this.sold_product_line_widget.replace(this.$('#placeholder-rightpart'));

    }
});

exports.CustomerListScreenWidget = ScreenWidget.extend({
    template: 'CustomerListScreenWidget',
    init: function(parent,options){
        this._super(parent,options)
    },
    start: function(){
        this.customer_list_widget = new CustomerList.CustomerListWidget(this, {});
        this.customer_list_widget.replace(this.$('#placeholder-customer-list-widget'));
    },
});

exports.ProductCatalogScreenWidget = ScreenWidget.extend({
    template: 'Product-Catalog-Screen-Widget',
    init: function(parent,options){
        this._super(parent,options)
    },
    start: function(){
        var self = this;
        this.product_catalog_widget = new ProductCatalog.ProductCatalogWidget(this, {});
        this.product_catalog_widget.replace(this.$('#placeholder-product-catalog-widget'));
    }
});

exports.OrderHistoryScreenWidget = ScreenWidget.extend({
    template: 'Order-History-Screen-Widget',
    init: function(parent,options){
        this._super(parent,options)
    },
    start: function(){
        this.order_history_widget = new OrderHistory.OrderHistoryWidget(this, {});
        this.order_history_widget.replace(this.$('#placeholder-order-history-widget'));
    },
});

// exports.SaleHistoryScreenWidget = ScreenWidget.extend({
//     template: 'Sale-History-Screen-Widget',
//     init: function(parent,options){
//         this._super(parent,options)
//     },
//     start: function(){
//         this.sale_history_widget = new SaleHistory.SaleHistoryWidget(this, {});
//         this.sale_history_widget.replace(this.$('#placeholder-sale-history-widget'));
//     },
// });

exports.KeyShortsScreenWidget = ScreenWidget.extend({
    template: 'Key-Shorts-Screen-Widget',
    init: function(parent,options){
        this._super(parent,options)
    },
});

return exports;

});
