/** @odoo-module **/

import Registries from 'point_of_sale.Registries';
import PosComponent from 'point_of_sale.PosComponent';


class ReloadOrdersButton extends PosComponent {
    async onClick() {
        const { confirmed } = await this.showPopup('ConfirmPopup', {
            title: this.env._t('Delete Unpaid Orders ?'),
            body: this.env._t(
                'This operation will destroy all unpaid orders in the browser. You will lose all the unsaved data and exit the point of sale. This operation cannot be undone.'
            ),
        });
        if (confirmed) {
            this.env.pos.db.remove_all_unpaid_orders();
            window.location = '/pos/ui';
        }
    }
}

ReloadOrdersButton.template = 'ReloadOrdersButton';

Registries.Component.add(ReloadOrdersButton);

