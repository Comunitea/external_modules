odoo.define('pos_restaurant_extend.TableWidget', function(require) {
    'use strict';

    const TableWidget = require('pos_restaurant.TableWidget');
    const Registries = require('point_of_sale.Registries');

    const PosExtTableWidget = TableWidget =>
        class extends TableWidget {
            /**
             * @override
             */
            get posPrintedStyle() {
                const table = this.props.table;
                if (table.pos_printed) {
                    var style = 'background-image: linear-gradient(black '+ (100 - table.pos_printed) + '%, red '+ table.pos_printed + '%);'
                    return style
                } else {
                    return false;
                }
            }
        };

    Registries.Component.extend(TableWidget, PosExtTableWidget);

    return TableWidget;
});
