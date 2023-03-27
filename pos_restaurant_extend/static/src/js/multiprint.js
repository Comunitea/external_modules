odoo.define('pos_restaurant_extend.multiprint', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var core = require('web.core');
    var QWeb = core.qweb;

    models.Order = models.Order.extend({
        /* Overwritten to add position */
        build_line_resume: function(){
            var resume = {};
            this.orderlines.each(function(line){
                if (line.mp_skip) {
                    return;
                }
                var qty  = Number(line.get_quantity());
                var note = line.get_note();
                var product_id = line.get_product().id;
                var product_name = line.get_full_product_name();
                var p_key = product_id + " - " + product_name;
                var position = line.get_position();
                var product_resume = p_key in resume ? resume[p_key] : {
                    pid: product_id,
                    position: position,
                    product_name_wrapped: line.generate_wrapped_product_name(),
                    qties: {},
                };
                if (note in product_resume['qties']) product_resume['qties'][note] += qty;
                else product_resume['qties'][note] = qty;
                resume[p_key] = product_resume;
            });
            return resume;
        },

        /* Overwritten to add position and user */
        computeChanges: function(categories){
            var current_res = this.build_line_resume();
            var old_res     = this.saved_resume || {};
            var json        = this.export_as_JSON();
            var add = [];
            var rem = [];
            var p_key, note;

            for (p_key in current_res) {
                for (note in current_res[p_key]['qties']) {
                    var curr = current_res[p_key];
                    var old  = old_res[p_key] || {};
                    var pid = curr.pid;
                    var found = p_key in old_res && note in old_res[p_key]['qties'];

                    if (!found) {
                        add.push({
                            'id':       pid,
                            'position': curr.position,
                            'name':     this.pos.db.get_product_by_id(pid).display_name,
                            'name_wrapped': curr.product_name_wrapped,
                            'note':     note,
                            'qty':      curr['qties'][note],
                        });
                    } else if (old['qties'][note] < curr['qties'][note]) {
                        add.push({
                            'id':       pid,
                            'position': curr.position,
                            'name':     this.pos.db.get_product_by_id(pid).display_name,
                            'name_wrapped': curr.product_name_wrapped,
                            'note':     note,
                            'qty':      curr['qties'][note] - old['qties'][note],
                        });
                    } else if (old['qties'][note] > curr['qties'][note]) {
                        rem.push({
                            'id':       pid,
                            'position': curr.position,
                            'name':     this.pos.db.get_product_by_id(pid).display_name,
                            'name_wrapped': curr.product_name_wrapped,
                            'note':     note,
                            'qty':      old['qties'][note] - curr['qties'][note],
                        });
                    }
                }
            }

            for (p_key in old_res) {
                for (note in old_res[p_key]['qties']) {
                    var found = p_key in current_res && note in current_res[p_key]['qties'];
                    if (!found) {
                        var old = old_res[p_key];
                        var pid = old.pid;
                        rem.push({
                            'id':       pid,
                            'position': old.position,
                            'name':     this.pos.db.get_product_by_id(pid).display_name,
                            'name_wrapped': old.product_name_wrapped,
                            'note':     note,
                            'qty':      old['qties'][note],
                        });
                    }
                }
            }

            if(categories && categories.length > 0){
                // filter the added and removed orders to only contains
                // products that belong to one of the categories supplied as a parameter

                var self = this;

                var _add = [];
                var _rem = [];

                for(var i = 0; i < add.length; i++){
                    if(self.pos.db.is_product_in_category(categories,add[i].id)){
                        _add.push(add[i]);
                    }
                }
                add = _add;

                for(var i = 0; i < rem.length; i++){
                    if(self.pos.db.is_product_in_category(categories,rem[i].id)){
                        _rem.push(rem[i]);
                    }
                }
                rem = _rem;
            }

            /* Sort by position */

            add.sort(function(a, b) {
                if (a.position === b.position) {
                    return a.note > b.note ? 1 : -1;
                }
                return a.position > b.position ? 1 : -1;
            });
            rem.sort(function(a, b) {
                if (a.position === b.position) {
                    return a.note > b.note ? 1 : -1;
                }
                return a.position > b.position ? 1 : -1;
            });

            var d = new Date();
            var hours   = '' + d.getHours();
                hours   = hours.length < 2 ? ('0' + hours) : hours;
            var minutes = '' + d.getMinutes();
                minutes = minutes.length < 2 ? ('0' + minutes) : minutes;
            var month = d.getMonth()+1;
            var day = d.getDate();
            var full_date = d.getFullYear() + '/' +
                (month<10 ? '0' : '') + month + '/' +
                (day<10 ? '0' : '') + day;

            /* Gets user */
            var user = false;
            const cashier = this.employee;
            if (cashier) {
                user = cashier.name.split(" ")[0];
            } else {
                user = '';
            }

            /* Adds user and customer_count */

            return {
                'new': add,
                'cancelled': rem,
                'user': user,
                'table': json.table || false,
                'floor': json.floor || false,
                'name': json.name  || 'unknown order',
                'time': {
                    'hours':   hours,
                    'minutes': minutes,
                },
                'date': full_date,
                'customer_count': this.customer_count,
            };

        },

        /* Overwritten to add changes.spaces */
        printChanges: async function(){
            var printers = this.pos.printers;
            let isPrintSuccessful = true;
            for(var i = 0; i < printers.length; i++){
                var changes = this.computeChanges(printers[i].config.product_categories_ids);
                if (printers[i].config.name == 'Cocina') {
                    changes["spaces"] = true;
                }
                if ( changes['new'].length > 0 || changes['cancelled'].length > 0){
                    var receipt = QWeb.render('OrderChangeReceipt',{changes:changes, widget:this});
                    const result = await printers[i].print_receipt(receipt);
                    if (!result.successful) {
                        isPrintSuccessful = false;
                    }
                }
            }
            return isPrintSuccessful;
        },

    });

});
