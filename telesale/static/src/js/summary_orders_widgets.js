odoo.define('telesale.Summary', function (require) {
"use strict";

var TsBaseWidget = require('telesale.TsBaseWidget');
var models = require('telesale.models');
var core = require('web.core');
var _t = core._t;

var exports = {};

exports.SummarylineWidget = TsBaseWidget.extend({
    template:'Summary-Line-Widget',
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
                                        ['supplier_id','contact_id','note','comercial','customer_comment','client_order_ref','name','partner_id','date_order','state','amount_total','date_invoice', 'date_planned', 'date_invoice'],  //faltan los impuestos etc
                                        [
                                            ['id', '=', order_id]
                                        ])
            .then(function(orders){
                var order = orders[0];
                self.order_fetch = order;
                return self.ts_model.fetch('sale.order.line',
                                            ['product_id','product_uom',
                                            'product_uom_qty',
                                            'price_unit','product_uos',
                                            'product_uos_qty',
                                            'price_udv',
                                            'price_subtotal','tax_id',
                                            'pvp_ref','current_pvp',
                                            'q_note', 'detail_note',
                                            'discount', 'tourism'],
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
                    self.ts_widget.new_order_screen.data_order_widget.refresh();  // show screen and order model refreshed.
//                        self.ts_widget.new_order_screen.totals_order_widget.changeTotals();
                }
            })
    },
    click_handler: function() {
        var self=this;
        $.when(self.load_order_from_server(self.order.id))
            .done(function(){
                $('button#button_no').click();
            }).fail(function(){
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
        // this.$el.click(_.bind(this.click_handler, this));
        this.$("#button-show-order").click(_.bind(this.click_handler, this));
        this.$("#button-adding-lines").click(_.bind(this.click_handler2, this));
    },
});

exports.SummaryOrderWidget = TsBaseWidget.extend({
    template:'Summary-Order-Widget',
    init: function(parent, options) {
        this._super(parent,options);
        this.partner_orders = [];
        this.summary_line_widgets = []

    },
    renderElement: function () {
        var self = this;
        this._super();
        this.$('#search-customer2').click(function (){ self.searchCustomerOrders() });
        this.$('#search-customer2-week').click(function (){ self.searchCustomerOrdersBy('week') });
        this.$('#search-customer2-month').click(function (){ self.searchCustomerOrdersBy('month') });
        this.$('#search-customer2-trimester').click(function (){ self.searchCustomerOrdersBy('trimester') });
        var $summary_content = this.$('.summary-lines');
        for(var i = 0, len = this.summary_line_widgets .length; i < len; i++){
            this.summary_line_widgets[i].destroy();
        }
        this.summary_line_widgets = [];
        for (var key in this.partner_orders){
            var summary_order = this.partner_orders[key];
            var summary_line = new SummarylineWidget(this, {order: summary_order});
            summary_line.appendTo($summary_content);
            self.summary_line_widgets.push(summary_line);
        }
    },
    load_partner_orders: function(date_start,date_end){
       // HAY QUE CONTROLAR LAS FECHAS CON UTC, HORARIO DE INVIERNO -1H VERANO -2H
        var self=this;
    //            var domain =   [['create_uid', '=', this.ts_model.get('user').id],['chanel', '=', 'telesale']]
        var domain =   [['create_uid', '=', this.ts_model.get('user').id]]
        if (date_start != ""){
            utc_date_start = self.ts_model.parse_str_date_to_utc(date_start + " 00:00:00")
            domain.push(['date_order', '>=', utc_date_start])
        }
        if (date_end != ""){
            utc_date_end = self.ts_model.parse_str_date_to_utc(date_end + " 23:59:59")
            domain.push(['date_order', '<=', utc_date_end])
        }
        var loaded = self.ts_model.fetch('sale.order',
                                        ['name','partner_id','date_order','state','amount_total','date_invoice', 'date_planned', 'date_invoice'],  //faltan los impuestos etc
                                        domain)
            .then(function(orders){
            self.partner_orders = orders;
             })

        return loaded;
    },
    searchCustomerOrders: function () {
        var self=this;
        // var partner_name = this.$('#input-customer2').val();
        var date_start = this.$('#input-date_start2').val();
        var date_end = this.$('#input-date_end2').val();

            $.when(this.load_partner_orders(date_start,date_end))
            .done(function(){
                self.renderElement();
            }).fail(function(){
                //?????
            });
        // };
    },
    searchCustomerOrdersBy: function (period){
        var self=this;
        var start_date = new Date();
        var end_date_str = this.ts_model.getCurrentDateStr()
        if (period == 'week')
            start_date.setDate(start_date.getDate() - 30);
        else if (period == 'month')
            start_date.setDate(start_date.getDate() - 30);
        else if (period == 'trimester')
            start_date.setDate(start_date.getDate() - 90);
        var start_date_str = this.ts_model.dateToStr(start_date);

            $.when(this.load_partner_orders(start_date_str,end_date_str))
            .done(function(){
                self.renderElement();
            }).fail(function(){
                //?????
            });

        }
    });
return exports;
});
