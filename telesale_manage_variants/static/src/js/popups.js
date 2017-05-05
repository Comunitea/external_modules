odoo.define('telesale_manage_variants.base_widgets', function (require) {
"use strict";
var BaseWidgets = require('telesale.BaseWidget');

var TsBaseWidget = require('telesale.TsBaseWidget');

var PopUp = require('telesale.PopUps');

var Model = require('web.DataModel');

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

        this.column_attrs = [];
        this.row_attrs = [];
        this.str_table = {};

    },
    renderElement: function(){
        var self = this;
        this._super();
        this.$('#add-variants-button').bind('click', function(event){
            self.add_variants_button();
            $('#close-filter').click();
        });
    },
    add_variants_button: function(){
        var self=this;
        this.$('.grid-cell').each(function(i, cell){

            var qty = $(cell).find('input.add-qty').val();
            if (!qty){
                return
            }
            var variant_id = cell.getAttribute('variant-id');
            // var price = $(cell).find('input.add-price').val();
            // var discount = $(cell).find('input.add-discount').val()
            self.prototipe_add(parseInt(variant_id), parseInt(qty));
        })
    },
    prototipe_add: function(variant_id, add_qty){
        debugger;
        if (!add_qty){
            add_qty: 1.0
        }
        var current_order= this.ts_model.get('selectedOrder');
        current_order.addProductLine(variant_id, add_qty, true);
        var added_line = this.ts_model.get('selectedOrder').getLastOrderline();
        added_line.mode = 'variant';
        added_line.parent_cid = this.line_widget.model.cid
        this.ts_model.ts_widget.new_order_screen.order_widget.renderElement();
    },
    get_column_values: function(){
        return this.column_attrs
    },
    get_row_values: function(){
        return this.row_attrs
    },
    get_cell_obj: function(col_id, row_id){
        return this.str_table[col_id][row_id]
    },
    get_grid_from_server: function(template_id){
        self=this;
        var model = new Model("product.template")
        var loaded = model.call("ts_get_grid_structure",[template_id])
        .then(function(result){
            self.column_attrs =result.column_attrs
            self.row_attrs = result.row_attrs
            self.str_table = result.str_table
        });
        return loaded
    },
    refresh: function(options){
        var self = this;
        this.line_widget = options.line_widget
        this.variant_ids = [];
        this.variant_objs = [];
        var template_obj = this.line_widget.get_template();
        for (var i = 0, len = template_obj.product_variant_ids.length; i < len; i++) {
            var variant_id = template_obj.product_variant_ids[i]
            var variant_obj = this.ts_model.db.get_product_by_id(variant_id)
            this.variant_ids.push(variant_id) 
            this.variant_objs.push(variant_obj)
        }
        $.when(this.get_grid_from_server(template_obj.id))
        .done(function(){
            self.renderElement();
        });
    },

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



