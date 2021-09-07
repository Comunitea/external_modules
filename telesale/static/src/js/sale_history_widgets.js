odoo.define('telesale.SaleHistory', function (require) {
"use strict";

var TsBaseWidget = require('telesale.TsBaseWidget');
var models = require('telesale.models');
var rpc = require('web.rpc');
var core = require('web.core');
var _t = core._t;
var session = require('web.session');


var exports = {}

exports.SaleHistoryLineWidget = TsBaseWidget.extend({
    template:'Sale-History-Line-Widget',
    init: function(parent, options){
        this._super(parent,options);
        this.sale_line = options.line;
    },

    get_line_obj: function(){
        var line = this.sale_line;
        return line;
    },
    add_product_to_order: function(no_refresh) {
        this.ts_model.delete_if_empty_line();
        var self=this;
        var product_id = this.sale_line.product_id
        if (product_id){
            var current_order= this.ts_model.get('selectedOrder')
            // current_order.addProductLine(product_id);
            var order_widget = this.ts_widget.new_order_screen.order_widget

            // Get qty to add and current pricelist price to add (default is the sale_order_line_price)
            var qty = this.ts_model.my_str2float(  this.$('#add-qty-sh').val() );
            var price = this.ts_model.my_str2float(  this.$('#add-price-sh').val() );
            if (qty == 0){
                return;
            }
            var vals = {
                'qty': qty,
                'price':  price,
                'discount': this.sale_line.discount,
                'taxes_ids': this.sale_line.taxes_ids || [],
            }
            order_widget.create_line_from_vals(product_id, vals)
            if (no_refresh)
                return;
            order_widget.renderElement(); 
            self.ts_widget.new_order_screen.totals_order_widget.changeTotals();
            $('button#button_no').click();
        }
    },
    renderElement: function() {
        var self=this;
        this._super();
        this.$('.add-history-line').click(function (){ 
            self.add_product_to_order(false);
        });
    },
});






exports.SaleHistoryWidget = TsBaseWidget.extend({
    template:'Sale-History-Widget',
    
    init: function(parent, options) {
        var self = this;
        this._super(parent,options);
        this.history_lines = [];
        this.page = 1;  // To do the offset search
        this.limit = 50; // To do the offset search
        this.result_str = "";
        this.line_widgets = [];
        this.partner_name = ''
    },


    load_sale_history_from_server: function(){
        var self=this;
        // Wee need the partner to ger the product price from server.
        var offset = (this.page - 1) * this.limit;
        var current_order = this.ts_model.get('selectedOrder');
        self.partner_name = current_order.get('partner')
        var partner_id = this.ts_model.db.partner_name_id[current_order.get('partner')];
        var pricelist_id = this.ts_model.db.pricelist_name_id[current_order.get('pricelist')];
        var loaded = rpc.query({model: 'sale.order.line', method: 'ts_get_sale_history', args:[partner_id, pricelist_id, offset, self.limit], kwargs: {context: session.user_context}})
        .then(function(result){
            self.history_lines = result['history_lines'];
            self.result_str = result['result_str'];
            self.renderElement();
        });
        return loaded;

    },

    add_all_lines: function() {
        var self = this;
        for (var key in self.line_widgets){
            var line_obj = self.line_widgets[key];
            line_obj.add_product_to_order(true);  // true passed to no_refresh
        }
        var order_widget = this.ts_widget.new_order_screen.order_widget
        self.ts_widget.new_order_screen.totals_order_widget.changeTotals();
        order_widget.renderElement(); 
        $('button#button_no').click();
    },

    bind_onchange_events: function(){
        // this.$('.add-qty').unbind();
        // this.$('.add-price').unbind();
        // this.$('.add-discount').unbind();

        var self=this;
        this.$('.add-qty-sh').bind('change', function(event){
             self.ts_model.check_float(this);
            //  self.call_product_uom_change(this);
        });
        this.$('.add-price-sh').bind('change', function(event){
             self.ts_model.check_float(this);
        });
    },

    renderElement: function () {
        var self = this;
        this._super();
        // Destroy line widgets
        for(var i = 0, len = this.line_widgets.length; i < len; i++){
            this.line_widgets[i].destroy();
        }
        this.line_widgets = [];
        var $lines_content = this.$('.salehistorylines');
        for (var key in this.history_lines){
            var line_obj = self.history_lines[key];
            var history_line = new exports.SaleHistoryLineWidget(self, {line: line_obj});
            history_line.appendTo($lines_content);
            self.line_widgets.push(history_line);
        }

        this.$('#search-history-prev').click(function (){
            if (self.page > 1) 
                self.page = self.page - 1;
            self.load_sale_history_from_server();
        });
        this.$('#search-history-next').click(function (){ 
            self.page = self.page + 1;
            self.load_sale_history_from_server();
        });
        this.$('#add-all-lines').click(function (){ 
            self.add_all_lines();
        });
        this.bind_onchange_events();
    },
});




return exports

});
