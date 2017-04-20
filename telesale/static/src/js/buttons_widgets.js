odoo.define('telesale.ButtonsWidgets', function (require) {
"use strict";

var TsBaseWidget = require('telesale.TsBaseWidget');
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
        this.button_so = _t("My Customers");
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

return {
    SynchIconWidget:  SynchIconWidget,
    HeaderButtonWidget: HeaderButtonWidget,
    ScreenButtonWidget: ScreenButtonWidget
};

});
