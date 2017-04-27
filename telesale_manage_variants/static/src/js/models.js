odoo.define('telesale_manage_variants.models2', function (require) {
"use strict";
var TsModels = require('telesale.models');
// var OrderLineSuper = TsModels.OrderLine
// var OrderSuper = TsModels.Order
// var Backbone = window.Backbone;

var TsModelSuper = TsModels.TsModel
TsModels.TsModel = TsModels.TsModel.extend({
    // Fetch order template from server
    load_server_data: function(){
        var self=this;
        var loaded = TsModelSuper.prototype.load_server_data.call(this,{})
        var template_fields = ['name', 'display_name', 'product_variant_ids', 'product_variant_count']
        var template_domain = [['sale_ok','=',true]]
        // FIX; NOT RENDER DATAWIDGET AT TIME
        loaded = self.fetch('product.template', template_fields, template_domain)
            .then(function(templates){
              self.set('template_names', [])
              for (var key in templates){
                    var tmp = templates[key]
                    self.get('template_names').push(tmp.display_name);
                }
            });
        return TsModelSuper.prototype.load_server_data.call(this,{})
    }
});

});
