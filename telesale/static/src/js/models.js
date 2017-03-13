odoo.define('telesale.models', function (require) {
"use strict";

var Backbone = window.Backbone;
var Model = require('web.DataModel');
var core = require('web.core');
var _t = core._t;

var exports = {};

exports.TsModel = Backbone.Model.extend({
    initialize: function(session, attributes) {
        Backbone.Model.prototype.initialize.call(this, attributes);
        var  self = this;
        this.session = session;  // openerp session
        this.ready = $.Deferred(); // used to notify the GUI that the PosModel has loaded all resources
        this.ts_widget = attributes.ts_widget;

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
    load_server_data: function(){
        var self=this;

        var loaded = self.fetch('res.users',['name','company_id'],[['id', '=', this.session.uid]])
            .then(function(users){
                self.set('user',users[0]);
                console.time('Test performance company');
                return self.fetch('res.company',
                [
                    'currency_id',
                    'email',
                    'website',
                    'company_registry',
                    'vat',
                    'name',
                    'phone',
                    'partner_id',
                    'min_limit',
                    'min_margin',
                ],
                [['id','=',users[0].company_id[0]]]);
                })
        return loaded;
    }
});

return exports; 

});


