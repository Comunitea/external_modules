/** @odoo-module **/

import Registries from 'point_of_sale.Registries';
import TableWidget from 'pos_restaurant.TableWidget';


const PostExtTableWidget = (TableWidget) =>
    class extends TableWidget {

        get posPrintedStyle(){
            const table = this.props.table;
            if (table.pos_printed) {
                var style = 'background-image: linear-gradient(black '+ (100 - table.pos_printed) + '%, red '+ table.pos_printed + '%);'
                return style
            } else {
                return;
            }
        }
    };

Registries.Component.extend(TableWidget, PostExtTableWidget);