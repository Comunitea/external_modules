odoo.define('telesale.PopUps', function (require) {
"use strict";

var TsBaseWidget = require('telesale.TsBaseWidget');
var rpc = require('web.rpc');
var session = require('web.session');


var PopUpWidget = TsBaseWidget.extend({
    show: function(){
        if(this.$el){
            this.$el.show();
        }
    },
    close: function(){
    },
    hide: function(){
        if(this.$el){
            this.$el.hide();
        }
    },
});

var SoldHistoryWidget = TsBaseWidget.extend({
    template: 'Sold-History-Widget',

    init: function(parent, options){
        this._super(parent, options);
        this.line_results = [];
        this.selected_line = false;
    },

    // Load Grid From server
    get_history_from_server: function(product_id){
        self=this;
        var current_order = this.ts_model.get('selectedOrder');
        var partner_id = this.ts_model.db.partner_name_id[current_order.get('partner')];
        var loaded = rpc.query({model: 'product.product', method: 'get_history_product_info', args:[product_id, partner_id], kwargs: {context: session.user_context}})
        .then(function(result){
            self.line_results = result
        });
        return loaded
    },

    refresh: function(options){
        var self = this;
        this.selected_line = options.selected_line;
        if (this.selected_line){
            var product_obj = this.selected_line.get_product();
            $.when(this.get_history_from_server(product_obj.id))
            .then(function(){
                self.renderElement();
            });
        }
    }

});


var CustomerHistoryPopUp = PopUpWidget.extend({
    template: 'Customer-History-PopUp',
    start: function(){
        var self = this
        this._super();
        this.$('#close-filter').off('click').click(function(){
            self.ts_widget.screen_selector.show_popup('filter_customer_popup', undefined);
            self.ts_widget.screen_selector.close_popup('filter-customer_popup');
        })
        // LLamo a hide en el start, que será la unica vez que entre
        // Ya que parece que es asincrona la llamada de apendto y no puedo
        // hacer invisible el popup despues de renderizarelo
        this.hide()
    },
    show: function(selected_line){
        var self = this;
        this.sold_history_widget = new SoldHistoryWidget(this, {});
        this.sold_history_widget.appendTo($(this.el));

        var options = {
            'selected_line': selected_line
        }
        this.sold_history_widget.refresh(options);

        this._super();
        this.$('#close-filter').off('click').click(function(){
            // self.ts_widget.screen_selector.show_popup('filter_customer_popup', undefined);
            self.ts_widget.screen_selector.close_popup('filter-customer_popup');
        })
    },
    hide: function(){
        if (this.sold_history_widget){

            this.sold_history_widget.destroy();
        }
        this._super();
    }
});

return {CustomerHistoryPopUp: CustomerHistoryPopUp,
        PopUpWidget: PopUpWidget};

});
