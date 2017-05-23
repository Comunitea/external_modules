odoo.define('telesale_manage_variants.BaseWidget', function (require) {
"use strict";

var BaseWidgets = require('telesale.BaseWidget');

var TsWidget = BaseWidgets.TsWidget.include({
    add_shortkey_events: function(){
        var self=this;
        this._super();
        Mousetrap.unbind('ctrl+down')
        Mousetrap.bind('ctrl+down', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            var wgt_order = self.new_order_screen.order_widget;
            var order_lines_wgts = wgt_order.orderlinewidgets;
            if (!$.isEmptyObject(order_lines_wgts)){
                var order_model = self.ts_model.get('selectedOrder');
                var selected_line_model = order_model.getSelectedLine();
                var index = 0;
                if (selected_line_model){
                    var index = selected_line_model.get('n_line');
                }
                var cur_line = order_lines_wgts[index-1]
                if (index == order_lines_wgts.length)
                    index = 0;

                var line_wgt = order_lines_wgts[index];
                // if (!line_wgt.model.is_selected()){
                    // if (cur_line) cur_line.$('.mandatory').blur();
                    line_wgt.$el.click();
                    line_wgt.$('.col-template').focus();
                // }
            }
        });
        Mousetrap.unbind('ctrl+up')
        Mousetrap.bind('ctrl+up', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            var wgt_order = self.new_order_screen.order_widget;
            var order_lines_wgts = wgt_order.orderlinewidgets;
            if (!$.isEmptyObject(order_lines_wgts)){
                var order_model = self.ts_model.get('selectedOrder');
                var selected_line_model = order_model.getSelectedLine();
                var index = 0;
                if (selected_line_model){
                    var index = selected_line_model.get('n_line') - 2;
                }
                var cur_line = order_lines_wgts[index+1]
                if (index == -1)
                    index = order_lines_wgts.length - 1;
                var line_wgt = order_lines_wgts[index];
                if (!line_wgt.model.is_selected()){
                    // if (cur_line) cur_line.$('.mandatory').blur()
                    line_wgt.$el.click();
                    line_wgt.$('.col-template').focus();
                }
            }
        });
        Mousetrap.unbind('alt-x')
        Mousetrap.bind('alt+x', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('.col-template').focus();
        });
    }

});

});


