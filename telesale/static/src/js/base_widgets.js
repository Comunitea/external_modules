odoo.define('telesale.BaseWidget', function (require) {
"use strict";

var Widget = require('web.Widget');


// This is a base class for all Widgets in the TS.
var TsBaseWidget = Widget.extend({
    init:function(parent,options){
        this._super(parent);
        options = options || {};
        this.ts    = options.ts    || (parent ? parent.ts : undefined);
        this.chrome = options.chrome || (parent ? parent.chrome : undefined);
        this.gui    = options.gui    || (parent ? parent.gui : undefined); 
    },
   
    show: function(){
        this.$el.removeClass('oe_hidden');
    },
    hide: function(){
        this.$el.addClass('oe_hidden');
    },
});


var TsWidget = TsBaseWidget.extend({
    template: 'TsWidget',
    init: function() {
        var self = this;
        this._super(arguments[0],{});
    },
    start: function() {
    },
});

return TsWidget;

});
