/** @odoo-module **/

import Registries from 'point_of_sale.Registries';
import { PosGlobalState, Order, Orderline, Payment } from 'point_of_sale.models';
import { _t, qweb } from 'web.core';

const PosRestaurantPosGlobalStateExtended = (PosGlobalState) =>
    class extends PosGlobalState {
        constructor(obj){
            super(obj);
            this.failed_orders_to_sync = [];
            this.show_guests = false;
        }

        async setTable(table, orderUid=null) {
            const currentOrder = this.getTableOrders(table.id).find(order => orderUid ? order.uid === orderUid : !order.finalized);
            this.show_guests =  eval(!currentOrder && this.config.show_guests_popup) ;
            return await super.setTable(table, orderUid);
        }

        async load_orders() {
            if(this.config.cash_control && this.pos_session.state == 'opening_control') {
                this.env.pos.db.remove_all_unpaid_orders();
            }
            return await super.load_orders();
        }

        _save_to_server (orders, options) {
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
            this.set_synch('connecting', orders.length);
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
            return this.env.services.rpc({
                    model: 'pos.order',
                    method: 'create_from_ui',
                    args: args,
                    kwargs: {context: this.env.session.user_context},
                }, {
                    timeout: timeout,
                    shadow: !options.to_invoice
                })
                .then(function (server_ids) {
                    _.each(order_ids_to_sync, function (order_id) {
                        self.db.remove_order(order_id);
                    });
                    self.failed = false;// En la 14 esto se quita al heredar
                    self.failed_orders_to_sync = [];
                    self.set_synch('connected');
                    return server_ids;
                }).catch(function (reason){
                    console.warn('Failed to send orders:', orders);
                    if (reason.message.data && reason.message.data.name == 'odoo.exceptions.AccessDenied'){
                        window.location.reload();
                    }
                    _.each(orders, function (order) {
                        if ($.inArray(order, self.failed_orders_to_sync) < 0){
                            self.failed_orders_to_sync.push(order);
                        }
                    });
                    if(error.code === 200 ){    // Business Logic Error, not a connection problem
                        // Hide error if already shown before ...
                        if ((!self.failed || options.show_error) && !options.to_invoice) {
                            self.failed = error;
                            self.set_synch('error');
                            throw error;
                        }
                    }
                    self.set_synch('disconnected');
                    throw error;
                });

        }

        async transferTable(table) {
            var curr_table = this.tables_by_id[this.orderToTransfer.tableId]
            var final_table = table;
            await super.transferTable(table);
            var data = await this.computeTransferData(curr_table, final_table);
            console.log(data);
            this.print_transfer(curr_table, final_table);
        }
        
        async print_transfer(curr_table, final_table){
            var printers = this.unwatched.printers;
            let isPrintSuccessful = true;
            for (var i = 0; i < printers.length; i++) {
                if (printers[i].config.name == 'Cocina') {
                    var data = await this.computeTransferData(curr_table, final_table);
                    var receipt = qweb.render('PrintTableTransfer', { data: data, widget: this });
                    const result = await printers[i].print_receipt(receipt);
                    if (!result.successful) {
                        isPrintSuccessful = false;
                    }
                }
            }
            return isPrintSuccessful;

        }

        async computeTransferData(curr_table, final_table) {
            var d = new Date();
            var day = String(d.getDate()).padStart(2, '0');
            var month = String(d.getMonth() + 1).padStart(2, '0'); // Los meses en JS van de 0 a 11
            var year = d.getFullYear();
            var hours = String(d.getHours()).padStart(2, '0');
            var minutes = String(d.getMinutes()).padStart(2, '0');

            var cashier = this.get_cashier();
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

    };

Registries.Model.extend(PosGlobalState, PosRestaurantPosGlobalStateExtended);