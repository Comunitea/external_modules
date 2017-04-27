odoo.define('telesale_manage_variants.new_order_widgets', function (require) {
"use strict";
// var Model = require('web.DataModel');
var NewOrderWidgets = require('telesale.new_order_widgets');
var core = require('web.core');
var _t = core._t;

var OrderlineWidget = NewOrderWidgets.OrderlineWidget.include({
    set_input_handlers: function() {
        // Add product templete event handler
        this._super();
        this.$('.col-template').blur(_.bind(this.set_value, this, 'template'));
        this.$('.col-template').focus(_.bind(this.click_handler, this, 'template'));
        
        // Events dick seemns not working in the inherit
        var self=this;
        this.$('.open-grid').click(function(){
            self.button_open_grid();
        });
    },
    load_input_fields: function() {
        // Set product name autocomplete
        this._super();
        var product_names = this.ts_model.get('template_names')
        this.$('.col-template').autocomplete({
            source: function(request, response) {
                var results = $.ui.autocomplete.filter(product_names, request.term);
                response(results.slice(0, 20));
            }
        });
    },
    button_open_grid: function(){
        // Opens Grid PopUp
        this.ts_widget.screen_selector.show_popup('grid_popup', this);
    },
    perform_onchange: function(key){
    // Onchange for product template;
        this._super(key);
        if (key == 'template'){
            var value = this.$('.col-'+key).val();
            var template_id = this.ts_model.db.template_name_id[value];
            // Case name not valid
            if (!template_id){
                alert(_t("Template name '" + value + "' does not exist"));
                this.model.set('template', "");
                this.model.set('product', "");
                this.model.set('product_uos_qty', 0.0);
                this.refresh('qty');
            }
            else{
                var template_obj = this.model.get_template();
                if (template_obj.product_variant_count == 1){
                    var product_id = template_obj.product_variant_ids[0];
                    var product_obj = this.ts_model.db.get_product_by_id(product_id)
                    if (product_obj){
                        this.model.set('product', product_obj.display_name);
                        this.call_product_id_change(product_id);
                    }
                }
                else{
                    this.button_open_grid();
                }
            }
        }
    }
});

});



