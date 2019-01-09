/* Copyright 2018 Tecnativa - David Vidal
   License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define('pos.custom_anz.models', function (require) {
    'use strict';

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');

    var core = require('web.core');
    var _t = core._t;

    // Validate button prompts for reason
    screens.PaymentScreenWidget.include({

        validate_order: function(options) {
            var order = this.pos.get_order()
            if (order.return){
                let reason = prompt(_t("Return Reason"), '');
                order.return_reason = reason
            }
            this._super(options);
        },
    });

    // Export new field return reason
    var order_super = models.Order.prototype;
    models.Order = models.Order.extend({
        export_as_JSON: function () {
            var res = order_super.export_as_JSON.apply(this, arguments);
            if (this.return) {
                res.return_reason = this.return_reason;
            }
            return res;
        },
        to_upper_case: function(){
            var res = this.simplified_invoice.toLocaleUpperCase()
            return res;
        }
    });
    
});
