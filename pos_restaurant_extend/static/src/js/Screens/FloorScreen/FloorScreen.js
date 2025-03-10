/** @odoo-module **/

import FloorScreen  from 'pos_restaurant.FloorScreen';
import Registries from 'point_of_sale.Registries';
import { isConnectionError } from 'point_of_sale.utils';


const PostExtFloorScreen = (FloorScreen) =>
    class extends FloorScreen {
        setup() {
            super.setup();
        }

        /**
         * @override
         * Adds the pos_printed val to the table_obj
         */

        async _tableLongpolling() {
            if (this.state.isEditMode){
                return;
            }
            try{
                const result = await this.rpc({
                    model: 'pos.config',
                    method: 'get_tables_order_count',
                    args: [this.env.pos.config.id],
                });
                result.forEach((table) => {
                    const table_obj = this.env.pos.tables_by_id[table.id];
                    if (table_obj === undefined) {
                        console.warn(`Table with id ${table.id} is not found in the POS`);
                        return; // skip the table
                    }
                    const unsynced_orders = this.env.pos
                        .getTableOrders(table_obj.id)
                        .filter(
                            (o) =>
                                o.server_id === undefined &&
                                (o.orderlines.length !== 0 || o.paymentlines.length !== 0) &&
                                // do not count the orders that are already finalized
                                !o.finalized
                        ).length;
                    table_obj.order_count = table.orders + unsynced_orders;
                    table_obj.pos_printed = table.pos_printed;
                });

            }catch (error) {
                if (isConnectionError(error)) {
                    await this.showPopup('OfflineErrorPopup', {
                        title: 'Offline',
                        body: 'Unable to get orders count',
                    });
                } else {
                    throw error;
                }
            }
        }
    };

Registries.Component.extend(FloorScreen, PostExtFloorScreen);
