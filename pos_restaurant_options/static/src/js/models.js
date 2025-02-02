/** @odoo-module **/

import Registries from 'point_of_sale.Registries';
import { Order, Orderline } from 'point_of_sale.models';



const PosOptOrder = (Order) => 
    class extends Order {

         /* Overwritten because the function has no return */

        add_product(product, options) {
            super.add_product(...arguments);
            if (options.selected_attribute_value_ids) {
                this.selected_orderline.set_selected_attribute_value_ids(options.selected_attribute_value_ids);
            }
        }
    }

Registries.Model.extend(Order, PosOptOrder);

const PosOptOrderline = (Orderline) =>
    class extends Orderline {

        constructor(obj, options) {
            super(obj, options);
            this.selected_attribute_value_ids = this.selected_attribute_value_ids || [];
        }

        // se puede eliminar la variable selected_attribute_value_ids
        get_selected_attribute_value_ids() {
            return this.selected_attribute_value_ids;
        }

        set_selected_attribute_value_ids(value) {
            this.selected_attribute_value_ids = value;
        }

        export_as_JSON() {
            var json = super.export_as_JSON();
            json.selected_attribute_value_ids = this.selected_attribute_value_ids;
            return json;
        }

        init_from_JSON(json) {
            super.init_from_JSON(json);
            this.selected_attribute_value_ids = json.selected_attribute_value_ids;
        }
    }

Registries.Model.extend(Orderline, PosOptOrderline);