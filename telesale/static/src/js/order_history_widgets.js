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
    load_order_from_server: function(order_id, flag){
        var self=this;
        if (!flag){
            this.ts_model.get('orders').add(new models.Order({ ts_model: self.ts_model}));
        }
        this.open_order =  this.ts_model.get('selectedOrder')
        var loaded = self.ts_model.fetch('sale.order',
                                        ['contact_id','note','comercial','customer_comment','name','partner_id','date_order',
                                         'state','amount_total','date_planned'],
                                        [
                                        ['id', '=', order_id]
                                        ])
            .then(function(orders){
                var order = orders[0];
                self.order_fetch = order;
                return self.ts_model.fetch('sale.order.line',
                                            ['product_id','product_uom',
                                            'product_uom_qty',
                                            'price_unit',
                                            'tax_id',
                                            'price_subtotal',
                                            'discount'],
                                            [
                                                ['order_id', '=', order_id],
                                             ]);
            }).then(function(order_lines){
                if (flag =='add_lines'){
                    self.open_order.add_lines_to_current_order(order_lines);
                    self.ts_widget.new_order_screen.data_order_widget.refresh();
                    self.ts_widget.new_order_screen.order_widget.change_selected_order()
                    self.ts_widget.new_order_screen.totals_order_widget.changeTotals();
                }else{
                    self.ts_model.build_order(self.order_fetch, self.open_order, order_lines); //build de order model
                    self.ts_widget.new_order_screen.data_order_widget.refresh();
                }
            })
        return loaded
    },
    click_handler: function() {
        var self=this;
        $.when(self.load_order_from_server(self.order.id))
            .done(function(){
                $('button#button_no').click();
            });
    },
    click_handler2: function() {
        var self=this;
        var order =  self.ts_model.get('selectedOrder')
        var partner_id = self.ts_model.db.partner_name_id[order.get('partner')]
        if (!partner_id){
                alert(_t('Please select a customer before adding a order line'));
        }else{
        $.when(self.load_order_from_server(self.order.id, 'add_lines'))
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
        this.$('#search-customer').click(function (){ self.searchCustomerOrders() });
        this.$('#search-customer-week').click(function (){ self.searchCustomerOrdersBy('week') });
        this.$('#search-customer-month').click(function (){ self.searchCustomerOrdersBy('month') });
        this.$('#search-customer-trimester').click(function (){ self.searchCustomerOrdersBy('trimester') });
        var $history_content = this.$('.historylines');
        for (var key in this.partner_orders){
            var history_order = this.partner_orders[key];
            var history_line = new HistorylineWidget(this, {order: history_order});
            history_line.appendTo($history_content);
        }
    },
    load_partner_orders: function(partner_id, date_start, date_end){
        var self=this;
        var domain =   [['partner_id', '=', partner_id]]
        if (date_start != ""){
            domain.push(['date_order', '>=', date_start])
        }
        if (date_end != ""){
            domain.push(['date_order', '<=', date_end])
        }
        var loaded = self.ts_model.fetch('sale.order',
                                        ['name','partner_id','date_order','state','date_planned', 'amount_total'],
                                        domain)
            .then(function(orders){
             self.partner_orders = orders;
             })

        return loaded;
    },
    searchCustomerOrders: function () {
        var self=this;
        var partner_name = this.$('#input-customer').val();
        var date_start = this.$('#input-date_start').val();
        var date_end = this.$('#input-date_end').val();
        var partner_id = this.ts_model.db.partner_name_id[partner_name];
        if (!partner_id){
            alert(_t("Customer " + "'"+partner_name+"'" + " does not exist."));
            this.$('#input-customer').focus();
        }
        else{
            $.when(this.load_partner_orders(partner_id,date_start,date_end))
            .done(function(){
                self.renderElement();
                self.$('#input-customer').val(partner_name);
            }).fail(function(){
                //?????
            });
        };
    },
    searchCustomerOrdersBy: function (period){
        var self=this;
        var start_date = new Date();
        var end_date_str = this.ts_model.getCurrentDateStr();
        var partner_name = this.$('#input-customer').val();
        if (period == 'week')
            start_date.setDate(start_date.getDate() - 30);
        else if (period == 'month')
            start_date.setDate(start_date.getDate() - 30);
        else if (period == 'trimester')
            start_date.setDate(start_date.getDate() - 90);
        var start_date_str = this.ts_model.dateToStr(start_date);
        var partner_name = this.$('#input-customer').val();
        var partner_id = this.ts_model.db.partner_name_id[partner_name];
        if (!partner_id){
            alert(_t("Customer " + "'"+partner_name+"'" + " does not exist."));
        }
        else{
            $.when(this.load_partner_orders(partner_id,start_date_str,end_date_str))
            .done(function(){
                self.renderElement();
                self.$('#input-customer').val(partner_name);
            }).fail(function(){
            });
        }
    },
});

return {
    HistorylineWidget: HistorylineWidget,
    OrderHistoryWidget: OrderHistoryWidget
};
});
