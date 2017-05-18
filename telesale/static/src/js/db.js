
odoo.define('telesale.db', function (require) {
"use strict";

var core = require('web.core');
var _t = core._t;

var exports = {};

exports.TS_LS = core.Class.extend({
    name: 'openerp_ts_ls', //the prefix of the localstorage data
    limit: 100,            // the maximum number of results returned by a search
    init: function(options){
        options = options || {};
        this.name = options.name || this.name;
        this.limit = options.limit || this.limit;

        //cache the data in memory to avoid roundtrips to the localstorage
        this.cache = {};

        //PRODUCTS DB
        this.product_by_id = {};
        this.product_by_tmp_id = {};
        this.product_code_id = {};
        this.product_name_id = {};

        // PARTNERS DB
        this.partner_sorted = [];
        this.partner_by_id = {};
        this.partner_ref_id = {};
        this.partner_name_id = {};
        this.partner_search_string = "";
        this.partner_write_date = null;

        this.suppliers_name_id = {};
        this.supplier_from_name_to_id = {};

        this.tax_by_id = {};
        this.map_tax_by_id = {};
        this.fposition_by_id = {};

        this.unit_by_id = {};
        this.unit_name_id = {};
        this.all_units = {};
      
        this.cache_sold_lines = {};
    },

    /* loads a record store from the database. returns default if nothing is found */
    load: function(store,deft){
        if(this.cache[store] !== undefined){
            return this.cache[store];
        }
        var data = localStorage[this.name + '_' + store];
        if(data !== undefined){
            data = JSON.parse(data);
            this.cache[store] = data;
            return data;
        }else{
            return deft;
        }
    },
    /* saves a record store to the database */
    save: function(store,data){
        var str_data = JSON.stringify(data);
        localStorage[this.name + '_' + store] = JSON.stringify(data);
        this.cache[store] = data;
    },
    _product_search_string: function(product){
        var str = '' + product.id + ':' + product.display_name;
        if(product.default_code){
            str += '|' + product.default_code;
        }
        return str + '\n';
    },
    add_products: function(products){
        if(!products instanceof Array){
            products = [products];
        }
        for(var i = 0, len = products.length; i < len; i++){
            var product = products[i];
            // var search_string = this._product_search_string(product);
            this.product_by_id[product.id] = product;
            // this.product_by_tmp_id[product.product_tmpl_id[0]] = product;
            this.product_name_id[product.display_name] = product.id;
            if(product.default_code){
                this.product_code_id[product.default_code] = product.id;
            }
        }
    },
    add_units: function(units){
        if(!units instanceof Array){
            units = [units];
        }
        for(var i = 0, len = units.length; i < len; i++){
            var unit = units[i];

            this.unit_by_id[unit.id] = unit;
            this.unit_name_id[unit.name] = unit.id;
        }
        this.all_units = units
    },
    add_taxes: function(taxes){
        if(!taxes instanceof Array){
            taxes = [taxes];
        }
        for(var i = 0, len = taxes.length; i < len; i++){
            var tax = taxes[i];
            this.tax_by_id[tax.id] = tax;
        }
    },
    get_tax_by_id: function(id){
        return this.tax_by_id[id];
    },
    add_taxes_map: function(fpos_map){
        if(!fpos_map instanceof Array){
            fpos_map = [fpos_map];
        }
        for(var i = 0, len = fpos_map.length; i < len; i++){
            var map = fpos_map[i];
            var map_obj = {position_id: map.position_id[0], src_tax: map.tax_src_id[0], dest_tax: map.tax_dest_id[0], }
            this.map_tax_by_id[map.id] = map_obj;
        }
    },
    get_map_tax_by_id: function(id){
        return this.map_tax_by_id[id];
    },
    add_fiscal_position: function(fiscal_position){
        if(!fiscal_position instanceof Array){
            fiscal_position = [fiscal_position];
        }
        for(var i = 0, len = fiscal_position.length; i < len; i++){
            var fpos = fiscal_position[i];
            this.fposition_by_id[fpos.id] = fpos;
        }
    },
    get_fiscal_position_by_id: function(id){
        return this.fposition_by_id[id];
    },
    /* removes all the data from the database. TODO : being able to selectively remove data */
    clear: function(stores){
        for(var i = 0, len = arguments.length; i < len; i++){
            localStorage.removeItem(this.name + '_' + arguments[i]);
        }
    },
    get_product_by_id: function(id){
        return this.product_by_id[id];
    },
    // get_product_by_tmp_id: function(id){
    //     return this.product_by_tmp_id[id];
    // },
    get_product_by_code: function(code){
        if(this.product_by_code[code]){
            return this.product_by_code[code];
        }
        return undefined;
    },
    _partner_search_string: function(partner){
        var str = partner.name;
        // if (partner.ref){
        //     str += '|' + partner.ref;
        // }
        // if(partner.address){
        //     str += '|' + partner.adress;
        // }
         // if (partner.ref){
        //     str += '|' + partner.ref;
        // }
        if(partner.commercial_partner_name){
            str += '|' + partner.commercial_partner_name;
        }
        if(partner.street){
            str += '|' + partner.street;
        }
        if(partner.zip){
            str += '|' + partner.zip;
        }
        if(partner.city){
            str += '|' + partner.city;
        }
        if(partner.state_id){
            str += '|' + partner.state_id[0];
        }
        if(partner.phone){
            str += '|' + partner.phone.split(' ').join('');
        }
        if(partner.email){
            str += '|' + partner.email;
        }
        str = '' + partner.id + ':' + str.replace(':','') + '\n';
        return str
    },
    // add_partners: function(partners){
    //     if(!partners instanceof Array){
    //         partners = [partners];
    //     }
    //     for(var i = 0, len = partners.length; i < len; i++){
    //         var partner = partners[i];

    //         this.partner_by_id[partner.id] = partner;
    //         var cus_name = partner.name + ' | ' + partner.ref
    //         this.partner_name_id[cus_name] = partner.id;
    //         if(partner.ref){
    //             this.partner_ref_id[partner.ref] = partner.id;
    //         }
    //         var search_string = this._partner_search_string(partner);
    //         this.partner_search_string += search_string
    //     }
    // },
    get_partners_stored: function(max_count){
        max_count = max_count ? Math.min(this.partner_sorted.length, max_count) : this.partner_sorted.length;
        var partners = [];
        for (var i = 0; i < max_count; i++) {
            partners.push(this.partner_by_id[this.partner_sorted[i]]);
        }
        return partners;
    },
    search_partner: function(query){
        try {
            query = query.replace(/[\[\]\(\)\+\*\?\.\-\!\&\^\$\|\~\_\{\}\:\,\\\/]/g,'.');
            query = query.replace(' ','.+');
            var re = RegExp("([0-9]+):.*?"+query,"gi");
        }catch(e){
            return [];
        }
        var results = [];
        for(var i = 0; i < this.limit; i++){
            var r = re.exec(this.partner_search_string);
            if(r){
                var id = Number(r[1]);
                results.push(this.get_partner_by_id(id));
            }else{
                break;
            }
        }
        return results;
    },
    add_partners: function(partners){
        var updated_count = 0;
        var new_write_date = '';
        var partner;
        for(var i = 0, len = partners.length; i < len; i++){
            partner = partners[i];

            if (    this.partner_write_date && 
                    this.partner_by_id[partner.id] &&
                    new Date(this.partner_write_date).getTime() + 1000 >=
                    new Date(partner.write_date).getTime() ) {
                // FIXME: The write_date is stored with milisec precision in the database
                // but the dates we get back are only precise to the second. This means when
                // you read partners modified strictly after time X, you get back partners that were
                // modified X - 1 sec ago. 
                continue;
            } else if ( new_write_date < partner.write_date ) { 
                new_write_date  = partner.write_date;
            }
            if (!this.partner_by_id[partner.id]) {
                this.partner_sorted.push(partner.id);
            }
            this.partner_by_id[partner.id] = partner;

            updated_count += 1;

            // TODO IMPROVE como obtener el id del partner, partner_name_id no es lo mejor
            var cus_name = partner.name + ' | ' + partner.ref
            this.partner_name_id[cus_name] = partner.id;
            if(partner.ref){
                this.partner_ref_id[partner.ref] = partner.id;
            }
        }

        this.partner_write_date = new_write_date || this.partner_write_date;

        if (updated_count) {
            // If there were updates, we need to completely 
            // rebuild the search string and the barcode indexing

            this.partner_search_string = "";

            for (var id in this.partner_by_id) {
                partner = this.partner_by_id[id];

                partner.address = (partner.street || '') +', '+ 
                                  (partner.zip || '')    +' '+
                                  (partner.city || '')   +', '+ 
                                  (partner.country_id[1] || '');
                this.partner_search_string += this._partner_search_string(partner);
            }
        }
        return updated_count;
    },
    get_partner_write_date: function(){
        return this.partner_write_date || "1970-01-01 00:00:00";
    },
    get_partner_by_id: function(id){
        return this.partner_by_id[id];
    },
    get_partner_by_code: function(ref){
        if(this.partner_by_ref[ref]){
            return this.partner_by_ref[ref];
        }
        return undefined;
    },
    get_unit_by_id: function(id){
        return this.unit_by_id[id];
    },
    add_order: function(order){
        var last_id = this.load('last_order_id',0);
        var orders  = this.load('orders',[]);
        orders.push({id: last_id + 1, data: order});
        this.save('last_order_id',last_id+1);
        this.save('orders',orders);
    },
    remove_order: function(order_id){
        var orders = this.load('orders',[]);
        orders = _.filter(orders, function(order){  //solo pasan al nuevo array aquellos que cumplan que el id no es el pasado.
            return order.id !== order_id;
        });
        this.save('orders',orders);
    },
    get_orders: function(){
        return this.load('orders',[]);
    },
});


return exports;
});
