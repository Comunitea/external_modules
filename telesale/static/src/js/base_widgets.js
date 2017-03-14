odoo.define('telesale.BaseWidget', function (require) {
"use strict";

var Model = require('web.DataModel');

var TsBaseWidget = require('telesale.TsBaseWidget');
var Buttons = require('telesale.ButtonsWidgets');
var Screens = require('telesale.Screens');
var models = require('telesale.models');
var core = require('web.core');
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
            self.renderElement();  //Contruye la plantilla????

            self.build_widgets(); // BUILD ALL WIDGETS AND CREENS WIDGETS
            self.screen_selector.set_default_screen(); // set principal screen
            self.$('.loader').animate({opacity:0},1500,'swing',function(){self.$('.loader').hide();});
            // self.add_shortkey_events();
            // self.ts_model.get_calls_by_date_state(self.ts_model.getCurrentDateStr()); // get call list for current date
            // self.$("#partner").focus();


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
        // var self = this;
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
        // var draft_order = _.find( self.ts_model.get('orders').models, function(order){
        //     return order.get('orderLines').length !== 0
        // });
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
