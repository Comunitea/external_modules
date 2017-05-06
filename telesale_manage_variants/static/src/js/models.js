odoo.define('telesale_manage_variants.models2', function (require) {
"use strict";
var TsModels = require('telesale.models');
var OrderSuper = TsModels.Order
// var Backbone = window.Backbone;

var TsModelSuper = TsModels.TsModel
TsModels.TsModel = TsModels.TsModel.extend({
    // Fetch order template from server
    load_server_data: function(){
        var self=this;
        var loaded = TsModelSuper.prototype.load_server_data.call(this,{})
        var template_fields = ['name', 'display_name', 'product_variant_ids', 'product_variant_count']
        var template_domain = [['sale_ok','=',true]]
        // FIX; NOT RENDER DATAWIDGET AT TIME?
        loaded = self.fetch('product.template', template_fields, template_domain)
            .then(function(templates){
                self.db.add_templates(templates);

                // Set names list to autocomplete
                self.set('template_names', [])
                for (var key in templates){
                    var tmp = templates[key]
                    self.get('template_names').push(tmp.display_name);
                }
            });
        return TsModelSuper.prototype.load_server_data.call(this,{})
    }
});

// Set template to store the template name en la linea
var _initialize_ = TsModels.Orderline.prototype.initialize;
TsModels.Orderline.prototype.initialize = function(options){
    var self = this;
    this.set({
        template : options.template || ''
    });

    //template_singe: A normal line, template with one variant
    //template_variants: Grouping line with special grouping behavior
    //variant: Line created with the grid, parent line is a template_variants
    this.mode = options.mode || 'template_single'
    this.parent_cid = options.parent_cid || undefined;
    this.variant_related_cid = options.variant_related_id || {};
    return _initialize_.call(this, options);
}

//Overwrited to not fail when product empty if is a template grouping line
TsModels.Orderline.prototype.check = function(){
    var res = true
    if ( this.mode != "template_variants" && this.get('product') == "" ) {
       res = false;
    }
    return res
}

TsModels.Orderline.prototype.get_line_model_by_cid = function(line_cid){
    var current_order = this.ts_model.get('selectedOrder');
    var line_model = current_order.get('orderLines').get({cid: line_cid}); 
    return line_model;
},


// Function to get template obj from model (Extend is not working)
TsModels.Orderline.prototype.get_template = function(){
    var template_name = this.get('template');
    if (this.get('template') != ""){
        var template_id = this.ts_model.db.template_name_id[template_name];
        var template_obj = this.ts_model.db.template_by_id[template_id]
        return template_obj
    }
    return false
}

var _exportJSON_ = TsModels.Orderline.prototype.export_as_JSON;
TsModels.Orderline.prototype.export_as_JSON = function(){
    var res = _exportJSON_.call(this, {});
    var to_add = {mode: this.mode,
                  cid: this.cid,
                  parent_cid: this.parent_cid}
    res = $.extend(res, to_add)
    return res
}



});
