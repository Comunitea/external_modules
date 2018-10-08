odoo.define('telesale_manage_variants.product_catalog_widgets', function (require) {
"use strict";

var Catalog = require('telesale.ProductCatalog');
var TsModels = require('telesale.models');
// var core = require('web.core');
// var _t = core._t;

var ProductCatalogWidget = Catalog.ProductCatalogWidget.include({

    // Catalog method to create new lines
    new_line: function(line_vals){
        var line = new TsModels.Orderline(line_vals);
        var current_order = this.ts_model.get('selectedOrder');
        current_order.get('orderLines').add(line);
        return line;
    },

    // Get values from catalog vals to create a new line
    get_create_line_vals: function(product_id, catalog_vals, mode){
        var current_order = this.ts_model.get('selectedOrder');
        var res = this._super(product_id, catalog_vals, mode);
        var prod_obj = this.ts_model.db.get_product_by_id(product_id);

        if (mode == 'template_variants'){
            res = $.extend(res, {
                ts_model: this.ts_model, 
                order:current_order,
                code: "" ,
                product:'',
                unit:'',
                qty: 0.0,
                pvp: 0.0,
                discount: 0.0,
                taxes_ids:[],
            });
        }
        else{
            var uom_obj = self.ts_model.db.get_unit_by_id(catalog_vals.product_obj.uom_id)
            res = $.extend(res, {
                ts_model: this.ts_model, 
                order:current_order,
                code: "" ,
                product: catalog_vals.product_obj.display_name || '',
                unit: uom_obj.name || '',
                qty: catalog_vals.qty || 0.0,
                pvp: catalog_vals.price || 0.0,
                discount: catalog_vals.discount || 0.0,
                // El chained discount debería estar abstraido en jim_telese
                chained_discount: catalog_vals.chained_discount || 0.0,
                taxes_ids: catalog_vals.taxes_ids || [],
            });
        }
        // Add info to manage variants
        var new_vals = {
             mode: mode || 'template_single',
             template: catalog_vals.template_obj.display_name || '',
             parent_cid: catalog_vals.parent_cid || "",
             variant_related_cid: catalog_vals.variant_related_cid || {}
        }
        $.extend(res, new_vals)
        return res
    },

    get_template_in_current_order: function(template_obj){
        var template_line = false;
        var current_order = this.ts_model.get('selectedOrder');
        var order_lines = current_order.get('orderLines').models;
        for (var key in order_lines){
            var line_model = order_lines[key];
            var template_name = line_model.get('template')
            var line_template_id = this.ts_model.db.template_name_id[template_name]
            if (line_template_id && line_template_id == template_obj.id){
                template_line = line_model;
                break;
            }
        }
        return template_line;
    },

    // FULL OVERWRITED TO INTEGRATE WITH TEMPLATE LINES STRUCTURE
    catalog_add_product(product_id, catalog_vals){
        // Create new line
        var current_order = this.ts_model.get('selectedOrder');

        var prod_obj = this.ts_model.db.get_product_by_id(product_id);
        var template_id = prod_obj.product_tmpl_id;
        var template_obj = this.ts_model.db.template_by_id[template_id];
        $.extend(catalog_vals, {product_obj: prod_obj,
                                template_obj: template_obj,
                                parent_cid: "",
                                variant_related_cid: {}});
        // More than one variant
        if (template_obj.product_variant_count > 1){

            // Get template line model if exists
            var existing_template = this.get_template_in_current_order(template_obj) 

            // If no template line, create it.
            if (!existing_template){
                var template_line_vals = {
                    variant_related_cid: {},
                    template: template_obj.display_name,
                    product: '',
                    parent_cid: "",
                }
                $.extend(catalog_vals, template_line_vals);
                var create_values = this.get_create_line_vals(product_id, catalog_vals, 'template_variants');
                existing_template = this.new_line(create_values)
            }

            // Link parent and Create Variant line
            catalog_vals.parent_cid = existing_template.cid;
            var create_values = this.get_create_line_vals(product_id, catalog_vals, 'variant');
            var variant_line = this.new_line(create_values);

            variant_line.update_line_values();

            // Update structure for Grid
            existing_template.variant_related_cid[prod_obj.id] = variant_line.cid
        }

        // Create a new template single line
        else{
            var to_add = {
                parent_cid: "",
                variant_related_cid: {}
            }
            $.extend(catalog_vals, to_add);
            var create_values = this.get_create_line_vals(product_id, catalog_vals, 'template_single');
            var template_single_line = this.new_line(create_values);
            template_single_line.update_line_values();
        }
    },

    delete_if_empty_line: function(){
        //If selected line is an empty line delete it.
        var order =  this.ts_model.get('selectedOrder')
        var selected_orderline = order.getSelectedLine();
        if(selected_orderline && selected_orderline.get('product') == "" &&  selected_orderline.get('template') == ""){
            $('.remove-line-button').click()
        }
    }


});
    return {ProductCatalogWidget: ProductCatalogWidget}

});



