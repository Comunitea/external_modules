odoo.define('pos_restaurant_extend.PrintServeServiceButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const { Gui } = require('point_of_sale.Gui');
    var core = require('web.core');
    var QWeb = core.qweb;
    var _t   = core._t;

    class PrintServeServiceButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }

        get selectedOrder() {
            return this.env.pos.get_order();
        }

        get nService() {
            return this.selectedOrder ? this.selectedOrder.get_last_requested_service() : 0;
        }

        get username() {
            const cashier = this.env.pos.get_cashier();
            if (cashier) {
                return cashier.name.split(" ")[0];
            } else {
                return '';
            }
        }

        async computeData(selectedService) {
            var json = this.selectedOrder.export_as_JSON();
            var d = new Date();
            var day = '' + d.getDate();
            var month = '' + d.getMonth();
                month = month + 1
                month = month.length < 2 ? ('0' + month) : month;
            var year = '' + d.getFullYear();
            var day = '' + d.getDate();
            var hours = '' + d.getHours();
                hours = hours.length < 2 ? ('0' + hours) : hours;
            var minutes = '' + d.getMinutes();
                minutes = minutes.length < 2 ? ('0' + minutes) : minutes;
            var user = this.username;
            var msg = '';

            switch(selectedService) {
                case 1:
                    msg = 'MARCHAR PRIMEROS';
                    break;
                case 2:
                    msg = 'MARCHAR SEGUNDOS';
                    break;
                case 3:
                    msg = 'MARCHAR TERCEROS';
                    break;
                case 4:
                    msg = 'MARCHAR CUARTOS';
                    break;
                case 5:
                    msg = 'MARCHAR QUINTOS';
                    break;
                case 6:
                    msg = 'MARCHAR SEXTOS';
                    break;
                case 7:
                    msg = 'MARCHAR SÉPTIMOS';
                    break;
                case 8:
                    msg = 'MARCHAR OCTAVOS';
                    break;
                case 9:
                    msg = 'MARCHAR NOVENOS';
                    break;
                case 10:
                    msg = 'MARCHAR DÉCIMOS';
                }

            return {
                'user': user,
                'table': json.table || false,
                'floor': json.floor || false,
                'name': json.name || 'unknown order',
                'customer_count': json.customer_count || false,
                'time': {
                    'day': day,
                    'month': month,
                    'year': year,
                    'hours': hours,
                    'minutes': minutes,
                },
                'msg': msg,
            };
        }

        async onClick() {

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
                this.printSelectedService(parseInt(selectedService));
                this.showScreen('FloorScreen', { floor: this.floor });
            }
        }

        async printSelectedService(selectedService) {
            this.selectedOrder.set_last_requested_service(selectedService);
            let isPrintSuccessful = true;
            var printers = this.env.pos.printers;
            for (var i = 0; i < printers.length; i++) {
                if (printers[i].config.name == 'Cocina') {
                    var data = await this.computeData(selectedService);
                    var receipt = QWeb.render('PrintServeServiceReceipt', { data: data, widget: this });
                    const result = await printers[i].print_receipt(receipt);
                    if (!result.successful) {
                        isPrintSuccessful = false;
                    }
                }
            }
            return isPrintSuccessful;
        }
    }
    PrintServeServiceButton.template = 'PrintServeServiceButton';

    ProductScreen.addControlButton({
        component: PrintServeServiceButton,
        condition: function() {
            return true;
        },
    });

    Registries.Component.add(PrintServeServiceButton);

    return PrintServeServiceButton;
});
