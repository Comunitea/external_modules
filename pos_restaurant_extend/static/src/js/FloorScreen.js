odoo.define('pos_restaurant_extend.FloorScreen', function(require) {
    'use strict';

    const FloorScreen = require('pos_restaurant.FloorScreen');
    const Registries = require('point_of_sale.Registries');

    const PosExtFloorScreen = FloorScreen =>
        class extends FloorScreen {
            /**
             * @override
             * Adds the pos_printed val to the table_obj
             */
            async _tableLongpolling() {
                if (this.state.isEditMode) {
                    return;
                }
                try {
                    const result = await this.rpc({
                        model: 'pos.config',
                        method: 'get_tables_order_count',
                        args: [this.env.pos.config.id],
                    });
                    result.forEach((table) => {
                        const table_obj = this.env.pos.tables_by_id[table.id];
                        const unsynced_orders = this.env.pos
                            .get_table_orders(table_obj)
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
                    this.render();
                } catch (error) {
                    if (error.message.code < 0) {
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

    Registries.Component.extend(FloorScreen, PosExtFloorScreen);

    return FloorScreen;
});
