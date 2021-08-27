odoo.define('telesale.TsBaseWidget', function (require) {
"use strict";

var Widget = require('web.Widget');

// This is a base class for all Widgets in the TS.
var TsBaseWidget = Widget.extend({
    init:function(parent,options){
        this._super(parent, options);
        options = options || {}; //avoid options undefined
        this.ts_model = options.ts_model || (parent ? parent.ts_model : undefined)
        this.ts_widget = options.ts_widget || (parent ? parent.ts_widget : undefined);  // In order all child's can acces telesale widget
    },
   
    show: function(){
        this.$el.show();
    },
    hide: function(){
        this.$el.hide();
    },
});

return TsBaseWidget;

});
