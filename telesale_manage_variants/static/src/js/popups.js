odoo.define('telesale_manage_variants.base_widgets', function (require) {
"use strict";
var BaseWidgets = require('telesale.BaseWidget');
var PopUp = require('telesale.PopUps');

var GridPopUp = PopUp.PopUpWidget.extend({
    template: 'Grid-PopUp',
    init: function(parent,options){
        this._super(parent,options);
    },
    show: function(line_widget){
        var self = this;
        this._super();
        this.$('#close-filter').off('click').click(function(){
            self.ts_widget.screen_selector.close_popup('filter_customer_popup');
        })
    },
});


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

});



