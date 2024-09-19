/** @odoo-module **/

import Registries from 'point_of_sale.Registries';
import { PosGlobalState, Order, Orderline, Payment } from 'point_of_sale.models';

const PosRestaurantPosGlobalStateExtended = (PosGlobalState) =>
    class extends PosGlobalState {
        constructor(obj){
            super(obj);
            this.failed_orders_to_sync = [];
        }

        async setTable(table, orderUid=null) {
            this.table = table;
            try {
                this.loadingOrderState = true;
                await this._syncTableOrdersFromServer(table.id);
            } catch (error) {
                throw error;
            } finally {
                this.loadingOrderState = false;
                const currentOrder = this.getTableOrders(table.id).find(order => orderUid ? order.uid === orderUid : !order.finalized);
                if (currentOrder) {
                    this.set_order(currentOrder);
                } else {
                   var new_order=this.add_new_order();
                   if (new_order.pos.config.show_guests_popup) {
                    //BUSCAR UNA FORMA MEJOR DE HACER ESTO
                    $(document).ready(function() {
                        $(".control-button-number").parent().trigger("click");
                    });
                   }
                }
            }
        }

        async load_orders() {
            if(this.config.cash_control && this.pos_session.state == 'opening_control') {
                this.env.pos.db.remove_all_unpaid_orders();
            }
            await super.load_orders();
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
    };

Registries.Model.extend(PosGlobalState, PosRestaurantPosGlobalStateExtended);