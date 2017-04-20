odoo.define('telesale.PopUps', function (require) {
"use strict";

var TsBaseWidget = require('telesale.TsBaseWidget');
// var NewOrder = require('telesale.new_order_widgets');
// var Summary = require('telesale.CustomerList');
// var OrderHistory = require('telesale.OrderHistory');
// var ProductCatalog = require('telesale.ProductCatalog');
// var models = require('telesale.models');
// var core = require('web.core');
// var _t = core._t;

var exports = {}



var PopUpWidget = TsBaseWidget.extend({
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

var FilterCustomerPopUp = PopUpWidget.extend({
    template: 'Filter-Customer-PopUp',
    init: function(parent,options){
        this._super(parent,options)
    },
    show: function(){
        var self = this;
        this._super();
        this.$('#close-filter').off('click').click(function(){
            self.ts_widget.screen_selector.close_popup('filter_customer_popup');
        })
    }
});

return {FilterCustomerPopUp: FilterCustomerPopUp};

});
