
odoo.define('telesale.main', function (require) {
"use strict";
var ts_widget = require('telesale.BaseWidget');
var core = require('web.core');

core.action_registry.add('ts.ui', ts_widget);

});
