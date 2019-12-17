odoo.define('web_tree_dynamic_colored_field_external', function (require) {
    'use strict';

    var ListRenderer = require('web.ListRenderer');
    var pyeval = require('web.pyeval');

        ListRenderer.include({

        applyColorize: function ($td, record, node, ctx) {
            // safely resolve value of `color_field` given in <tree>
            var treeColor = record.data[this.colorField];
            if (treeColor) {
                $td.css('color', treeColor);
            }
            // apply <field>'s own `options`
            if (!node.attrs.options) { return; }
            if (node.tag !== 'field' && node.tag !== 'button') { return; }
            var nodeOptions = node.attrs.options;
            if (!_.isObject(nodeOptions)) {
                nodeOptions = pyeval.py_eval(nodeOptions);
            }
            this.applyColorizeHelper($td, nodeOptions, node, 'fg_color', 'color', ctx);
            this.applyColorizeHelper($td, nodeOptions, node, 'bg_color', 'background-color', ctx);
        },
});
});
