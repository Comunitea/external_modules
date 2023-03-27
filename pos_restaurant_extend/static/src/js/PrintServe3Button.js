odoo.define('pos_restaurant_extend.PrintServe3Button', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    var core = require('web.core');
    var QWeb = core.qweb;

    class PrintServe3Button extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }

        get selectedOrder() {
            return this.env.pos.get_order();
        }

        async computeData() {
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
            var user = false
            if (json.user_id) {
                for (var i in this.env.pos.users) {
                    if (this.env.pos.users[i].id == json.user_id) {
                        user = this.env.pos.users[i].name;
                    }
                }
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
            };
        }

        async onClick() {
            let isPrintSuccessful = true;
            var printers = this.env.pos.printers;
            for (var i = 0; i < printers.length; i++) {
                if (printers[i].config.name == 'Cocina') {
                    var data = await this.computeData();
                    var receipt = QWeb.render('Serve3Receipt', { data: data, widget: this });
                    const result = await printers[i].print_receipt(receipt);
                    if (!result.successful) {
                        isPrintSuccessful = false;
                    }
                }
            }
            return isPrintSuccessful;
        }
    }
    PrintServe3Button.template = 'PrintServe3Button';

    ProductScreen.addControlButton({
        component: PrintServe3Button,
        condition: function() {
            return true;
        },
    });

    Registries.Component.add(PrintServe3Button);

    return PrintServe3Button;
});
