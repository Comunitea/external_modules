odoo.define('telesale.BaseWidget', function (require) {
"use strict";

var Widget = require('web.Widget');
var Model = require('web.DataModel');

var TsBaseWidget = require('telesale.BaseWidget0');
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

//Generic Buttons whitch actions are part of TsWidget, like close button
var HeaderButtonWidget = TsBaseWidget.extend({
    template: 'HeaderButtonWidget',
    init: function(parent, options){
        options = options || {};
        this._super(parent, options);
        this.action = options.action;
        this.label   = options.label;

    },
    renderElement: function(){
        var self = this;
        this._super();
        if(this.action){
            this.$el.click(function(){ self.action(); });
        }
    },
    show: function(){ this.$el.show(); },
    hide: function(){ this.$el.hide(); },
});

var ButtonBlockWidget = TsBaseWidget.extend({
    init: function(parent,options){
        this._super(parent,options);
        this.hidden = false;
    },
    show: function(){
        var self = this;
        this.hidden = false;
        if(this.$el){
            this.$el.show();
        }
    },
    hide: function(){
        this.hidden = true;
        if (this.$el){
            this.$el.hide();
        }
    },
    renderElement: function(){
        // we need this because some screens re-render themselves when they are hidden
        // (due to some events, or magic, or both...)  we must make sure they remain hidden.
        this._super();
        if(this.hidden){
            if(this.$el){
                this.$el.hide();
            }
        }
    },
    select_screen: function(screen_name){
        var self = this;
        this.ts_widget.screen_selector.set_current_screen(screen_name);
    },
    select_button_block: function(block_name){
        var self = this;
        this.ts_widget.button_block_selector.set_current_block(block_name);
        // if (this.$('.selected-screen'))
        //      this.$('.selected-screen').removeClass('selected-screen');
        // this.$el.addClass('selected-screen');
    },
    // close: function(){

    // },
});

// Buttons block to change between principal screens
var ScreenButtonWidget = ButtonBlockWidget.extend({
    template: 'ScreenButtonWidget',
    init: function(parent,options){
        this._super(parent,options);
        this.button_no = _t("New Order");
        this.button_so = _t("My Orders");
        this.button_pc = _t("Product Catalog");
        this.button_pr = _t("Product Reserved");
        this.button_cl = _t("Call List");
        this.button_oh = _t("Order History");
        this.button_ks = _t("Key Shorts");
    },
    renderElement: function(){
        var self = this;
        this._super();
        this.$el.find('button#button_no').click(function(){ self.select_screen('new_order');
                                                          // self.select_button_block('order_buttons');
                                                          self.setButtonSelected('button#button_no');
                                                         });
        this.$el.find('button#button_so').click(function(){ self.select_screen('summary_order');
                                                          self.setButtonSelected('button#button_so');
                                                             });
        this.$el.find('button#button_cl').click(function(){ self.select_screen('call_list');
                                                          self.setButtonSelected('button#button_cl');
                                                             });
        this.$el.find('button#button_oh').click(function(){ self.select_screen('order_history')
                                                          self.setButtonSelected('button#button_oh');
                                                             });
        this.$el.find('button#button_pc').click(function(){ self.select_screen('product_catalog');
                                                            var upd = self.ts_model.get('update_catalog')
                                                            if (upd === 'a'){
                                                                upd = 'b'
                                                            }
                                                            else{
                                                                upd = 'a'
                                                            }
                                                            self.ts_model.set('update_catalog', upd)
                                                          self.setButtonSelected('button#button_pc');
                                                         });
        this.$el.find('button#button_pr').click(function(){ self.select_screen('product_reserved');
                                                           self.setButtonSelected('button#button_pr');
                                                         });
        this.$el.find('button#button_ks').click(function(){ self.select_screen('key_shorts');
                                                           self.setButtonSelected('button#button_ks');
                                                         });


    },
    setButtonSelected: function(button_selector) {
        $('.selected-screen').removeClass('selected-screen');
        $(button_selector).addClass('selected-screen');
        $('.tab1').focus();
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


            debugger;
            self.build_widgets(); // BUILD ALL WIDGETS AND CREENS WIDGETS
            // self.screen_selector.set_default_screen(); // set principal screen
            self.$('.loader').animate({opacity:0},1500,'swing',function(){self.$('.loader').hide();});
            // self.add_shortkey_events();
            // self.ts_model.get_calls_by_date_state(self.ts_model.getCurrentDateStr()); // get call list for current date
            // self.$("#partner").focus();


        }).fail(function(){   // error when loading models data from the backend
            self.try_close();
        });
    },
    build_widgets: function() {
         // --------  BUTTON WIDGETS ---------
        this.notification = new SynchIconWidget(this,{});
        this.notification.replace(this.$('#placeholder-session-buttons1'));

        // Close button --> Close the session
        this.close_button = new HeaderButtonWidget(this,{
            label: _t('Close'),
            action: function(){ self.try_close(); },
        });
        this.close_button.replace(this.$('#placeholder-session-buttons2'));

        // Buttons navigation screens
        this.screen_buttons = new ScreenButtonWidget(this, {});
        this.screen_buttons.replace(this.$('#placeholder-screen-buttons'));
        var self = this;
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
