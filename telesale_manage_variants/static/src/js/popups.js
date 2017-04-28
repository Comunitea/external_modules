odoo.define('telesale_manage_variants.base_widgets', function (require) {
"use strict";
var BaseWidgets = require('telesale.BaseWidget');

var TsBaseWidget = require('telesale.TsBaseWidget');

var PopUp = require('telesale.PopUps');

// Set grid PopUp In 
BaseWidgets.TsWidget.include({
    build_widgets: function() {
        // Set product name autocomplete
        this.grid_popup = new GridPopUp(this, {});
        this.grid_popup.appendTo(this.$('#content'));
        this._super();
    },
    _get_screen_selector_vals: function() {
    // Set product name autocomplete
        var res = this._super();
        res.popup_set['grid_popup'] = this.grid_popup
        return res
    },
});

// The Grid Widget
var GridWidget = TsBaseWidget.extend({
    template: 'Grid-Widget',
    init: function(parent, options){
        this._super(parent, options);
        this.variant_ids = [];
        this.variant_objs = [];
    },
    renderElement: function(){
        var self = this;
        this._super();
        this.$('.grid-cell').bind('click', function(event){
            self.prototipe_add(parseInt(this.getAttribute('variant-id')));
        });
    },
    prototipe_add: function(variant_id){
        var current_order= this.ts_model.get('selectedOrder');
        current_order.addProductLine(variant_id, 3.69, true);
        var added_line = this.ts_model.get('selectedOrder').getLastOrderline();
        added_line.mode = 'product';

    },
    refresh: function(options){
        this.variant_ids = [];
        this.variant_objs = [];
        var template_obj = options.line_widget.get_template();
        for (var i = 0, len = template_obj.product_variant_ids.length; i < len; i++) {
            var variant_id = template_obj.product_variant_ids[i]
            var variant_obj = this.ts_model.db.get_product_by_id(variant_id)
            this.variant_ids.push(variant_id) 
            this.variant_objs.push(variant_obj)
        }
        this.renderElement();
    }

});


// The Grid Pop Up
var GridPopUp = PopUp.PopUpWidget.extend({
    template: 'Grid-PopUp',
    start: function(){
        var self = this
        // Define Grid Widget
        this.grid_widget = new GridWidget(this, {});
        this.grid_widget.replace(this.$('#placeholder-grid-widget'));

        // Cancel button
        this.$('#close-filter').off('click').click(function(){
            self.ts_widget.screen_selector.close_popup('filter_customer_popup');
        });
    },
    show: function(line_widget){
        var options = {
            'line_widget': line_widget
        }
        this.grid_widget.refresh(options)
        this._super();
        
    },
});



});



