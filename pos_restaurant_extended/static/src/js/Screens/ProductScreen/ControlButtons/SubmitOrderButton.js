/** @odoo-module **/

import SubmitOrderButton from 'pos_restaurant.SubmitOrderButton';
import Registries from 'point_of_sale.Registries';

const PosExtSubmitOrderButton = (SubmitOrderButton) =>
    class extends SubmitOrderButton {
        async _onClick() {
            if (!this.clicked) {
                try {
                    this.clicked = true;
                    const order = this.env.pos.get_order();
                    const table = order.getTable();
                    const floor = table.floor;
                    if (order.hasChangesToPrint()) {
                        const isPrintSuccessful = await order.printChanges();
                        if (isPrintSuccessful) {
                            order.updatePrintedResume();
                            this.showScreen('FloorScreen', { floor: floor });
                        } else {
                            this.showPopup('ErrorPopup', {
                                title: this.env._t('Printing failed'),
                                body: this.env._t('Failed in printing the changes in the order'),
                            });
                        }
                    }
                } finally {
                    this.clicked = false;
                }
            }
        }
    };

Registries.Component.extend(SubmitOrderButton, PosExtSubmitOrderButton);