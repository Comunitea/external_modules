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



/* <script type="text/javascript" src="/pos_restaurant_extend/static/src/js/floors.js" /> NO
<script type="text/javascript" src="/pos_restaurant_extend/static/src/js/lines.js" /> SI
<script type="text/javascript" src="/pos_restaurant_extend/static/src/js/multiprint.js" /> NO
<script type="text/javascript" src="/pos_restaurant_extend/static/src/js/PrintServeServiceButton.js" /> SI
<script type="text/javascript" src="/pos_restaurant_extend/static/src/js/ServiceSelectionButton.js" /> SI 
<script type="text/javascript" src="/pos_restaurant_extend/static/src/js/ReceiptScreen.js" /> SI 
<script type="text/javascript" src="/pos_restaurant_extend/static/src/js/TableWidget.js" /> SI 
<script type="text/javascript" src="/pos_restaurant_extend/static/src/js/FloorScreen.js" /> SI 
<script type="text/javascript" src="/pos_restaurant_extend/static/src/js/ChromeWidgets/ReloadOrdersButton.js"></script>
<script type="text/javascript" src="/pos_restaurant_extend/static/src/js/SubmitOrderButton.js" /> SI 
FALTA REVISAR EL TEMA IMPRESIÓN
*/