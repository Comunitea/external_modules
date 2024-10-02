/** @odoo-module **/

import Registries from 'point_of_sale.Registries';
import ReceiptScreen from 'point_of_sale.ReceiptScreen';

const PosExtReceiptScreen = (ReceiptScreen) =>
    class extends ReceiptScreen {
        async printReceipt() {
            await super.printReceipt();
            if (!this.currentOrder.finalized) {
                this.currentOrder.initialize_validation_date();
                this.currentOrder.set_pos_printed(true);
            }
        }

        // get currentOrder() {
        //     var order = super.currentOrder;
        //     //order.initialize_validation_date(); ESTO IMPIDE QUE SE IMPRIMA LA FACTURA
        //     return order;
        // }

        _shouldAutoPrint() {
            return this.env.pos.config.iface_not_autoprint_cash && this.currentOrder.has_only_cash_payment() ? false : super._shouldAutoPrint();
        }
    };

Registries.Component.extend(ReceiptScreen, PosExtReceiptScreen);