odoo.define('telesale.models', function (require) {
"use strict";

var Backbone = window.Backbone;
var Model = require('web.DataModel');
var core = require('web.core');
var time = require('web.time');
var DB = require('telesale.db');
var _t = core._t;

var exports = {};


var my_round = function(number, decimals){
        var n = number || 0;
        if (typeof n === "string"){
            n = n * 1;
        }
        return n.toFixed(decimals) * 1
}

var TsModel = Backbone.Model.extend({
    initialize: function(session, attributes) {
    Backbone.Model.prototype.initialize.call(this, attributes);
        var  self = this;
        this.session = session;  // openerp session
        this.ready = $.Deferred(); // used to notify the GUI that the PosModel has loaded all resources
        this.ready2 = $.Deferred(); // used to notify the GUI that thepromotion has writed in the server
        // this.flush_mutex = new $.Mutex();  // used to make sure the orders are sent to the server once at time
        this.db = new DB.TS_LS();                       // a database used to store the products and categories
        // this.db.clear('products','partners');
        this.ts_widget = attributes.ts_widget;
        this.set({
            'currency':              {symbol: $, position: 'after'},
            'shop':                  null,
            'user':                  null,
            'company':               null,
            'orders':                new OrderCollection(),
            'products':              new ProductCollection(),
            'sold_lines':            new SoldLinesCollection(),
            'product_search_string': "",
            'products_names':        [], // Array of products names
            'products_codes':        [], // Array of products code

            'taxes':                  null,
            'ts_session':             null,
            'ts_config':              null,
            'units':                  [], // Array of units
            'units_names':            [], // Array of units names
           
            'customer_names':            [], // Array of customer names
            'customer_codes':         [], // Array of customer refs

            'pricelist':              null,
            'selectedOrder':          null,
            'nbr_pending_operations': 0,

            'update_catalog': 'a',  //value to detect changes between a and b to update the catalog only when click in label
            'bo_id': 0 //it's a counter to assign to the buttons when you do click on '+'
        });

        this.get('orders').bind('remove', function(){ self.on_removed_order(); });
        $.when(this.load_server_data())
            .done(function(){
                self.ready.resolve();

            }).fail(function(){
                self.ready.reject();
            });
    },
    // helper function to load data from the server
    fetch: function(model, fields, domain, ctx){
        this._load_progress = (this._load_progress || 0) + 0.05;
        this.ts_widget.loading_message(_t('Loading')+' '+model,this._load_progress);
        return new Model(model).query(fields).filter(domain).context(ctx).all()
    },
    fetch_limited_ordered: function(model, fields, domain, limit, orderby, ctx){
        return new Model(model).query(fields).filter(domain).limit(limit).order_by(orderby).context(ctx).first()
    },
    fetch_ordered: function(model, fields, domain, orderby, ctx){
        return new Model(model).query(fields).filter(domain).order_by(orderby).context(ctx).all()
    },
    // loads all the needed data on the sever. returns a deferred indicating when all the data has loaded.
    load_server_data: function(){
        var self=this;

        var loaded = self.fetch('res.users',['name','company_id'],[['id', '=', this.session.uid]])
            .then(function(users){
                self.set('user', users[0]);
                    // COMPANY
                return self.fetch('res.company',
                [
                    'currency_id',
                    'name',
                    'phone',
                    'partner_id',
                ],
                [['id','=',users[0].company_id[0]]]);
                }).then(function(companies){
                    self.set('company',companies[0]);

                    // UNITS
                    return self.fetch('product.uom', ['name'], []);
                }).then(function(units){
                    for (var key in units){
                        self.get('units_names').push(units[key].name)
                    }

                    self.db.add_units(units);
                    console.time('Test performance products');

                    // PRODUCTS
                    return self.fetch(
                        'product.product',
                        ['name', 'default_code', 'list_price', 'standard_price', 'uom_id', 'taxes_id', 'weight'],
                        [['sale_ok', '=', true]]
                    );
                }).then(function(products){
                    // TODO OPTIMIZAR
                    self.db.add_products(products);
                    var products_list = [];
                    var search_string = ""
                    for (var key in products){
                        var product_obj = self.db.get_product_by_id(products[key].id)
                         products_list.push(product_obj);
                         search_string += self.db._product_search_string(product_obj)
                         self.get('products_names').push(product_obj.name);
                         self.get('products_codes').push(product_obj.default_code);
                    }
                    self.set('product_search_string', search_string)
                    self.get('products').reset(products_list)

                    // PARTNERS
                    return self.fetch(
                        'res.partner',
                        ['name', 'comercial', 'ref', 'child_ids', 'phone', 'user_id',  'comment'],
                        [['customer','=',true]])
                }).then(function(customers){
                    for (var key in customers){
                        var customer_name = self.getComplexName(customers[key]);
                        self.get('customer_names').push(customer_name);
                        self.get('customer_codes').push(customers[key].ref);
                    }
                    self.db.add_partners(customers);

                    // TAXES
                    return self.fetch('account.tax', ['amount', 'price_include', 'amount_type'], [['type_tax_use','=','sale']]);
                }).then(function(taxes) {
                    self.set('taxes', taxes);
                    self.db.add_taxes(taxes);

                    // FISCAL POSITION TAX
                    return self.fetch('account.fiscal.position.tax', ['position_id', 'tax_src_id', 'tax_dest_id']);
                }).then(function(fposition_map) {
                    self.db.add_taxes_map(fposition_map);

                    // FISCAL POSITION
                    return self.fetch('account.fiscal.position', ['name', 'tax_ids']);
                }).then(function(fposition) {
                    self.db.add_fiscal_position(fposition);
                });
        return loaded;
    },
    getCurrentDateStr: function() {
        var date = new Date();
        var day = date.getDate();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        if (month < 10) month = "0" + month;
        if (day < 10) day = "0" + day;

        var today = year + "-" + month + "-" + day;
        return today;
    },

    add_new_order: function(){
        var order = new Order({ts_model:this});
        this.get('orders').add(order);
        this.set('selectedOrder', order);
    },
    on_removed_order: function(removed_order){
        if( this.get('orders').isEmpty()){
            this.add_new_order();
        }else{
            this.set({ selectedOrder: this.get('orders').last() });
        }
    },
    push_order: function(record) {
        this.db.add_order(record);
        this.flush();
    },
    cancel_order: function(erp_id){
        var self = this;
        // (new Model('sale.order')).call('cancel_order_from_ui',,undefined,{shadow:true})
        (new Model('sale.order')).call('cancel_order_from_ui', [[erp_id]])
            .fail(function(unused, event){
                //don't show error popup if it fails
                console.error('Failed to cancel order:',erp_id);
            })
            .done(function(){
                //remove from db if success
                self.get('selectedOrder').destroy(); // remove order from UI
            });
    },
    flush: function() {
        this._flush(0);
    },
    // attempts to send an order of index 'index' in the list of order to send. The index
    // is used to skip orders that failed.
    _flush: function(index) {
        var self = this;
        var orders = this.db.get_orders();
        self.set('nbr_pending_operations',orders.length);
        var order  = orders[index];
        if(!order){
            return;
        }
        self.ready2 = $.Deferred();
        //try to push an order to the server
        // shadow : true is to prevent a spinner to appear in case of timeout
        (new Model('sale.order')).call('create_order_from_ui',[[order]])
            .fail(function(unused, event){
                //don't show error popup if it fails
                console.error('Failed to send order:',order);
                self._flush(index+1);
                self.ready2.reject()
            })
            .done(function(){
                //remove from db if success
                self.db.remove_order(order.id);
                self._flush(index);
                self.get('selectedOrder').destroy(); // remove order from UI
                self.ready2.resolve()
            });
    },
     _flush2: function(record) {
        var self = this;
        var last_id = self.db.load('last_order_id',0);
        var order = {id: last_id + 1, data: record};
        console.log(order)
        self.set('nbr_pending_operations',orders.length);
        if(!order){
            return;
        }
        self.ready2 = $.Deferred();
        //try to push an order to the server
        // shadow : true is to prevent a spinner to appear in case of timeout
        (new Model('sale.order')).call('create_order_from_ui',[[order]],{})
            .fail(function(unused, event){
                alert('Ocurrió un fallo en al mandar el pedido al servidor');
                self.ready2.reject()
            })
            .done(function(){
                //remove from db if success
                self.get('selectedOrder').destroy(); // remove order from UI
                self.ready2.resolve()
            });
    },
    // Build a order loaded from the server as order_obj the selected order_model
    build_order: function(order_obj, order_model, order_lines){
        var partner_obj = this.db.get_partner_by_id(order_obj.partner_id[0]);
        var cus_name = this.getComplexName(partner_obj);
        order_model.set('partner', cus_name);
        order_model.set('partner_code', partner_obj.ref || "");
        // order_model.set('customer_debt', my_round(partner_obj.credit,2));
        // order_model.set('limit_credit', my_round(partner_obj.credit_limit,2));
        order_model.set('erp_id', order_obj.id);
        order_model.set('erp_state', order_obj.state);
        var state = order_obj.state
        order_model.set('state', state);
      
        if (order_obj.date_planned){
            var only_date = order_obj.date_planned.split(' ');
            if(only_date.length > 1){
              order_model.set('date_planned', only_date[0]);
            }else {
              order_model.set('date_planned', order_obj.date_planned);
            }
        }
        order_model.set('num_order',order_obj.name);
        // TODO SACARLO DEL CLIENTE
        order_model.set('customer_comment',order_obj.customer_comment || '');
        order_model.set('comercial',partner_obj.user_id[1]);
        order_model.set('coment',order_obj.note || '');

    
        var contact = this.db.get_partner_contact(order_obj.partner_id[0])
        order_model.set('contact_name',contact.name);

        for (var key in order_lines){
            var line = order_lines[key];
            var prod_obj = this.db.get_product_by_id(line.product_id[0]);
            //TODO: Calculo de los impuestos en la linea para tener en cuenta tarifa a domicilio
            var line_vals = {ts_model: this, order:order_model,
                             code:prod_obj.default_code || "" ,
                             product:prod_obj.name,
                             unit:line.product_uom[1],
                             qty:line.product_uom_qty,
                             pvp:my_round(line.price_unit,2), //TODO poner precio del producto???
                             total: my_round(line.product_uom_qty * line.price_unit * (1 - line.discount /100)),
                             discount: my_round(line.discount, 2) || 0.0,
                             taxes_ids: line.tax_id || prod_obj.taxes_id || [],
                            }
            var line = new Orderline(line_vals);
            order_model.get('orderLines').add(line);
        }
    },
    parse_duration_watch_format: function(minutes){
        var res = "00:00";
        if (minutes){
            var int_part = Math.floor(minutes); // integer part of minutes
            var decimal_part = minutes - int_part;
            var seconds = Math.round(decimal_part * 60);
            if (int_part < 10) int_part = "0" + int_part;
            if (seconds < 10) seconds = "0" + seconds;
            res = int_part + ":" + seconds
        }
        return res;
    },
    get_calls_by_date_state: function(date, state, route){
        var self=this;
        if (!state){state = $('#state-select').val()}
        if (!date){date = $('#date-call-search').val()}
        if (!route){route = $('#route_search').val()}
        if(date == ""){
          var domain = [['partner_id', '!=', false]]
        }else{
          var domain = [['date', '>=', date + " 00:00:00"],['date', '<=', date + " 23:59:59"], ['partner_id', '!=', false]]
        }
        if (state){
            if (state != "any")
                domain.push(['state','=',state])
        }
        if (route != "0"){
          domain.push(['route_id', '=', parseInt(route)])
        }
        self.fetch('crm.phonecall',['date','partner_id','name','partner_phone','customer_phone', 'state','duration','route_id'],domain)
        .then(function(calls){
            if (!$.isEmptyObject(calls)){
                for (var key in calls){
                    calls[key].date = self.parse_utc_to_str_date(calls[key].date); //set dates in browser timezone
                    calls[key].duration = self.parse_duration_watch_format(calls[key].duration); //set dates in browser timezone
                    var contact = self.db.get_partner_contact(calls[key].partner_id[0])
                    if (contact){
                        calls[key].partner_phone = contact.phone|| "-" //set phone of contact
                        calls[key].contact_name = contact.name //add contact name to phone
                    }
                }
            }
            self.get('calls').reset(calls);
        });

    },
    getCurrentFullDateStr: function() {
        var date = new Date();
        var day = date.getDate();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        var hours = date.getHours();
        var minutes = date.getMinutes();
        var seconds = date.getSeconds();
        if (month < 10) month = "0" + month;
        if (day < 10) day = "0" + day;
        if (hours < 10) hours = "0" + hours;
        if (minutes < 10) minutes = "0" + minutes;
        if (seconds < 10) seconds = "0" + seconds;

        var today = year + "-" + month + "-" + day + " " + hours + ":" + minutes + ":" + seconds;
        return today;
    },
    getUTCDateStr: function() {
        var date = new Date();
        var day = date.getDate();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        var hours = date.getUTCHours();
        var minutes = date.getMinutes();
        var seconds = date.getSeconds();
        if (month < 10) month = "0" + month;
        if (day < 10) day = "0" + day;
        if (hours < 10) hours = "0" + hours;
        if (minutes < 10) minutes = "0" + minutes;
        if (seconds < 10) seconds = "0" + seconds;

        var today = year + "-" + month + "-" + day + " " + hours + ":" + minutes + ":" + seconds;
        return today;
    },
    datetimeToStr: function(date) {
        var day = date.getDate();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        var hours = date.getHours();
        var minutes = date.getMinutes();
        var seconds = date.getSeconds();
        if (month < 10) month = "0" + month;
        if (day < 10) day = "0" + day;
        if (hours < 10) hours = "0" + hours;
        if (minutes < 10) minutes = "0" + minutes;
        if (seconds < 10) seconds = "0" + seconds;

        var today = year + "-" + month + "-" + day + " " + hours + ":" + minutes + ":" + seconds;
        return today;
    },
    getCurrentDateStr: function() {
        var date = new Date();
        var day = date.getDate();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        if (month < 10) month = "0" + month;
        if (day < 10) day = "0" + day;

        var today = year + "-" + month + "-" + day;
        return today;
    },
    getCurrentDatePlannedStr: function() {
        var date = new Date();
        day = date.getDay()
        add_days = 1
        if (day === 5) add_days = 3
        if (day === 6) add_days = 2
        date.setDate(date.getDate() + add_days)
        var day = date.getDate();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        if (month < 10) month = "0" + month;
        if (day < 10) day = "0" + day;

        var today = year + "-" + month + "-" + day;
        return today;
    },
    parse_str_date_to_utc: function(str_date){

        // Todo esto porque lo de abajo cambia el mes por el día, le cambiamos la fecha antes para obtener el resultado correcto
        // var str_date2 = instance.web.datetime_to_str(Date.parse(str_date)); //Se comenta porque intercambia day por month, puede que dependa de si estás en firefox o en chrome
        var str_date2 = str_date;
        var str_year = str_date2.split(" ")[0].split("-")[0]
        var str_month = str_date2.split(" ")[0].split("-")[1]
        var str_day = str_date2.split(" ")[0].split("-")[2]
        var new_str = str_year + "-" + str_month + "-" + str_day + " " + str_date2.split(" ")[1]
        return new_str
    },
    parse_utc_to_str_date: function(str_date){
        return this.datetimeToStr(time.str_to_datetime(str_date));
    },
    dateToStr: function(date) {
        var day = date.getDate();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        if (month < 10) month = "0" + month;
        if (day < 10) day = "0" + day;

        var today = year + "-" + month + "-" + day;
        return today;
    },
    localFormatDate: function(date){
        var splited =  date.split("-");
        return splited[2] + "-" +  splited[1] + "-" + splited[0];
    },
    localFormatDateTime: function(date_time){
        if (date_time){
          var splited =  date_time.split(" ");
          var date_part =  splited[0].split('-');
          var hour_part =  splited[1];
          return date_part[2] + "-" +  date_part[1] + "-" + date_part[0] + " " + hour_part;
      }
    },
    getComplexName: function(partner_obj){
        var res = '';
        if (partner_obj){
          res =  partner_obj.name + ' | ' + partner_obj.ref
        }
        return res;
    },
    my_round: function(number, decimals){
        var n = number || 0;
        if (typeof n === "string"){
            n = n * 1;
        }
        return n.toFixed(decimals) * 1
    },

});

// ****************************************************************************************************************
// ******************************************** PRODUCT MODEL **************************************************
// ****************************************************************************************************************
var Product = Backbone.Model.extend({
});

var ProductCollection = Backbone.Collection.extend({
    model: Product,
});

// ****************************************************************************************************************
// ******************************************** ORDER LINE MODEL **************************************************
// ****************************************************************************************************************
var Orderline = Backbone.Model.extend({
    defaults: {
        n_line: '',
        code: '',
        product: '',
        qty: 1,
        unit: '',
        pvp: 0,
        total: 0,
        //to calc totals
        margin: 0,
        taxes_ids: [],

    },
    initialize: function(options){
        this.ts_model = options.ts_model;
        this.order = options.order;
        this.selected = false;
    },
    set_selected: function(selected){
        this.selected = selected;
    },
    is_selected: function(){
        return this.selected;
    },
    check: function(){
        var res = true
        if ( this.get('product') == "" ) {
           res = false;
        }
        return res
    },
    get_product: function(){
        var product_obj = false
        if (this.check()){
            var product_name = this.get('product');
            var product_id = this.ts_model.db.product_name_id[product_name];
            var product_obj = this.ts_model.db.product_by_id[product_id]
        }
        return product_obj;
    },
    export_as_JSON: function() {
        var product_id = this.ts_model.db.product_name_id[this.get('product')];
        var uom_id = this.ts_model.db.unit_name_id[this.get('unit')];
        return {
            product_id:  product_id,
            qty: this.get('qty'),
            product_uom: uom_id,
            price_unit: this.get('pvp'),
            tax_ids: this.get('taxes_ids'),
            discount: this.get('discount') || 0.0,
        };
    },
    get_price_without_tax: function(){
        return this.get_all_prices().priceWithoutTax;
    },
    get_price_with_tax: function(){
        return this.get_all_prices().priceWithTax;
    },
    get_tax: function(){
        return this.get_all_prices().tax;
    },
    get_all_prices: function(){
        var self = this;
        var base = this.get('qty') * this.get('pvp') * (1 - (this.get('discount') / 100.0));
        var totalTax = base;
        var totalNoTax = base;
        var taxtotal = 0;
        var product =  this.get_product();

        if (product){
            var taxes_ids = self.get('taxes_ids')
            var taxes =  self.ts_model.get('taxes');
            var tmp;
            _.each(taxes_ids, function(el) {
                var tax = _.detect(taxes, function(t) {return t.id === el;});
                if (tax.price_include) {
                    if (tax.amount_type === "percent") {
                        tmp =  base - base / (1 + (tax.amount / 100.0));
                    } else if (tax.amount_type === "fixed") {
                        tmp = (tax.amount / 100.0) * self.get('qty');
                    } else {
                        throw "This type of tax is not supported by the telesale system: " + tax.amount_type;
                    }
                    // tmp = round_dc(tmp,2);
                    taxtotal += tmp;
                    totalNoTax -= tmp;
                } else {
                    if (tax.amount_type === "percent") {
                        tmp = (tax.amount / 100.0) * base;
                    } else if (tax.amount_type === "fixed") {
                        tmp = (tax.amount / 100.0) * self.get('qty');
                    } else {
                        throw "This type of tax is not supported by the telesale system: " + tax.amount_type;
                    }
                    // tmp = round_dc(tmp,2);
                    taxtotal += tmp;
                    totalTax += tmp;
                }
            });
        }
        return {
            "priceWithTax": my_round(totalTax,2),
            "priceWithoutTax": my_round(totalNoTax,2),
            "tax": my_round(taxtotal,2),
        };
    },
});
var OrderlineCollection = Backbone.Collection.extend({
    model: Orderline,
});


// ****************************************************************************************************************
// ******************************************** ORDER MODEL **************************************************
// ****************************************************************************************************************
var counter = 0;
var Order = Backbone.Model.extend({
    initialize: function(attributes){
        Backbone.Model.prototype.initialize.apply(this, arguments);
        this.set({
            creationDate:   new Date(),
            orderLines:     new OrderlineCollection(),
            name:           this.generateUniqueId(),
            //order #toppart values
            num_order: this.generateNumOrder(),
            partner_code: '',
            partner: '',
            customer_comment: '',
            contact_name: '',
            date_order: this.getStrDate(),
            date_planned: this.getStrDatePlanned(),
            limit_credit: (0),
            customer_debt: (0),
            //order #bottompart values
            total_discount: (0),
            total_discount_per: (0).toFixed(2)+" %",
            total_margin_per: (0).toFixed(2)+" %",
            total: (0),
            total_base: (0),
            total_iva: (0),
            total_margin: (0),
            selected_line: null,
            //to pas the button action to the server
            action_button: null,
            //to check save confirm cancel butons
            erp_id: false,
            erp_state: false,
            state:"draft",
            comercial: '',
            coment: '',
        });
        this.ts_model = attributes.ts_model;
        this.selected_orderline = undefined;
        this.screen_data = {};  // see ScreenSelector
        return this;
    },
    generateNumOrder: function(){
        counter += 1;
        return "TStmp "+counter
    },
    getStrDate: function() {
        var date = new Date();
        var day = date.getDate();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        if (month < 10) month = "0" + month;
        if (day < 10) day = "0" + day;

        var today = year + "-" + month + "-" + day;
        return today;
    },
     getStrDatePlanned: function() {
        var date = new Date();
        var day = date.getDate();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        if (month < 10) month = "0" + month;
        if (day < 10) day = "0" + day;

        var today = year + "-" + month + "-" + day;
        return today;
    },
    dateToStr: function(date) {
        var day = date.getDate();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        if (month < 10) month = "0" + month;
        if (day < 10) day = "0" + day;

        var today = year + "-" + month + "-" + day;
        return today;
    },
    generateUniqueId: function() {
        return new Date().getTime();
    },
    addLine: function() {
        var line = new Orderline({ts_model: this.ts_model, order:this})
        this.get('orderLines').add(line);
        return line
    },
    getSelectedLine: function(){
        var order_lines = this.get('orderLines').models;
        var res = false
        for (var key in order_lines){
            var line = order_lines[key];
            if (line.is_selected())
                res = line;
        }
        return res
    },
    removeLine: function(){
        var index = 0;
        (this.get('orderLines')).each(_.bind( function(item) {
            if ( item.is_selected() ){
                this.get('orderLines').remove(item)
                index = item.get('n_line') - 1;
            }
        }, this));
        if ( !$.isEmptyObject( this.get('orderLines')) ){
             if (index > 0)
                index = index - 1;
            var new_line = this.get('orderLines').models[index]
            this.selectLine(new_line);
        }

    },
    selectLine: function(line){
        if(line){
            if (line !== this.selected_orderline){
                if(this.selected_orderline) {
                    this.selected_orderline.set_selected(false);
                }
                this.selected_orderline = line;
                this.set('selected_line',   this.selected_orderline );
                this.selected_orderline.set_selected(true);
            }
        }
        else{
          this.selected_orderline = undefined;
        }
    },
    getLastOrderline: function(){
        return this.get('orderLines').at(this.get('orderLines').length -1);
    },
    check: function(){
        var res = true
        if ( this.get("partner") == "" ){
            alert(_t("Partner can not be empty."));
            res = false
        }
        if ( this.get("orderLines").length == 0 ){
            alert(_t("Order lines can not be empty."));
            res = false;
        } else{
            (this.get('orderLines')).each(_.bind( function(item) {
                if ( !item.check() ){
                    alert(_t("Product can not be empty"));
                    res = false;
                }
            }, this));
        }
        return res
    },
    exportAsJSON: function() {
        var orderLines;
        orderLines = [];
        (this.get('orderLines')).each(_.bind( function(item) {
            return orderLines.push(item.export_as_JSON());
        }, this));
        return {
            lines: orderLines,
            name: this.get('num_order'),
            partner_id: this.ts_model.db.partner_name_id[this.get('partner')],
            action_button: this.get('action_button'),
            erp_id: this.get('erp_id'),
            erp_state: this.get('erp_state'),
            date_order: this.get('date_order'),
            date_planned: this.get('date_planned'),
            note: this.get('coment'),
            customer_comment: this.get('customer_comment'),
        };
    },
    get_last_line_by: function(period, client_id){
      var self = this;
      // TODO TODA ESTA PARTE
      var model = new Model('sale.order.line');
      var cache_sold_lines = self.ts_model.db.cache_sold_lines[client_id]
      if (cache_sold_lines && period == 'year'){
          self.ts_model.get('sold_lines').reset(cache_sold_lines)
      }
      else{
          var loaded = model.call("get_last_lines_by",[period, client_id])
              .then(function(order_lines){
                      if (!order_lines){
                        order_lines = []
                      }
                        // self.add_lines_to_current_order(order_lines);
                      if(period == 'year'){
                          self.ts_model.db.cache_sold_lines[client_id] = order_lines;
                      }
                      self.ts_model.get('sold_lines').reset(order_lines)
              });
            return loaded
      }
    },
    add_lines_to_current_order: function(order_lines, fromsoldprodhistory){
        this.get('orderLines').unbind();  //unbind to render all the lines once, then in OrderWideget we bind again
        if(this.selected_orderline && this.selected_orderline.get('code') == "" && this.selected_orderline.get('product') == "" ){
          $('.remove-line-button').click()
        }
        for (var key in order_lines){
            var line = order_lines[key];
            var prod_obj = this.ts_model.db.get_product_by_id(line.product_id[0]);
            if  (!prod_obj){
              alert(_t('This product can not be loaded, becouse is not registerd'))
              return
            }
            var current_olines = this.get('orderLines').models
            for (var key2 in current_olines){
                var o_line = current_olines[key2];
                var line_product_id =  this.ts_model.db.product_name_id[o_line.get('product')];
            }
            var l_qty = line.product_uom_qty
            if(fromsoldprodhistory){
              l_qty = 1.0;
            }
            var line_vals = {ts_model: this.ts_model, order:this,
                             code:prod_obj.default_code || "" ,
                             product:prod_obj.name,
                             unit:prod_obj.uom_id[1] || line.product_uom[1], 
                             qty:my_round(l_qty),
                             pvp: my_round(line.current_pvp ? line.current_pvp : 0, 2),
                             total: my_round(line.product_uom_qty * line.price_unit * (1 - line.discount /100)),
                             discount: my_round( line.discount || 0.0, 2 ),
                             taxes_ids: line.tax_id || product_obj.taxes_id || [],
                            }
            var line = new Orderline(line_vals);
            this.get('orderLines').add(line);
        }
        $('.col-code').focus(); //si no, al añadir línea desde resumen de pedidos, no existe foco y si añade más líneas da error
    },
    deleteProductLine: function(id_line){
      var self=this;
      // self.get('orderLines')
    },
    addProductLine: function(product_id){
        var self=this;
        // var customer_id = this.ts_model.db.partner_name_id[this.get('partner')];
        if($('#partner').val()){
            if(this.selected_orderline && this.selected_orderline.get('code') == "" && this.selected_orderline.get('product') == "" ){
              $('.remove-line-button').click()
            }
            $('.add-line-button').click()
            var added_line = self.ts_model.get('selectedOrder').getLastOrderline();
            var lines_widgets = self.ts_model.ts_widget.new_order_screen.order_widget.orderlinewidgets
            lines_widgets[lines_widgets.length - 1].call_product_id_change(product_id)
        }
        else{
            alert(_t('Please select a customer before adding a order line'));
        }
    },

});

var OrderCollection = Backbone.Collection.extend({
    model: Order,
});

 //**************************** SOLD LINES AND SOLD LINESCOLLECTION***********************************************
var SoldLines = Backbone.Model.extend({
    });

var SoldLinesCollection = Backbone.Collection.extend({
        model: SoldLines,
    });
exports = {
    Order: Order,
    TsModel: TsModel
}; 
return exports;
});


