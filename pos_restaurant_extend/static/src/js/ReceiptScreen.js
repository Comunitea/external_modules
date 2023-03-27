odoo.define('pos_restaurant_extend.ReceiptScreen', function(require) {
    'use strict';

    const ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const Registries = require('point_of_sale.Registries');

    const PosExtReceiptScreen = ReceiptScreen =>
        class extends ReceiptScreen {
            /**
             * @override
             */
            async printReceipt() {
                await super.printReceipt();
                if (!this.currentOrder.finalized) {
                    this.currentOrder.set_pos_printed(true);
                }
            }
            get currentOrder() {
                var order = super.currentOrder;
                order.initialize_validation_date();
                return order;
            }
            _shouldAutoPrint() {
                if (this.env.pos.config.iface_not_autoprint_cash && this.currentOrder.has_only_cash_payment()) {
                    return false
                } else {
                    return super._shouldAutoPrint();
                }
            }
        };

    Registries.Component.extend(ReceiptScreen, PosExtReceiptScreen);

    return ReceiptScreen;
});
