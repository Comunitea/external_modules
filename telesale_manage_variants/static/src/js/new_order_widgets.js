odoo.define('telesale_manage_variants.new_order_widgets', function (require) {
"use strict";
// var Model = require('web.DataModel');
var NewOrderWidgets = require('telesale.new_order_widgets');
var core = require('web.core');
var _t = core._t;

var OrderlineWidget = NewOrderWidgets.OrderlineWidget.include({
    // Add product templete event handler
    set_input_handlers: function() {
        this._super();
        this.$('.col-template').blur(_.bind(this.set_value, this, 'template'));
        this.$('.col-template').focus(_.bind(this.click_handler, this, 'template'));
        
        // Events dick seemns not working in the inherit
        var self=this;
        this.$('.open-grid').click(function(){
            self.button_open_grid();
        });
    },

    // Set template autocomplete
    load_input_fields: function() {
        this._super();
        var product_names = this.ts_model.get('template_names')
        this.$('.col-template').autocomplete({
            source: function(request, response) {
                var results = $.ui.autocomplete.filter(product_names, request.term);
                response(results.slice(0, 20));
            }
        });
    },

    // Get template_obj related with the name in the input field 
    get_template: function(){
        var template_obj = false;
        var value = this.$('.col-template').val();
        var template_id =  this.ts_model.db.template_name_id[value];
        if (template_id){
            template_obj = this.ts_model.db.get_template_by_id(template_id);
        }
        if (!template_obj)
            template_obj = false;
        return template_obj
    },

    // Calls PopUp widget to show the grid
    button_open_grid: function(){
        var template_obj = this.get_template();
        if (!template_obj){
            alert(_t("No template defined to open grid"));
        }
        else{
        // Pase the line widget to grid PopUp
        this.ts_widget.screen_selector.show_popup('grid_popup', this);
        }
    },

    // Get product if only one variant, open grid if more than one variant
    perform_onchange: function(key){
        this._super(key);
        if (key == 'template'){
            var value = this.$('.col-'+key).val();
            // Case name not valid
            var template_obj = this.get_template();
            if (!template_obj){
                var value = this.$('.col-template').val();
                alert(_t("Template name '" + value + "' does not exist"));
                this.model.set('template', "");
                this.model.set('product', "");
                this.model.set('product_uos_qty', 0.0);
                this.refresh('qty');
            }
            else{
                // Get product from model
                if (template_obj.product_variant_count == 1){
                    var product_id = template_obj.product_variant_ids[0];
                    var product_obj = this.ts_model.db.get_product_by_id(product_id)
                    if (product_obj){
                        this.model.set('product', product_obj.display_name);
                        this.call_product_id_change(product_id);
                    }
                }
                // Open the grid
                else{
                    this.button_open_grid();
                }
            }
        }
    }

});

});



