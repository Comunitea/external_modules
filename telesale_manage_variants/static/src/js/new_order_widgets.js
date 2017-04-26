odoo.define('telesale_manage_variants.new_order_widgets', function (require) {
"use strict";
// var Model = require('web.DataModel');
var NewOrderWidgets = require('telesale.new_order_widgets');
// var core = require('web.core');
// var _t = core._t;

var OrderlineWidget = NewOrderWidgets.OrderlineWidget.include({
    set_input_handlers: function() {
        // Add product templete event handler
        this._super();
        this.$('.col-product-tmpl').blur(_.bind(this.set_value, this, 'product-tmpl'));
        this.$('.col-product-tmpl').focus(_.bind(this.click_handler, this, 'product-tmpl'));
        
        // Events dick seemns not working in the inherit
        var self=this;
        this.$('.open-grid').click(function(){
            self.button_open_grid();
        })
            

    },
    load_input_fields: function() {
        // Set product name autocomplete
        this._super();
        var product_names = this.ts_model.get('template_names')
        this.$('.col-product-tmpl').autocomplete({
            source: function(request, response) {
                var results = $.ui.autocomplete.filter(product_names, request.term);
                response(results.slice(0, 20));
            }
        });
    },
    button_open_grid: function(){
        // Opens Grid PopUp
        this.ts_widget.screen_selector.show_popup('filter_customer_popup', false);
    }
});

});



