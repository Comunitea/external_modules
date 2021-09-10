odoo.define('telesale_manage_variants.popups', function (require) {
"use strict";
var BaseWidgets = require('telesale.BaseWidget');

var TsBaseWidget = require('telesale.TsBaseWidget');

var PopUp = require('telesale.PopUps');

// var Model = require('web.DataModel');
var core = require('web.core');
var _t = core._t;

var rpc = require('web.rpc');
var session = require('web.session');

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
        this.aux_field = null; // used in callback funcion

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
        var col_id = $(cell).attr('col-id');
        var row_id = $(cell).attr('row-id');
        var cell_obj = this.get_cell_obj(col_id, row_id)
        var vals = {
            'qty': qty,
            'price': price,
            'discount': discount,
            'tax_ids': cell_obj.tax_ids,
            'enable': cell_obj.enable
        }
        return vals
    },

    prototipe_delete_variant: function(line_cid){
        var line_model = this.get_line_model_by_cid(line_cid)
        if (line_model){
            var current_order = this.ts_model.get('selectedOrder')
            current_order.selectLine(line_model);
            current_order.removeLine();
        }
    },

    // For each cell add or update a line variant
    add_variants_button: function(){
        var self=this;
        this.$('.grid-cell').each(function(i, cell){
            var line_vals = self.get_cell_vals(cell);
            var variant_id = cell.getAttribute('variant-id');
            var line_cid = cell.getAttribute('line-cid');
            if (!line_vals.qty){
                // An existing line is setted to 0, delete it
                if (line_cid != ""){
                    self.prototipe_delete_variant(line_cid);
                }
                return  // Continue to next iteration
            }
            
            if (line_cid == ""){
                self.prototipe_add(parseInt(variant_id), line_vals);
            }
            else{
                 self.prototipe_update(line_cid, line_vals);
            }
        });
    },

    // OVERWRITED IN JIM TELESALE Set the line model with line_vals info
    set_cell_vals: function(line_model, line_vals){
        line_model.set('qty', line_vals.qty);
        line_model.set('pvp', line_vals.price);
        if (!$.isEmptyObject(line_vals.name)){
            line_model.set('description', line_vals.name);
        }
        line_model.set('discount', line_vals.discount);
        line_model.set('taxes_ids', line_vals.tax_ids || []); 
        line_model.update_line_values();
    },

    // Adds a new variant line from the Grid
    prototipe_add: function(variant_id, line_vals){
        var self=this;
        var template_line_model = this.line_widget.model;

        // Create new line
        var added_line = self.ts_widget.new_order_screen.order_widget.create_line_empty(variant_id, true)
        // Needed because addProductLine not set add_qty at time.
        $.when(this.ts_model.get_translated_line_name(variant_id,))
            .done(function(result){
                line_vals['name'] = result
                self.set_cell_vals(added_line, line_vals);


                // Set line behaviour to a variant
                added_line.mode = 'variant';
                added_line.parent_cid = template_line_model.cid;
                // Update parent_line dictionary with child line
                template_line_model.variant_related_cid[variant_id] = added_line.cid;
                // self.ts_model.ts_widget.new_order_screen.order_widget.renderElement();
        })
        .fail(function(unused, event){
            alert('Ocurrió un fallo en al obtener la traducción');
        })
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
        var current_order = this.ts_model.get('selectedOrder');
        var partner_id = this.ts_model.db.partner_name_id[current_order.get('partner')];
        var pricelist_id = this.ts_model.db.pricelist_name_id[current_order.get('pricelist')];
        return rpc.query({model: 'product.template', method: 'ts_get_grid_structure', args:[template_id, partner_id, pricelist_id], kwargs: {context: session.user_context}})
        .then(function(result){
            self.column_attrs =result.column_attrs
            self.row_attrs = result.row_attrs
            self.str_table = result.str_table
        });
        // return loaded
    },

    // Renders the witget waiting for callback of the server
    refresh: function(options){
        var self = this;
        this.line_widget = options.line_widget

        if (this.line_widget){

            
            var template_obj = this.line_widget.get_template();
            $.when(this.get_grid_from_server(template_obj.id))
            .done(function(){
                self.renderElement();
            });
        }
    },

    check_float(input_field){
        var value = $(input_field).val();
        if (isNaN(value)){
            alert(value + _t("is not a valid number"));
            $(input_field).val("0.00")
            $(input_field).focus();
            $(input_field).select();
        }
    },

    // Load Grid From server
    call_product_uom_change: function(input_field){
        self=this;
        self.aux_field = input_field
        var current_order = this.ts_model.get('selectedOrder');
        var partner_id = this.ts_model.db.partner_name_id[current_order.get('partner')];
        var pricelist_id = this.ts_model.db.pricelist_name_id[current_order.get('pricelist')];
        var qty = parseFloat($(input_field).val());
        var product_id = parseInt($(input_field).parent().parent().parent()[0].getAttribute('variant-id'))
        return rpc.query({model: 'sale.order.line', method: 'ts_product_uom_change', args:[product_id, partner_id, pricelist_id, qty], kwargs: {context: session.user_context}})
        .then(function(result){
            var input_field = self.aux_field
            $(input_field).parent().parent().next().children()[1].children[0].value = result.price_unit.toFixed(2)
        });
    },

    bind_onchange_events: function(){
        this.$('.add-qty').unbind();
        this.$('.add-price').unbind();
        this.$('.add-discount').unbind();

        var self=this;
        this.$('.add-qty').bind('change', function(event){
             self.check_float(this);
             self.call_product_uom_change(this);
        });
        this.$('.add-price').bind('change', function(event){
             self.check_float(this);
        });
        this.$('.add-discount').bind('change', function(event){
             self.check_float(this);
        });
    },

    control_arrow_keys: function(){
        var self=this;
        this.$('.add-qty').keydown(function(event){
          var keyCode = event.keyCode || event.which;
          if (keyCode == 40) {  // KEY DOWWN (40) 
                event.preventDefault();
                var col = $(this).parent().parent().parent().parent().attr('col')
                var i = parseInt(col)
                $(this).parent().parent().parent().parent().parent().next().children().eq(i).find('.add-qty').select();

            }
            else if (keyCode == 38){  //KEY UP
                event.preventDefault();
                var col = $(this).parent().parent().parent().parent().attr('col')
                var i = parseInt(col)
                $(this).parent().parent().parent().parent().parent().prev().children().eq(i).find('.add-qty').select();
            }
            else if (keyCode == 37){  //KEY LEFT
                event.preventDefault();
                var col = $(this).parent().parent().parent().parent().attr('col')
                var i = parseInt(col)
                $(this).parent().parent().parent().parent().prev().find('.add-qty').select();
            }
            else if (keyCode == 39){  //KEY RIGHT
                event.preventDefault();

                var col = $(this).parent().parent().parent().parent().attr('col')
                var i = parseInt(col)
                $(this).parent().parent().parent().parent().next().find('.add-qty').select();
            }
        });
        this.$('.add-price').keydown(function(event){
          var keyCode = event.keyCode || event.which;
          if (keyCode == 40) {  // KEY DOWWN (40) 
                event.preventDefault();
                var col = $(this).parent().parent().parent().parent().attr('col')
                var i = parseInt(col)
                $(this).parent().parent().parent().parent().parent().next().children().eq(i).find('.add-price').select();

            }
            else if (keyCode == 38){  //KEY UP
                event.preventDefault();
                var col = $(this).parent().parent().parent().parent().attr('col')
                var i = parseInt(col)
                $(this).parent().parent().parent().parent().parent().prev().children().eq(i).find('.add-price').select();
            }
            else if (keyCode == 37){  //KEY LEFT
                event.preventDefault();
                var col = $(this).parent().parent().parent().parent().attr('col')
                var i = parseInt(col)
                $(this).parent().parent().parent().parent().prev().find('.add-price').select();
            }
            else if (keyCode == 39){  //KEY RIGHT
                event.preventDefault();

                var col = $(this).parent().parent().parent().parent().attr('col')
                var i = parseInt(col)
                $(this).parent().parent().parent().parent().next().find('.add-price').select();
            }
        });
        this.$('.add-discount').keydown(function(event){
          var keyCode = event.keyCode || event.which;
          if (keyCode == 40) {  // KEY DOWWN (40) 
                event.preventDefault();
                var col = $(this).parent().parent().parent().parent().attr('col')
                var i = parseInt(col)
                $(this).parent().parent().parent().parent().parent().next().children().eq(i).find('.add-discount').select();

            }
            else if (keyCode == 38){  //KEY UP
                event.preventDefault();
                var col = $(this).parent().parent().parent().parent().attr('col')
                var i = parseInt(col)
                $(this).parent().parent().parent().parent().parent().prev().children().eq(i).find('.add-discount').select();
            }
            else if (keyCode == 37){  //KEY LEFT
                event.preventDefault();
                var col = $(this).parent().parent().parent().parent().attr('col')
                var i = parseInt(col)
                $(this).parent().parent().parent().parent().prev().find('.add-discount').select();
            }
            else if (keyCode == 39){  //KEY RIGHT
                event.preventDefault();

                var col = $(this).parent().parent().parent().parent().attr('col')
                var i = parseInt(col)
                $(this).parent().parent().parent().parent().next().find('.add-discount').select();
            }
        });
    },

    // Set behaviour of Button Apply, Cancel, and checks of inputs
    renderElement: function(){
        var self = this;
        this._super();
        this.$('#add-variants-button').bind('click', function(event){
            self.add_variants_button();
            self.ts_model.ts_widget.new_order_screen.order_widget.renderElement();
            self.ts_widget.new_order_screen.totals_order_widget.changeTotals();
            self.$('#close-filter').click();
        });

        // Cancel button
        this.$('#close-filter').off('click').click(function(){
            self.ts_widget.screen_selector.close_popup('grid_popup');
        });

        this.bind_onchange_events();
        this.control_arrow_keys();
    },

});


// The Grid Pop Up
var GridPopUp = PopUp.PopUpWidget.extend({
    template: 'Grid-PopUp',

    start: function(){
        var self = this
        // Define Grid Widget
        this.grid_widget = new GridWidget(this, {});
        this.grid_widget.appendTo($(this.el));
        // LLamo a hide en el start, que será la unica vez que entre
        // Ya que parece que es asincrona la llamada de apendto y no puedo
        // hacer invisible el popup despues de renderizarelo
        this.hide()
    },
    // Render the withget to load info from server each time we show it.
    show: function(line_widget){
        this.grid_widget = new GridWidget(this, {});
        this.grid_widget.appendTo($(this.el));
        var options = {
            'line_widget': line_widget
        }
        this.grid_widget.refresh(options);
        this._super();
        
    },
    hide: function(){
        if (this.grid_widget){
            this.grid_widget.destroy();
        }
        this._super();
    }
});

return {GridWidget: GridWidget}


});



