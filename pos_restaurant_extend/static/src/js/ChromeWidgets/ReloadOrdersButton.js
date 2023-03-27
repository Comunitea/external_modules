odoo.define('pos_restaurant_extend.ReloadOrdersButton', function (require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const { posbus } = require('point_of_sale.utils');


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

    return ReloadOrdersButton;
});
