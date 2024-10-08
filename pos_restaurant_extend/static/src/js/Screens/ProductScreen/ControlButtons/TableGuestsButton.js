/** @odoo-module **/


import Registries from 'point_of_sale.Registries';
import TableGuestsButton from 'pos_restaurant.TableGuestsButton';
import { onMounted } from '@odoo/owl';


const PosExtTableGuestsButton = (TableGuestsButton) => 
    class extends TableGuestsButton {
        
        setup() {
            super.setup();
            onMounted(() => {
                if (this.env.pos.show_guests) {
                    this.env.pos.show_guests = false;
                    this.onClick();
                }
            })
        }
    };

Registries.Component.extend(TableGuestsButton, PosExtTableGuestsButton);