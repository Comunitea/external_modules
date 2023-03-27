odoo.define('pos_restaurant_extend.SubmitOrderButton', function(require) {
    'use strict';

    const SubmitOrderButton = require('pos_restaurant.SubmitOrderButton');
    const Registries = require('point_of_sale.Registries');

    const PosExtSubmitOrderButton = SubmitOrderButton =>
        class extends SubmitOrderButton {
            /**
             * @override
             * closes the table on print to force autosave.
             */
            async onClick() {
                const order = this.env.pos.get_order();
                if (order.hasChangesToPrint()) {
                    const isPrintSuccessful = await order.printChanges();
                    if (isPrintSuccessful) {
                        order.saveChanges();
                        this.showScreen('FloorScreen', { floor: this.floor });
                    } else {
                        await this.showPopup('ErrorPopup', {
                            title: 'Printing failed',
                            body: 'Failed in printing the changes in the order',
                        });
                    }
                }
            }
        };

    Registries.Component.extend(SubmitOrderButton, PosExtSubmitOrderButton);

    return SubmitOrderButton;
});
