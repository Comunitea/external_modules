/** @odoo-module **/

import Registries from 'point_of_sale.Registries';
import { Order } from 'point_of_sale.models';
import { qweb } from 'web.core';

const PosExtOrderMultiprint = (Order) =>
    class extends Order {
        updatePrintedResume(){
            // we first remove the removed orderlines
            for (const lineKey in this.printedResume) {
                if (!this._getPrintedLine(lineKey)) {
                    delete this.printedResume[lineKey];
                }
            }
            // we then update the added orderline or product quantity change
            this.orderlines.forEach(line => {
                if (!line.mp_skip) {
                    const note = line.get_note();
                    const lineKey = `${line.uuid} - ${note}`;
                    if (this.printedResume[lineKey]) {
                        this.printedResume[lineKey]['quantity'] = line.get_quantity();
                    } else {
                        this.printedResume[lineKey] = {
                            line_uuid: line.uuid,
                            product_id: line.get_product().id,
                            position: line.get_position(),
                            name: line.get_full_product_name(),
                            note: note,
                            quantity: line.get_quantity(),
                        }
                    }
                    line.set_dirty(false);
                }
            });
            this._resetPrintingChanges();
        }

        async printChanges(){
            let isPrintSuccessful = true;
            const d = new Date();
            let hours = '' + d.getHours();
            hours = hours.length < 2 ? ('0' + hours) : hours;
            let minutes = '' + d.getMinutes();
            minutes = minutes.length < 2 ? ('0' + minutes) : minutes;

            let full_date = d.getFullYear() + '/' +
            (d.getMonth() + 1) + 
            '/' + d.getDate() + 
            ' ' + hours + ':' + minutes;
    
            for (const printer of this.pos.unwatched.printers) {
                const changes = this._getPrintingCategoriesChanges(printer.config.product_categories_ids);
                if (printer.config.name == 'Cocina') {
                    changes["spaces"] = true;
                }
                if (changes['new'].length > 0 || changes['cancelled'].length > 0) {
                    var cashier = this.pos.get_cashier();
                    var user = cashier ? cashier.name.split(' ')[0] : '';
                    const printingChanges = {
                        new: changes['new'],
                        cancelled: changes['cancelled'],
                        user: user,
                        table_name: this.pos.config.iface_floorplan ? this.getTable().name : false,
                        floor_name: this.pos.config.iface_floorplan ? this.getTable().floor.name : false,
                        name: this.name || 'unknown order',
                        time: {
                            hours,
                            minutes,
                        },
                        date: full_date,
                        customer_count: this.customer_count || false,
                    };
                    const receipt = qweb.render('OrderChangeReceipt', { changes: printingChanges });
                    const result = await printer.print_receipt(receipt);
                    if (!result.successful) {
                        isPrintSuccessful = false;
                    }
                }
            }
           return isPrintSuccessful;
        }

        _getPrintingCategoriesChanges(categories) {
            var add = this.printingChanges['new'].filter(change => this.pos.db.is_product_in_category(categories, change['product_id']));
            var cancel = this.printingChanges['cancelled'].filter(change => this.pos.db.is_product_in_category(categories, change['product_id']));

            add.sort(function(a, b) {
                if (a.position === b.position) {
                    return a.note > b.note ? 1 : -1;
                }
                return a.position > b.position ? 1 : -1;
            });
            cancel.sort(function(a, b) {
                if (a.position === b.position) {
                    return a.note > b.note ? 1 : -1;
                }
                return a.position > b.position ? 1 : -1;
            });

            return {
                new: add,
                cancelled: cancel,
            }
        }

        _computePrintChanges() {
            const changes = {};
    
            // If there's a new orderline, we add it otherwise we add the change if there's one
            this.orderlines.forEach(line => {
                if (!line.mp_skip) {
                    const productId = line.get_product().id;
                    const note = line.get_note();
                    const productKey = `${productId} - ${line.get_full_product_name()} - ${note}`;
                    const lineKey = `${line.uuid} - ${note}`;
                    const quantityDiff = line.get_quantity() - (this.printedResume[lineKey] ? this.printedResume[lineKey]['quantity'] : 0);
                    const position = line.get_position();
                    if (quantityDiff) {
                        if (!changes[productKey]) {
                            changes[productKey] = {
                                product_id: productId,
                                position: position,
                                name: line.get_full_product_name(),
                                note: note,
                                quantity: quantityDiff,
                            }
                        } else {
                            changes[productKey]['quantity'] += quantityDiff;
                        }
                        line.set_dirty(true);
                    } else {
                        line.set_dirty(false);
                    }
                }
            })
    
            // If there's an orderline that's not present anymore, we consider it as removed (even if note changed)
            for (const [lineKey, lineResume] of Object.entries(this.printedResume)) {
                if (!this._getPrintedLine(lineKey)) {
                    const productKey = `${lineResume['product_id']} - ${lineResume['name']} - ${lineResume['note']}`;
                    if (!changes[productKey]) {
                        changes[productKey] = {
                            product_id: lineResume['product_id'],
                            name: lineResume['name'],
                            note: lineResume['note'],
                            quantity: -lineResume['quantity'],
                            position: lineResume['position'],
                        }
                    } else {
                        changes[productKey]['quantity'] -= lineResume['quantity'];
                    }
                }
            }
    
            return changes;
        }
   
};
Registries.Model.extend(Order, PosExtOrderMultiprint);