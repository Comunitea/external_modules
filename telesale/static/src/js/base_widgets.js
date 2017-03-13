odoo.define('telesale.BaseWidget', function (require) {
"use strict";

var Widget = require('web.Widget');
var models = require('telesale.models');

// This is a base class for all Widgets in the TS.
var TsBaseWidget = Widget.extend({
    init:function(parent,options){
        this._super(parent);
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
            // self.screen_selector.set_default_screen(); // set principal screen
            // self.$('.loader').animate({opacity:0},1500,'swing',function(){self.$('.loader').hide();});
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
        // this.close_button = new module.HeaderButtonWidget(this,{
        //     label: _t('Close'),
        //     action: function(){ self.try_close(); },
        // });
        // this.close_button.replace(this.$('#placeholder-session-buttons2'));

        // Buttons navigation screens
        // this.screen_buttons = new module.ScreenButtonWidget(this, {});
        // this.screen_buttons.replace(this.$('#placeholder-screen-buttons'));
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
});

return TsWidget;

});
