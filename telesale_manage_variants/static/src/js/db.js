odoo.define('telesale_manage_variants.db', function (require) {
"use strict";

var DB = require('telesale.db');
// var OrderLineSuper = TsModels.OrderLine
// var OrderSuper = TsModels.Order
// var Backbone = window.Backbone;

DB.TS_LS = DB.TS_LS.extend({
    init: function(options){
        this._super(options);
        this.template_by_id = {};
        this.template_name_id = {};
    },
    add_templates: function(templates){
        for(var i=0 ; i < templates.length; i++){
            var template = templates[i];
            this.template_by_id[template.id] = template
            this.template_name_id[template.display_name] = template.id
        }
    },
    get_template_by_id: function(template_id){
        return this.template_by_id[template_id];
    }
    
});

});
