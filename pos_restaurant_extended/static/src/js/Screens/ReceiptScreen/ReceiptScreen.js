/** @odoo-module **/

import Registries from 'point_of_sale.Registries';
import ReceiptScreen from 'point_of_sale.ReceiptScreen';

const PosExtReceiptScreen = (ReceiptScreen) =>
    class extends ReceiptScreen {
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