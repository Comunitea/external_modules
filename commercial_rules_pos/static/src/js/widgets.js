/* Copyright 2018 GRAP - Sylvain LE GAL
   Copyright 2018 Tecnativa - David Vidal
   License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */
odoo.define('commercial_rules_pos.widgets', function (require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var chrome = require('point_of_sale.chrome');
    var pos = require('point_of_sale.models');

    var QWeb = core.qweb;
    var ScreenWidget = screens.ScreenWidget;
    var DomCache = screens.DomCache;

   
    var CommercialRuleButtonWidget = PosBaseWidget.extend({
        template: 'CommercialRuleButtonWidget',
        init: function (parent, options) {
            var opts = options || {};
            this._super(parent, opts);
            this.action = opts.action;
            this.label = opts.label;
        },

        button_click: function () {
            this.pos.get_order().apply_commercial_rules();
        },

        renderElement: function () {
            var self = this;
            this._super();
            this.$el.click(function () {
                self.button_click();
            });
        },
    });

    // var widgets = chrome.Chrome.prototype.widgets;
    // widgets.push({
    //     'name': 'commercial_rules',
    //     'widget': CommercialRuleButtonWidget,
    //     'prepend': '.pos-rightheader',
    //     'args': {
    //         'label': 'Commercial Rules',
    //     },
    // });

    // Add action button above thge NumPad
    screens.define_action_button({
        'name': 'commercial_rule',
        'widget': CommercialRuleButtonWidget,
    });

    return {
        CommercialRuleButtonWidget: CommercialRuleButtonWidget,
    };

});
