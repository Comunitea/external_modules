odoo.define('pos_restaurant_extend.floors', function (require) {
    "use strict";

    require("web.dom_ready");
    require('pos_restaurant.floors');
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var QWeb = core.qweb;

    var _t   = core._t;

    var _super_posmodel = models.PosModel.prototype;

    models.PosModel = models.PosModel.extend({
        initialize: function () {
            _super_posmodel.initialize.apply(this, arguments);
            this.failed_orders_to_sync = [];
        },

        /* Moved from set_table (v12.0) */
        /* Overwritten to add the guests popup */

        set_order_on_table: function(order) {
            var orders = this.get_order_list();
            if (orders.length) {
                order = order ? orders.find((o) => o.uid === order.uid) : null;
                if (order) {
                    this.set_order(order);
                } else {
                    // do not mindlessly set the first order in the list.
                    orders = orders.filter(order => !order.finalized);
                    if (orders.length) {
                        this.set_order(orders[0]);
                    } else {
                        this.add_new_order();
                    }
                }
            } else {
                var new_order = this.add_new_order();  // or create a new order with the current table
                if (new_order) {
                    if(new_order.pos.config.show_guests_popup) {
                        /* Would be better to trigger the button calling the TableGuestsButton component but w/e */
                        $( document).ready(function() {
                            $(".control-button-number").parent().click();
                        });
                    }
                }
            }
        },

        load_orders: function() {
            if(this.env.pos.config.cash_control && this.env.pos.pos_session.state == 'opening_control') {
                this.env.pos.db.remove_all_unpaid_orders();
            }
            _super_posmodel.load_orders.apply(this, arguments);
        },

        _save_to_server: function (orders, options) {
            /* Overwritten to add failed_orders_to_sync variable */
            if (this.failed_orders_to_sync && this.failed_orders_to_sync.length > 0) {
                _.each(this.failed_orders_to_sync, function (failed_order) {
                    if ($.inArray(failed_order, orders) < 0){
                        orders.push(failed_order);
                    }
                });
            }
            if (!orders || !orders.length) {
                return Promise.resolve([]);
            }

            options = options || {};

            var self = this;
            var timeout = typeof options.timeout === 'number' ? options.timeout : 30000 * orders.length;

            // Keep the order ids that are about to be sent to the
            // backend. In between create_from_ui and the success callback
            // new orders may have been added to it.
            var order_ids_to_sync = _.pluck(orders, 'id');

            // we try to send the order. shadow prevents a spinner if it takes too long. (unless we are sending an invoice,
            // then we want to notify the user that we are waiting on something )
            var args = [_.map(orders, function (order) {
                    order.to_invoice = options.to_invoice || false;
                    return order;
                })];
            args.push(options.draft || false);
            return this.rpc({
                    model: 'pos.order',
                    method: 'create_from_ui',
                    args: args,
                    kwargs: {context: this.session.user_context},
                }, {
                    timeout: timeout,
                    shadow: !options.to_invoice
                })
                .then(function (server_ids) {
                    _.each(order_ids_to_sync, function (order_id) {
                        self.db.remove_order(order_id);
                    });
                    self.failed_orders_to_sync = [];
                    return server_ids;
                }).catch(function (reason){
                    if (reason.message.data && reason.message.data.name == 'odoo.exceptions.AccessDenied'){
                        window.location.reload();
                    }
                    _.each(orders, function (order) {
                        if ($.inArray(order, self.failed_orders_to_sync) < 0){
                            self.failed_orders_to_sync.push(order);
                        }
                    });
                    var error = reason.message;
                    if(error.code === 200 ){    // Business Logic Error, not a connection problem
                        // Hide error if already shown before ...
                        if ((!self.get('failed') || options.show_error) && !options.to_invoice) {
                            self.set('failed',error);
                            throw error;
                        }
                    }
                    throw error;
                });
        },

        transfer_order_to_table: function(table) {
            var curr_table = this.order_to_transfer_to_different_table.table;
            var final_table = table;
            _super_posmodel.transfer_order_to_table.apply(this, arguments);
            this.print_transfer(curr_table, final_table);
        },

        print_transfer: async function(curr_table, final_table) {
            var printers = this.env.pos.printers;
            for (var i = 0; i < printers.length; i++) {
                if (printers[i].config.name == 'Cocina') {
                    var data = await this.computeTransferData(curr_table, final_table);
                    var receipt = QWeb.render('PrintTableTransfer', { data: data, widget: this });
                    const result = await printers[i].print_receipt(receipt);
                    if (!result.successful) {
                        isPrintSuccessful = false;
                    }
                }
            }
        },

        async computeTransferData(curr_table, final_table) {
            var d = new Date();
            var day = '' + d.getDate();
            var month = '' + d.getMonth();
                month = month + 1
                month = month.length < 2 ? ('0' + month) : month;
            var year = '' + d.getFullYear();
            var day = '' + d.getDate();
            var hours = '' + d.getHours();
                hours = hours.length < 2 ? ('0' + hours) : hours;
            var minutes = '' + d.getMinutes();
                minutes = minutes.length < 2 ? ('0' + minutes) : minutes;
            var cashier = this.env.pos.get_cashier();
            var user = "";
            if (cashier) {
                user = cashier.name.split(" ")[0];
            }

            return {
                'user': user,
                'time': {
                    'day': day,
                    'month': month,
                    'year': year,
                    'hours': hours,
                    'minutes': minutes,
                },
                'curr_table': curr_table.name,
                'final_table': final_table.name,
            };
        }
    });

});
