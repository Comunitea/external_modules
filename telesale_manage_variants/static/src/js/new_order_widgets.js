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
        // var value = this.$('.col-template').val();
        var value = this.model.get('template');
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
                    this.model.mode = 'template_single'
                    var product_id = template_obj.product_variant_ids[0];
                    var product_obj = this.ts_model.db.get_product_by_id(product_id)
                    if (product_obj){
                        this.model.set('product', product_obj.display_name);
                        this.call_product_id_change(product_id);
                    }
                }
                // Open the grid
                else{
                    this.model.mode = 'template_variants'
                    this.refresh();
                    this.button_open_grid();
                }
            }
        }
    },

    set_value: function(key){
        if (key == 'template'){
            var value = this.$('.col-'+key).val();
            if (value != this.model.get('template')){
                this.order_widget.remove_lines_chlid_variants(this.model);
            }
        }
        this._super(key);
    },

    renderElement: function(){
        this._super();
        if (this.order_widget.view_mode == 'template'){
            this.$('.cell-product').hide();
        }
        else{
            this.$('.cell-template').hide();
            this.$('.cell-grid').hide();
        }
    },

    get_template_totals: function(){
        var totals = {
            'qty': 0.0,
            'pvp': 0.0,
            'subtotal': 0.0,
        }
        if (this.model.mode == 'template_variants'){
            var cid = "";
            var qty = 0.0
            var pvp = 0.0
            var subtotal = 0.0
            for (var variant_id in this.model.variant_related_cid){
                cid = this.model.variant_related_cid[variant_id];
                var line_model = this.model.get_line_model_by_cid(cid)
                if (line_model){
                    qty = qty + line_model.get('qty');
                    pvp = pvp + line_model.get('pvp');
                    subtotal = subtotal + line_model.get('total');
                }
            }
            totals['qty'] = qty;
            totals['pvp'] = pvp;
            totals['subtotal'] = subtotal;
        }
        return totals
    },

    get_template_qty: function(){
        var totals = this.get_template_totals()
        return totals['qty']
    },

    get_template_pvp: function(){
        // var totals = this.get_template_totals()
        // return totals['pvp']
        return "";
    },

    get_template_subtotal: function(){
        var totals = this.get_template_totals()
        return totals['subtotal']
    },

});


var OrderWidget = NewOrderWidgets.OrderWidget.include({
    events: {
            'click .add-line-button': 'button_add_line',
            'click .remove-line-button': 'button_remove_line',
            'click  #ult-button': 'button_ult',
            'click  #vua-button': 'button_vua',
            'click  #so-button': 'button_so',
            'click  #promo-button': 'button_promo',
            'click  #info-button': 'button_info',
            'click  #show-client': 'button_show_client',
            // ADDED
            'click  #change_view': 'button_change_view',
        },
    init: function(parent, options){
        this._super(parent, options);
        this.view_mode = 'template';
    },
    button_change_view: function(){

       if (this.view_mode == 'template'){
            this.view_mode = 'variant';
       }
       else{
            this.view_mode = 'template';
       }
       this.renderElement();
    },
    renderLines: function(options){
        var self = this;
        // Destroy line widgets
        for(var i = 0, len = this.orderlinewidgets.length; i < len; i++){
            this.orderlinewidgets[i].destroy();
        }
        this.orderlinewidgets = [];

        var $content = this.$('.orderlines');
        var nline = 1


        var allow_modes = ['template_single', 'template_variants']
        if (this.view_mode == 'variant'){
            allow_modes = ['template_single', 'variant']
        }
        this.currentOrderLines.each(_.bind( function(orderLine) {
            orderLine.set('n_line', nline++);
            var line_mode = orderLine.mode
            if (allow_modes.indexOf(line_mode) >= 0){
                var line = new NewOrderWidgets.OrderlineWidget(this, {
                    model: orderLine,
                    order: this.ts_model.get('selectedOrder'),
                });
                line.appendTo($content);
                self.orderlinewidgets.push(line);
            }
        }, this));
    },

    remove_lines_chlid_variants: function(template_line){
        var current_order = this.ts_model.get('selectedOrder')
        for (var variant_id in template_line.variant_related_cid){
            var cid = template_line.variant_related_cid[variant_id];
            var line_model = template_line.get_line_model_by_cid(cid)
            current_order.selectLine(line_model);
            current_order.removeLine();
            // delete template_line.variant_related_cid[variant_id]; 
            }
    },

    // get template_variants line and remove variant_related_cid key
    remove_variant_related: function(variant_line){
        var cid = variant_line.parent_cid
        var template_line = variant_line.get_line_model_by_cid(cid)

        var variant_id = variant_line.get_product().id
        delete template_line.variant_related_cid[variant_id]; 

    },

    //Ovewwrited to focus template
    button_remove_line: function(){
            var current_order = this.ts_model.get('selectedOrder');
            var selected_line = current_order.getSelectedLine();
            if (selected_line.mode == 'template_variants'){
                this.remove_lines_chlid_variants(selected_line)
            }

            if (selected_line.mode == 'variant'){
                this.remove_variant_related(selected_line)
            }

            // select line again to remove it
           current_order.selectLine(selected_line);
            this.ts_model.get('selectedOrder').removeLine();
            var selected_line = current_order.getSelectedLine();
            if (selected_line){
                var n_line = selected_line.get('n_line')
                if (this.orderlinewidgets[n_line-1]){
                    this.orderlinewidgets[n_line-1].$('.col-template').focus();
                }
            }
    },
    button_add_line: function(){
            // click add line event function
            var order =  this.ts_model.get('selectedOrder')
            var partner_id = this.ts_model.db.partner_name_id[order.get('partner')]
            if (!partner_id){
                alert(_t('Please select a customer before adding a order line'));
                $('#partner').focus();
            }else{
                this.ts_model.get('selectedOrder').addLine();
                var added_line = this.ts_model.get('selectedOrder').getLastOrderline();
                this.ts_model.get('selectedOrder').selectLine(added_line);
                this.orderlinewidgets[this.orderlinewidgets.length - 1].$('.col-template').focus(); //set focus on line when we add one
            }
    },

    renderElement: function(){
        this._super();
        if (this.view_mode == 'template'){
            this.$('.header-product').hide();
        }
        else{
            this.$('.header-template').hide();
            this.$('.header-grid').hide();
        }
    }
    });

});



