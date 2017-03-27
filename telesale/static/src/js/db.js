
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

        this.product_by_id = {};
        this.product_by_tmp_id = {};
        this.product_code_id = {};
        this.product_name_id = {};

        this.partner_by_id = {};
        this.partner_ref_id = {};
        this.partner_search_string = "";
        this.partner_name_id = {};
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
    _partner_search_string: function(partner){
        var str = partner.name;
        if (partner.ref){
            str += '|' + partner.ref;
        }
        str = '' + partner.id + ':' + str.replace(':','') + '\n';
        return str
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
    add_partners: function(partners){
        if(!partners instanceof Array){
            partners = [partners];
        }
        for(var i = 0, len = partners.length; i < len; i++){
            var partner = partners[i];

            this.partner_by_id[partner.id] = partner;
            // var cus_name = partner.comercial || partner.name
            var cus_name = partner.name + ' | ' + partner.ref
            // var cus_name = this.ts_model.getComplexName(partner)
            this.partner_name_id[cus_name] = partner.id;
            if(partner.ref){
                this.partner_ref_id[partner.ref] = partner.id;
            }
            var search_string = this._partner_search_string(partner);
            this.partner_search_string += search_string
        }
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
    get_product_by_tmp_id: function(id){
        return this.product_by_tmp_id[id];
    },
    get_product_by_code: function(code){
        if(this.product_by_code[code]){
            return this.product_by_code[code];
        }
        return undefined;
    },
    get_partner_by_id: function(id){
        return this.partner_by_id[id];
    },
    get_supplier_by_id: function(id){
        return this.suppliers_name_id[id];
    },
    get_partner_by_code: function(ref){
        if(this.partner_by_ref[ref]){
            return this.partner_by_ref[ref];
        }
        return undefined;
    },
    get_partner_contact: function(partner_id){
        res = undefined
        var partner_obj = this.get_partner_by_id(partner_id);
        if (partner_obj) {
        var res = partner_obj;
        for(var i = 0, len = partner_obj.child_ids.length; i < len; i++){
            var contact = this.get_partner_by_id(partner_obj.child_ids[i]);
            if (contact && contact.type == 'contact'){
                res = contact
                break;
            }
        }
        }
        return res;
    },
    get_unit_by_id: function(id){
        return this.unit_by_id[id];
    },
    get_qnote_by_id: function(id){
        return this.qnote_by_id[id];
    },
    get_route_by_id: function(id){
        return this.route_by_id[id];
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
    is_indirect_customer_by_name: function(partner){
        var res = false;
        if(partner){
          var partner_id = this.partner_name_id[partner];

          if (partner_id){
            var partner_obj = this.get_partner_by_id(partner_id)

            if (partner_obj){
              res = partner_obj.indirect_customer
            }
          }

        }

        return res
    },
});


return exports;
});
