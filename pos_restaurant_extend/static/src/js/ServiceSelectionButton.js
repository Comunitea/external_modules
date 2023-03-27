odoo.define('pos_restaurant_extend.ServiceSelectionButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const { Gui } = require('point_of_sale.Gui');
    var core = require('web.core');
    var QWeb = core.qweb;

    var _t   = core._t;

    class ServiceSelectionButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        get selectedOrderline() {
            return this.env.pos.get_order().get_selected_orderline();
        }
        async onClick() {
            if (!this.selectedOrderline) return;

            var service_level = this.env.pos.config.service_level;
            var list = [];
            for (var n = 1; n <= service_level; n++) {
                list.push({ label: '#' + n,  item: n, id: n });
            }

            const { confirmed, payload: selectedService } = await Gui.showPopup(
                'SelectionPopup',
                {
                    title: _t('Order'),
                    list: list,
                }
            );
            if (confirmed) {
                this.selectedOrderline.set_position(parseInt(selectedService));
            }
        }
    }
    ServiceSelectionButton.template = 'ServiceSelectionButton';

    ProductScreen.addControlButton({
        component: ServiceSelectionButton,
        condition: function() {
            return true;
        },
    });

    Registries.Component.add(ServiceSelectionButton);

    return ServiceSelectionButton;
});
