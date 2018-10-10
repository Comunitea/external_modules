odoo.define('telesale.CustomerList', function (require) {
"use strict";

var TsBaseWidget = require('telesale.TsBaseWidget');
var models = require('telesale.models');
var core = require('web.core');
// var Model = require('web.DataModel');
var rpc = require('web.rpc');

var _t = core._t;
var QWeb = core.qweb;


/*--------------------------------------*\
 |          THE DOM CACHE               |
\*======================================*/

// The Dom Cache is used by various screens to improve
// their performances when displaying many time the 
// same piece of DOM.
//
// It is a simple map from string 'keys' to DOM Nodes.
//
// The cache empties itself based on usage frequency 
// stats, so you may not always get back what
// you put in.

var DomCache = core.Class.extend({
    init: function(options){
        options = options || {};
        this.max_size = options.max_size || 2000;

        this.cache = {};
        this.access_time = {};
        this.size = 0;
    },
    cache_node: function(key,node){
        var cached = this.cache[key];
        this.cache[key] = node;
        this.access_time[key] = new Date().getTime();
        if(!cached){
            this.size++;
            while(this.size >= this.max_size){
                var oldest_key = null;
                var oldest_time = new Date().getTime();
                for(key in this.cache){
                    var time = this.access_time[key];
                    if(time <= oldest_time){
                        oldest_time = time;
                        oldest_key  = key;
                    }
                }
                if(oldest_key){
                    delete this.cache[oldest_key];
                    delete this.access_time[oldest_key];
                }
                this.size--;
            }
        }
        return node;
    },
    clear_node: function(key) {
        var cached = this.cache[key];
        if (cached) {
            delete this.cache[key];
            delete this.access_time[key];
            this.size --;
        }
    },
    get_node: function(key){
        var cached = this.cache[key];
        if(cached){
            this.access_time[key] = new Date().getTime();
        }
        return cached;
    },
});

var CustomerListWidget = TsBaseWidget.extend({
    template:'CustomerListWidget',
    init: function(parent, options){
        this._super(parent, options);
        this.partner_cache = new DomCache();
    },
    renderElement: function(){
        this._super();
        var self=this;

        this.details_visible = false;
        this.old_client = this.ts_model.get_order().get_client();

        // SHOW CREATE NEW CUSTOMER
        this.$('.new-customer').click(function(){
            self.display_customer_details('edit',{
                'country_id': self.ts_model.get('company').country_id,
            });
        });

        // Set customer
        this.$('.next').click(function(){   
            self.save_changes();
            // self.gui.back();    // FIXME HUH ?
        });
        // Set shipp addr
        this.$('.next2').click(function(){   
            self.set_partner_shipp();
            // self.gui.back();    // FIXME HUH ?
        });

        // Get partners
        var partners = this.ts_model.db.get_partners_stored(1000);
        this.render_list(partners);
        this.reload_partners();


        if( this.old_client ){
            this.display_customer_details('show',this.old_client,0);
        }

        this.$('.client-list-contents').delegate('.client-line','click',function(event){
            self.line_select(event,$(this),parseInt($(this).data('id')));
        });

        // Search customers implementation
        var search_timeout = null;
        this.$('.searchbox input').on('keyup',function(event){
            clearTimeout(search_timeout);

            var query = this.value;

            search_timeout = setTimeout(function(){
                self.perform_search(query,event.which === 13);
            },70);
        });

        // Clear search
        this.$('.searchbox .search-clear').click(function(){
            self.clear_search();
        });
    },
    save_changes: function(){
        var self = this;
        if (this.new_client.company_type != 'company'){
            alert(_t("You can set it as order's customer, because is not a company type"));
            return;
        }
        var order = this.ts_model.get_order();
        if( this.has_client_changed() ){
            var cus_name = self.ts_model.getComplexName(this.new_client);
            $('#partner').val(cus_name);
            $('button#button_no').click();
        }
    },
    set_partner_shipp: function(){
        var self = this;
        var order = this.ts_model.get_order();
        if( this.has_client_changed() ){
            var cus_name = self.ts_model.getComplexName(this.new_client);
            $('#shipp_addr').val(cus_name);
            $('button#button_no').click();
            $('#shipp_addr').focus();
        }
    },
    line_select: function(event,$line,id){
        var partner = this.ts_model.db.get_partner_by_id(id);
        this.$('.client-list .lowlight').removeClass('lowlight');
        if ( $line.hasClass('highlight') ){
            $line.removeClass('highlight');
            $line.addClass('lowlight');
            this.display_customer_details('hide',partner);
            this.new_client = null;
            this.toggle_save_button();
        }else{
            this.$('.client-list .highlight').removeClass('highlight');
            $line.addClass('highlight');
            var y = event.pageY - $line.parent().offset().top;
            this.display_customer_details('show',partner,y);
            this.new_client = partner;
            this.toggle_save_button();
        }
    },
    // ui handle for the 'cancel customer edit changes' action
    undo_client_details: function(partner) {
        if (!partner.id) {
            this.display_customer_details('hide');
        } else {
            this.display_customer_details('show',partner);
        }
    },
    perform_search: function(query, associate_result){
        var customers;
        if(query){
            customers = this.ts_model.db.search_partner(query);
            this.display_customer_details('hide');
            if ( associate_result && customers.length === 1){
                this.new_client = customers[0];
                // this.save_changes();
                // this.gui.back();
            }
            this.render_list(customers);
        }else{
            customers = this.ts_model.db.get_partners_stored();
            this.render_list(customers);
        }
    },
    clear_search: function(){
        var customers = this.ts_model.db.get_partners_stored(1000);
        this.render_list(customers);
        this.$('.searchbox input')[0].value = '';
        this.$('.searchbox input').focus();
    },
    render_list: function(partners){
        var contents = this.$el[0].querySelector('.client-list-contents');
        contents.innerHTML = "";
        for(var i = 0, len = Math.min(partners.length,1000); i < len; i++){
            var partner    = partners[i];
            var clientline = this.partner_cache.get_node(partner.id);
            if(!clientline){
                var clientline_html = QWeb.render('CustomerLine',{widget: this, partner:partners[i]});
                var clientline = document.createElement('tbody');
                clientline.innerHTML = clientline_html;
                clientline = clientline.childNodes[1];
                this.partner_cache.cache_node(partner.id,clientline);
            }
            if( partner === this.old_client ){
                clientline.classList.add('highlight');
            }else{
                clientline.classList.remove('highlight');
            }
            contents.appendChild(clientline);
        }
    },
    // This fetches partner changes on the server, and in case of changes, 
    // rerenders the affected views
    reload_partners: function(){
        var self = this;
        return this.ts_model.load_new_partners()
        .then(function(){
            self.render_list(self.ts_model.db.get_partners_stored(1000));
            // update the currently assigned client if it has been changed in db.
            // TODO ADAPTAR
            // var curr_client = self.pos.get_order().get_client();
            // if (curr_client) {
            //     self.pos.get_order().set_client(self.pos.db.get_partner_by_id(curr_client.id));
            // }
        });
    },
    display_customer_details: function(visibility,partner,clickpos){
        var self = this;
        var contents = this.$('.client-details-contents');
        var parent   = this.$('.client-list').parent();
        var scroll   = parent.scrollTop();
        var height   = contents.height();

        contents.off('click','.button.edit'); 
        contents.off('click','.button.save'); 
        contents.off('click','.button.undo'); 
        contents.on('click','.button.edit',function(){ self.edit_client_details(partner); });
        contents.on('click','.button.save',function(){ self.save_client_details(partner); });
        contents.on('click','.button.undo',function(){ self.undo_client_details(partner); });
        this.editing_client = false;
        this.uploaded_picture = null;
        if(visibility === 'show'){
            contents.empty();
            contents.append($(QWeb.render('CustomerDetails',{widget:this, partner:partner})));

            var new_height   = contents.height();

            if(!this.details_visible){
                // resize client list to take into account client details
                parent.height('-=' + new_height);

                if(clickpos < scroll + new_height + 20 ){
                    parent.scrollTop( clickpos - 20 );
                }else{
                    parent.scrollTop(parent.scrollTop() + new_height);
                }
            }else{
                parent.scrollTop(parent.scrollTop() - height + new_height);
            }

            this.details_visible = true;
            this.toggle_save_button();
        } else if (visibility === 'edit') {
            this.editing_client = true;
            contents.empty();
            contents.append($(QWeb.render('CustomerDetailsEdit',{widget:this,partner:partner})));
            // Autocomplete states from array of names
            var state_names = self.ts_model.get('state_names');
            contents.find('#state').autocomplete({
                source: function(request, response) {
                    var results = $.ui.autocomplete.filter(state_names, request.term);
                    response(results.slice(0, 20));
                }
            });
            contents.find('#state').keydown(function(e){
                if( e.keyCode != $.ui.keyCode.ENTER ) return; 

                e.keyCode = $.ui.keyCode.DOWN;
                $(this).trigger(e);

                self.$('#country').focus()
        
                return false;
            });
            // Pricelist autocomplete
            var pricelist_names = self.ts_model.get('pricelist_names');
            contents.find('#pricelist').autocomplete({
                source: function(request, response) {
                    var results = $.ui.autocomplete.filter(pricelist_names, request.term);
                    response(results.slice(0, 20));
                }
            });
            contents.find('#pricelist').keydown(function(e){
                if( e.keyCode != $.ui.keyCode.ENTER ) return; 

                e.keyCode = $.ui.keyCode.DOWN;
                $(this).trigger(e);

                self.$('#country').focus()
        
                return false;
            });
            // Countries autocomplete
            var country_names = self.ts_model.get('country_names');
            contents.find('#country').autocomplete({
                source: function(request, response) {
                    var results = $.ui.autocomplete.filter(country_names, request.term);
                    response(results.slice(0, 20));
                }
            });
            contents.find('#country').keydown(function(e){
                if( e.keyCode != $.ui.keyCode.ENTER ) return; 

                e.keyCode = $.ui.keyCode.DOWN;
                $(this).trigger(e);

                self.$('#phone').focus()
        
                return false;
            });
            var partner_names = self.ts_model.get('customer_names');
            contents.find('#parent').autocomplete({
                source: function(request, response) {
                    var results = $.ui.autocomplete.filter(partner_names, request.term);
                    response(results.slice(0, 20));
                }
            });
            contents.find('#parent').keydown(function(e){
                if( e.keyCode != $.ui.keyCode.ENTER ) return; 

                e.keyCode = $.ui.keyCode.DOWN;
                $(this).trigger(e);

                e.keyCode = $.ui.keyCode.TAB;
                $(this).trigger(e);
        
                return false;
            });
            this.toggle_save_button();

            // Browsers attempt to scroll invisible input elements
            // into view (eg. when hidden behind keyboard). They don't
            // seem to take into account that some elements are not
            // scrollable.
            contents.find('input').blur(function() {
                setTimeout(function() {
                    self.$('.window').scrollTop(0);
                }, 0);
            });

            contents.find('.image-uploader').on('change',function(event){
                self.load_image_file(event.target.files[0],function(res){
                    if (res) {
                        contents.find('.client-picture img, .client-picture .fa').remove();
                        contents.find('.client-picture').append("<img src='"+res+"'>");
                        contents.find('.detail.picture').remove();
                        self.uploaded_picture = res;
                    }
                });
            });
        } else if (visibility === 'hide') {
            contents.empty();
            parent.height('100%');
            if( height > scroll ){
                contents.css({height:height+'px'});
                contents.animate({height:0},400,function(){
                    contents.css({height:''});
                });
            }else{
                parent.scrollTop( parent.scrollTop() - height);
            }
            this.details_visible = false;
            this.toggle_save_button();
        }
    },
    toggle_save_button: function(){
        var $button = this.$('.button.next');
        if (this.editing_client) {
            $button.addClass('oe_hidden');
            return;
        } else if( this.new_client ){
            if( !this.old_client){
                $button.text(_t('Set Customer'));
            }else{
                $button.text(_t('Change Customer'));
            }
        }else{
            $button.text(_t('Deselect Customer'));
        }
        $button.toggleClass('oe_hidden',!this.has_client_changed());
    },
    has_client_changed: function(){
        if( this.old_client && this.new_client ){
            return this.old_client.id !== this.new_client.id;
        }else{
            return !!this.old_client !== !!this.new_client;
        }
    },
    // what happens when we save the changes on the client edit form -> we fetch the fields, sanitize them,
    // send them to the backend for update, and call saved_client_details() when the server tells us the
    // save was successfull.
    save_client_details: function(partner) {
        var self = this;
        
        var fields = {};
        this.$('.client-details-contents .detail').each(function(idx,el){
            fields[el.name] = el.value || false;
        });
        var company_type = this.$('.company_type').val();
        var is_company = company_type == 'company' ? true : false
        fields['is_company'] = is_company
        if (!is_company){
            fields['type'] = 'delivery'
        }

        fields['property_product_pricelist'] = false
        fields['state_id'] = false
        fields['country_id'] = false
        var pricelist_id = self.ts_model.db.pricelist_name_id[this.$('#pricelist').val()];
        if (pricelist_id){
            fields['property_product_pricelist'] = pricelist_id
        }
        var state_id = self.ts_model.db.state_name_id[this.$('#state').val()];
        if (state_id){
            fields['state_id'] = state_id
        }
        var country_id = self.ts_model.db.country_name_id[this.$('#country').val()];
        if (country_id){
            fields['country_id'] = country_id
        }
        var parent_id = self.ts_model.db.partner_name_id[this.$('#parent').val()];
        if (parent_id){
            fields['parent_id'] = parent_id;
        }

        if (!fields.name) {
            alert(_t('A Customer Name Is Required'));
            return;
        }
        if (!fields.city) {
            alert(_t('City Is Required'));
            return;
        }
        if (!fields.state_id) {
            if (country_id == 69){
                alert(_t('State Is Required'));
                return;
            }
        }
        
        fields.id           = partner.id || false;
        // fields.country_id   = fields.country_id || false;

        rpc.query({model: 'res.partner', method: 'update_partner_from_ui', args:[fields]}).then(function(partner_id){
            self.saved_client_details(partner_id);
        },function(err,event){
            event.preventDefault();
            alert(_t('Error saving partner to the server'))
        });


    },
    
    // what happens when we've just pushed modifications for a partner of id partner_id
    saved_client_details: function(partner_id){
        var self = this;
        this.reload_partners().then(function(){
            var partner = self.ts_model.db.get_partner_by_id(partner_id);
            if (partner) {
                self.new_client = partner;
                self.toggle_save_button();
                self.display_customer_details('show',partner);
                var customer_name = self.ts_model.getComplexName(partner);
                self.ts_model.get('customer_names').push(customer_name);
                self.ts_model.get('customer_codes').push(partner.ref);
            }
            else {
                // should never happen, because create_from_ui must return the id of the partner it
                // has created, and reload_partner() must have loaded the newly created partner. 
                self.display_customer_details('hide');
            }
        });
    },
    // ui handle for the 'edit selected customer' action
    edit_client_details: function(partner) {
        this.display_customer_details('edit',partner);
    },
});

return{
    CustomerListWidget: CustomerListWidget
};

});
