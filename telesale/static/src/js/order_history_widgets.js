odoo.define('telesale.OrderHistory', function (require) {
"use strict";

var TsBaseWidget = require('telesale.TsBaseWidget');
var models = require('telesale.models');
var core = require('web.core');
var _t = core._t;

var exports = {};

var HistorylineWidget = TsBaseWidget.extend({
    template:'History-Line-Widget',
    init: function(parent, options){
        this._super(parent,options);
        this.order = options.order;
        this.open_order = undefined;
        this.order_fetch = undefined;
    },
    exists_opened_order: function(parent, options){
        var self = this;
        var res = false;
        this.ts_model.get('orders').forEach(function(order){
            if (order.get('erp_id') == self.order.id){
                res = order;
            }
        });
        return res;
    },
    click_handler: function() {
        var self=this;
        var opened_order = this.exists_opened_order()
        if ( opened_order ){
            self.ts_model.set('selectedOrder', opened_order)
            $('button#button_no').click();
        }
        else {
        $.when(self.ts_widget.new_order_screen.order_widget.load_order_from_server(self.order.id, false))
            .done(function(){
                $('button#button_no').click();
            });
        }
    },
    click_handler2: function() {
        var self=this;
        var order =  self.ts_model.get('selectedOrder')
        var partner_id = self.ts_model.db.partner_name_id[order.get('partner')]
        if (!partner_id){
                alert(_t('Please select a customer before adding a order line'));
        }else{
        $.when(self.ts_widget.new_order_screen.order_widget.load_order_from_server(self.order.id, 'add_lines'))
            .done(function(){
                $('button#button_no').click();
            });
        }
    },
    renderElement: function() {
        var self=this;
        this._super();
        this.$("#button-line-adding").click(_.bind(this.click_handler2, this));
        this.$("#button-order-creating").click(_.bind(this.click_handler, this));
    },
});

var OrderHistoryWidget = TsBaseWidget.extend({
    template:'Order-History-Widget',
    init: function(parent, options) {
        this._super(parent,options);
        this.partner_orders = [];

    },
    renderElement: function () {
        var self = this;
        this._super();
        var array_names = self.ts_model.get('customer_names');
        // Autocomplete products and units from array of names
        this.$('#input-customer').autocomplete({
            source: function(request, response) {
                var results = $.ui.autocomplete.filter(array_names, request.term);
                response(results.slice(0, 20));
            }
        });
        this.$('#input-customer').keydown(function(e){
            if( e.keyCode != $.ui.keyCode.ENTER ) return; 

            e.keyCode = $.ui.keyCode.DOWN;
            $(this).trigger(e);

            self.$('#input-date_start').focus()
    
            return false;
        });
        this.$('#search-customer').click(function (){ self.searchCustomerOrders() });
        this.$('#search-customer-week').click(function (){ self.searchCustomerOrders('week') });
        this.$('#search-customer-month').click(function (){ self.searchCustomerOrders('month') });
        this.$('#search-customer-trimester').click(function (){ self.searchCustomerOrders('trimester') });
        var $history_content = this.$('.historylines');
        for (var key in this.partner_orders){
            var history_order = this.partner_orders[key];
            var history_line = new HistorylineWidget(this, {order: history_order});
            history_line.appendTo($history_content);
        }
    },
    get_order_fields: function(){
        var field_list = ['name', 'partner_id','date_order','state', 'requested_date', 'amount_total']
        return field_list
    },
    get_order_domain: function(partner_id, date_start, date_end, my_filter){
        var domain = []
        if (partner_id != ""){
            domain.push(['partner_id', '=', partner_id])
        }
        if (date_start != ""){
            domain.push(['date_order', '>=', date_start])
        }
        if (date_end != ""){
            domain.push(['date_order', '<=', date_end])
        }
        if (my_filter){
            domain.push(['create_uid', '=', this.ts_model.get('user').id])
        }
        return domain
    },
    load_partner_orders: function(partner_id, date_start, date_end, my_filter){
        var self=this;
        var domain = this.get_order_domain(partner_id, date_start, date_end, my_filter);
        var field_list = this.get_order_fields();
        var loaded = self.ts_model.fetch('sale.order', field_list, domain)
        .then(function(orders){
             self.partner_orders = orders;
        })
        return loaded;
    },
    searchCustomerOrders: function (period) {
        var self=this;
        // Geting dates filter
        if (!period){
            var date_start = this.$('#input-date_start').val();
            var date_end = this.$('#input-date_end').val();
        }
        else{
             var start_date = new Date();
             var end_date_str = this.ts_model.getCurrentDateStr();
            if (period == 'week')
                start_date.setDate(start_date.getDate() - 30);
            else if (period == 'month')
                start_date.setDate(start_date.getDate() - 30);
            else if (period == 'trimester')
                start_date.setDate(start_date.getDate() - 90);
            var start_date_str = this.ts_model.dateToStr(start_date);
            date_start = start_date_str
            date_end = end_date_str
        }
        // Geting partner
        var partner_name = this.$('#input-customer').val();
        var partner_id = false;
        if (partner_name != ""){
            partner_id = this.ts_model.db.partner_name_id[partner_name];
            if (!partner_id){
                alert(_t("Customer " + "'"+partner_name+"'" + " does not exist."));
                this.$('#input-customer').focus();
            }
        }

        // Geting my orders filter
        var my_orders = this.$('#my_orders').is(":checked");
        $.when(this.load_partner_orders(partner_id,date_start,date_end, my_orders))
        .done(function(){
            self.renderElement();
            self.$('#input-customer').val(partner_name);
        }).fail(function(){
           alert("Error fetching orders from server");
           this.$('#input-customer').focus();
        });
    },
});

return {
    HistorylineWidget: HistorylineWidget,
    OrderHistoryWidget: OrderHistoryWidget
};
});
