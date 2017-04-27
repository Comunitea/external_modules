
odoo.define('telesale.main', function (require) {
"use strict";
var BaseWidget = require('telesale.BaseWidget');
var ts_widget = BaseWidget.TsWidget;
var core = require('web.core');

core.action_registry.add('ts.ui', ts_widget);

});
