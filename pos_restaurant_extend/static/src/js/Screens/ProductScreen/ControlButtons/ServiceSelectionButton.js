/** @odoo-module **/

import Registries from 'point_of_sale.Registries';
import { Gui } from 'point_of_sale.Gui';
import PosComponent from 'point_of_sale.PosComponent';
import ProductScreen from 'point_of_sale.ProductScreen';
import { _t } from 'web.core';


class ServiceSelectionButton extends PosComponent{

    get selectedOrderLine(){
        return this.env.pos.get_order().get_selected_orderline();
    }

    async onClick() {
        if (!this.selectedOrderLine) return;

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
            this.selectedOrderLine.set_position(parseInt(selectedService));
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