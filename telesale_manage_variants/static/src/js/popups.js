odoo.define('telesale_manage_variants.base_widgets', function (require) {
"use strict";
var BaseWidgets = require('telesale.BaseWidget');

var TsBaseWidget = require('telesale.TsBaseWidget');

var PopUp = require('telesale.PopUps');

var Model = require('web.DataModel');

// Set grid PopUp In 
BaseWidgets.TsWidget.include({
    // Define Grid widget
    build_widgets: function() {
        this.grid_popup = new GridPopUp(this, {});
        this.grid_popup.appendTo(this.$('#content'));
        this._super();
    },

    // Set product name autocomplete
    _get_screen_selector_vals: function() {
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

    get_column_values: function(){
        return this.column_attrs
    },
    
    get_row_values: function(){
        return this.row_attrs
    },
    
    // Get input values from cell and format it to float.
    get_cell_vals: function(cell){
        var qty = this.ts_model.my_str2float( $(cell).find('input.add-qty').val() );
        var price = this.ts_model.my_str2float( $(cell).find('input.add-price').val() );
        var discount = this.ts_model.my_str2float( $(cell).find('input.add-discount').val() );

        var vals = {
            'qty': qty,
            'price': price,
            'discount': discount,
        }
        return vals
    },

    // For each cell add or update a line variant
    add_variants_button: function(){
        var self=this;
        this.$('.grid-cell').each(function(i, cell){
            var line_vals = self.get_cell_vals(cell);
            if (!line_vals.qty){
                return  // Continue to next iteration
            }
            var variant_id = cell.getAttribute('variant-id');
            var line_cid = cell.getAttribute('line-cid');
            
            if (line_cid == ""){
                self.prototipe_add(parseInt(variant_id), line_vals);
            }
            else{
                 self.prototipe_update(line_cid, line_vals);
            }
        });
    },

    // Set the line model with line_vals info
    set_cell_vals: function(line_model, line_vals){
        line_model.set('qty', line_vals.qty);
        line_model.set('pvp', line_vals.price);
        line_model.set('discount', line_vals.discount);
        line_model.update_line_values();
    },

    // Adds a new variant line from the Grid
    prototipe_add: function(variant_id, line_vals){

        var template_line_model = this.line_widget.model;

        // Create new line
        var current_order= this.ts_model.get('selectedOrder');
        var added_line = current_order.addLine();
        var product_obj = this.ts_model.db.get_product_by_id(variant_id)
        var product_name = product_obj.display_name;
        added_line.set('product', product_name);
        added_line.set('unit', product_obj.uom_id[1]);

        // Needed because addProductLine not set add_qty at time.
        this.set_cell_vals(added_line, line_vals);

        // Set line behaviour to a variant
        added_line.mode = 'variant';
        added_line.parent_cid = template_line_model.cid;

        // Update parent_line dictionary with child line
        template_line_model.variant_related_cid[variant_id] = added_line.cid;
    },

    // Update a exiting line from the Grid
    prototipe_update: function(line_cid, line_vals){

        var line_model = this.get_line_model_by_cid(line_cid);
        if (line_model){
            this.set_cell_vals(line_model, line_vals);
        }
    },

    // Get cid from Grid cell
    get_line_cid_related: function(cell){
        var variant_id = cell.id;

        var line_cid = "";
        var template_line_model = this.line_widget.model;
        if (template_line_model.variant_related_cid[variant_id]){
            line_cid = template_line_model.variant_related_cid[variant_id];
        }
        return line_cid;

    },

    // Get an order line by grid cell cid
    get_line_model_by_cid: function(line_cid){
        var current_order = this.ts_model.get('selectedOrder');
        var line_model = current_order.get('orderLines').get({cid: line_cid}); 
        return line_model;
    },

    // If line already exits get line vals from model to the cell
    update_cell: function(cell){
        var updated_cell = cell;
        var line_cid = this.get_line_cid_related(cell);
        updated_cell['line_cid'] = line_cid;
        if (line_cid){
            var line_model = this.get_line_model_by_cid(line_cid);
            if (line_model){
                updated_cell['qty'] = line_model.get('qty') || 0.0
                updated_cell['price'] = line_model.get('pvp') || 0.0
                updated_cell['discount'] = line_model.get('discount') || 0.0
            }
        }
        return updated_cell
    },

    // Structure table with data from server updated, we need to return the updated
    // and linked to orderlines model cell obj
    get_cell_obj: function(col_id, row_id){
        var cell = this.str_table[col_id][row_id]

        return this.update_cell(cell)
    },

    // Load Grid From server
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

    // Renders the witget waiting for callback of the server
    refresh: function(options){
        var self = this;
        this.line_widget = options.line_widget

        var template_obj = this.line_widget.get_template();
        $.when(this.get_grid_from_server(template_obj.id))
        .done(function(){
            self.renderElement();
        });
    },

    // Set behaviour of Button Apply
    renderElement: function(){
        var self = this;
        this._super();
        this.$('#add-variants-button').bind('click', function(event){
            self.add_variants_button();
            self.ts_model.ts_widget.new_order_screen.order_widget.renderElement();
            self.$('#close-filter').click();
        });

        // Cancel button
        this.$('#close-filter').off('click').click(function(){
            self.ts_widget.screen_selector.close_popup('filter_customer_popup');
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

        
    },

    // Render the withget to load info from server each time we show it.
    show: function(line_widget){
        var options = {
            'line_widget': line_widget
        }
        this.grid_widget.refresh(options)
        this._super();
        
    },
});

return {GridWidget: GridWidget}


});



