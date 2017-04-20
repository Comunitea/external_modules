odoo.define('telesale.CustomerList', function (require) {
"use strict";

var TsBaseWidget = require('telesale.TsBaseWidget');
var models = require('telesale.models');
var core = require('web.core');
var _t = core._t;

var CustomerListWidget = TsBaseWidget.extend({
    template:'CustomerListWidget',
});

return{
    CustomerListWidget: CustomerListWidget
};

});
