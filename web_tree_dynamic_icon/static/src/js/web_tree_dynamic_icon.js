odoo.define('web_tree_dynamic_icon', function (require) {
    'use strict';

    var ListRenderer = require('web.ListRenderer');
    var pyUtils = require("web.py_utils");

    ListRenderer.include({
        _renderBody: function () {
            return this._super();
        },
        /**
         * Icon a buttonduring it's render
         *
         * @override
         */

        _renderButton_no_usar_aqui: function (record, node) {
            if (node && node.tag == 'button' && node.attrs.context && node.attrs.context['icon']){
                var old_icon = node.attrs.icon
                var newNode = this.computeNewNode(record, node)
                var $button = this._super(record, newNode);
                return $button
            }
            return this._super(record, node);
         },

        _renderBodyCell: function (record, node, colIndex, options) {

            if (node && node.tag == 'button' && node.attrs.context && node.attrs.context['icon']){
                var old_icon = node.attrs.icon
                var icon = node.attrs.context['icon']
                var icons = _(icon.split(';'))
                    .chain()
                    .map(this.pairColors)
                    .value()
                    .filter(function CheckUndefined(value, index, ar) {
                        return value !== undefined;
                    });
                var ctx = this.getEvalContext(record);
                for (var i=0, len=icons.length; i<len; ++i) {
                    var pair = icons[i],
                        new_icon = pair[0],
                        expression = pair[1];
                    if (py.evaluate(expression, ctx).toJSON()) {
                        node['attrs']['icon'] = new_icon;
                    }
                }
                var $cell = this._super(record, node, colIndex, options);
                console.log (old_icon + ">>" + new_icon)
                node.attrs.icon = old_icon
                return $cell;}
            return this._super(record, node, colIndex, options);

        },

        computeNewNode: function (record, oldNode){
                var icon = oldNode.attrs.context['icon']
                var icons = _(icon.split(';'))
                    .chain()
                    .map(this.pairColors)
                    .value()
                    .filter(function CheckUndefined(value, index, ar) {
                        return value !== undefined;
                    });
                var ctx = this.getEvalContext(record);
                for (var i=0, len=icons.length; i<len; ++i) {
                    var pair = icons[i],
                        new_icon = pair[0],
                        expression = pair[1];
                    if (py.evaluate(expression, ctx).toJSON()) {
                        oldNode['attrs']['icon'] = new_icon;
                    }
                }
                return oldNode
        },

        pairColors: function (pairColor) {
            if (pairColor !== "") {
                var pairList = pairColor.split(':'),
                    color = pairList[0],
                    // if one passes a bare color instead of an expression,
                    // then we consider that color is to be shown in any case
                    expression = pairList[1]? pairList[1] : 'True';
                return [color, py.parse(py.tokenize(expression)), expression];
            }
            return undefined;
        },
        getEvalContext: function (record) {
            var ctx = _.extend(
                {},
                record.data,
                pyUtils.context()
            );
            for (var key in ctx) {
                var value = ctx[key];
                if (ctx[key] instanceof moment) {
                    // date/datetime fields are represented w/ Moment objects
                    // docs: https://momentjs.com/
                    ctx[key] = value.format('YYYY-MM-DD hh:mm:ss');
                }
            }
            return ctx;
        }
    });
});
