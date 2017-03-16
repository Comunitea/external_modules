
/* mousetrap v1.4.6 craig.is/killing/mice */
odoo.define('telesale.BaseWidget', function (require) {
"use strict";

var Model = require('web.DataModel');

var TsBaseWidget = require('telesale.TsBaseWidget');
var Buttons = require('telesale.ButtonsWidgets');
var Screens = require('telesale.Screens');
var models = require('telesale.models');
var core = require('web.core');
// var Mousetrap = require('telesale.Mousetrap')
var _t = core._t;


var SynchIconWidget = TsBaseWidget.extend({
    template: "Synch-Notification-Widget",
    init: function(parent, options){
        options = options || {};
        this._super(parent, options);
    },
    renderElement: function() {
        var self = this;
        this._super();
        this.$el.click(function(){
            self.ts_model.flush();
        });
    },
    start: function(){
        var self = this;
        this.ts_model.bind('change:nbr_pending_operations', function(){
            self.renderElement();
        });
    },
    get_nbr_pending: function(){
        return this.ts_model.get('nbr_pending_operations');
    },
});

var TsWidget = TsBaseWidget.extend({
    template: 'TsWidget',
    init: function() {
        this._super(arguments[0],{});
        this.ts_model = new models.TsModel(this.session,{ts_widget:this});
        this.ts_widget = this; //So that Tswidget's childs have ts_widget set automatically
    },
    start: function() {
        var self = this;
        return self.ts_model.ready.done(function(){
            self.renderElement();
            self.build_widgets(); // BUILD ALL WIDGETS AND CREENS WIDGETS
            self.screen_selector.set_default_screen(); // set principal screen
            self.$('.loader').animate({opacity:0},1500,'swing',function(){self.$('.loader').hide();});
            self.add_shortkey_events();
            self.$("#partner").focus();

        }).fail(function(){   // error when loading models data from the backend
            self.try_close();
        });
    },
    build_widgets: function() {
        var self = this;
         // --------  SCREEN WIDGETS ---------

        //New Order Screen (default)
        this.new_order_screen = new Screens.OrderScreenWidget(this, {});
        this.new_order_screen.appendTo(this.$('#content'));

        //Order History Screen
        this.order_history_screen = new Screens.OrderHistoryScreenWidget(this, {});
        this.order_history_screen.appendTo(this.$('#content'));

         //Summary Orders Screen
        this.summary_order_screen = new Screens.SummaryOrderScreenWidget(this, {});
        this.summary_order_screen.appendTo(this.$('#content'));

        //Product Catalog Screen
        this.product_catalog_screen = new Screens.ProductCatalogScreenWidget(this, {});
        this.product_catalog_screen.appendTo(this.$('#content'));

        //Key Shorts Screen
        this.key_shorts_screen = new Screens.KeyShortsScreenWidget(this, {});
        this.key_shorts_screen.appendTo(this.$('#content'));

        // --------  SCREEN SELECTOR ---------
        this.screen_selector = new Screens.ScreenSelector({
            screen_set:{
                'new_order': this.new_order_screen,
                'order_history': this.order_history_screen,
                'product_catalog': this.product_catalog_screen,
                'summary_order': this.summary_order_screen,
                'key_shorts': this.key_shorts_screen,
            },
            popup_set:{
                // 'product_sust_popup': this.product_sust_popup,
                // 'add_call_popup': this.add_call_popup,
                // 'finish_call_popup': this.finish_call_popup,
                // 'create_reserve_popup': this.create_reserve_popup,
            },
            default_client_screen: 'new_order',
         });
        //  // --------  BUTTON WIDGETS ---------
        this.notification = new Buttons.SynchIconWidget(this,{});
        this.notification.replace(this.$('#placeholder-session-buttons1'));

        // Close button --> Close the session
        this.close_button = new Buttons.HeaderButtonWidget(this,{
            label: _t('Close'),
            action: function(){ self.try_close(); },
        });
        this.close_button.replace(this.$('#placeholder-session-buttons2'));

        // Buttons navigation screens
        this.screen_buttons = new Buttons.ScreenButtonWidget(this, {});
        this.screen_buttons.replace(this.$('#placeholder-screen-buttons'));
    },
    add_shortkey_events: function(){
        var self=this;
        // allow shortcuts in any field of the screen.
        Mousetrap.stopCallback = function () {
            return false;
        }
        // Mousetrap.bind('esc', function() {
        //     self.$(window).click();
        // });
        //Add line
        Mousetrap.bind('alt+a', function(e) {
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('.add-line-button').click();
        });
        //Remove line
        Mousetrap.bind('alt+s', function(e) {
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('.remove-line-button').click()
        });

        //change betwen button block
        Mousetrap.bind('alt+q', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('#button_no').click();  //new order screen
            self.$("#partner").focus();
        });

        Mousetrap.bind('alt+w', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('#button_oh').click(); //Order history page
            self.$('.ui-autocomplete-input').focus();
            // self.$('#button2').click(); //Summary orders page
            // self.$("#input-date_start2").focus();
        });
        Mousetrap.bind('alt+e', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('#button_cl').click();//call list page
            self.$('.tab1').focus();
        });
        Mousetrap.bind('alt+r', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('#button_pc').click(); //product catalog
            self.$('#search-product').focus();
        });
        Mousetrap.bind('alt+t', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('#button_pr').click();  //product reserved page
            self.$('#input-customer').focus();
        });
        Mousetrap.bind('alt+y', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
             self.$('#button_so').click(); //Summary orders page
            self.$("#input-date_start2").focus();
        });
        Mousetrap.bind('alt+f12', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
             self.$('#button_ks').click(); //key shorts page
        });
        Mousetrap.bind('ctrl+u', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('#ult-button').click();  //ULT button
        });
        Mousetrap.bind('ctrl+m', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('#vua-button').click();  //VUM button
        });
        Mousetrap.bind('ctrl+a', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('#via-button').click();  //VIA button
        });
        Mousetrap.bind('ctrl+p', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('#promo-button').click();  //PROMOT button
        });
        Mousetrap.bind('ctrl+s', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('#sust-button').click();  //SUST button
        });
        Mousetrap.bind('ctrl+i', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('#info-button').click();  //INFO button
        });
        Mousetrap.bind('ctrl+q', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('#show-client').click();  //SHOW button
        });

        Mousetrap.bind('ctrl+alt+b', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('.save-button').click();  //SAVE button
        });
        Mousetrap.bind('ctrl+alt+c', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('.cancel-button').click();  //CANCEL button
        });
        Mousetrap.bind('ctrl+alt+enter', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('.confirm-button').click();  //CONFIRM button
        });
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
                    line_wgt.$('.col-code').focus();
                // }
            }
        });
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
                    line_wgt.$('.col-code').focus();
                }
            }
        });

        Mousetrap.bind('alt+p', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('.neworder-button').click();  //new order
            self.$('#partner').focus();
        });

        Mousetrap.bind('alt+o', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('.removeorder-button').click();  //remove order
            self.$('#partner').focus();
        });

        Mousetrap.bind('ctrl+left', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('.select-order')[0].click();
        });
        Mousetrap.bind('alt+z', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('.tab1').focus();
        });
        Mousetrap.bind('alt+x', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('.col-code').focus();
        });
        Mousetrap.bind('alt+c', function(e){
            $( document.activeElement ).blur();
            if (e.defaultPrevented) e.defaultPrevented;
            else e.returnValue = false;
            self.$('#add-line').focus();
        });
    },
    loading_progress: function(fac){
            this.$('.loader .loader-feedback').removeClass('oe_hidden');
            this.$('.loader .progress').css({'width': ''+Math.floor(fac*100)+'%'});
        },
    loading_message: function(msg,progress){
        this.$('.loader .loader-feedback').removeClass('oe_hidden');
        this.$('.loader .message').text(msg);
        if(typeof progress !== 'undefined'){
            this.loading_progress(progress);
        }
    },
    try_close: function() {
            var self = this;
            self.close();
    },
    close: function() {
        var self = this;

        function close(){
            return new Model("ir.model.data").get_func("search_read")([['name', '=', 'action_client_ts_menu']], ['res_id']).pipe(function(res) {
                window.location = '/web#action=' + res[0]['res_id'];
            });
        }
        var draft_order = true
        if(draft_order){
            if (confirm(_t("Pending orders will be lost.\nAre you sure you want to leave this session?"))) {
                return close();
            }
        }else{
            return close();
        }
    },
});

return TsWidget;

});
