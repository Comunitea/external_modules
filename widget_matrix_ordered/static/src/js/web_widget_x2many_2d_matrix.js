odoo.define('widget_matrix_ordered.widget2', function (require) {
"use strict";

var core = require('web.core');
    var formats = require('web.formats');
    var MatrixWidget2 = core.form_widget_registry.get('x2many_2d_matrix');
    var MatrixWidget = require('web_widget_x2many_2d_matrix.widget');

var WidgetX2Many2dMatrix = MatrixWidget2.include({
    init: function(field_manager, node){
        this.x_axis_order = node.attrs.x_axis_order || this.x_axis_order;
        this.y_axis_order = node.attrs.y_axis_order || this.y_axis_order;
        this._super(field_manager, node);
    },
    add_xy_row: function(row){
        this._super(row);
        this.x_order = row.x_order
        this.y_order = row.y_order
    },
     // get x axis values in the correct order
    get_x_axis_values: function()
    {   
        var self=this;
        var res = this._super()
        if ( !(_.isEmpty(this.x_order)) ){
            res = this.x_order.split(',')
        }
        return res
    },

    // get y axis values in the correct order
    get_y_axis_values: function()
    {   
        var self=this;
        var res = this._super()
        if ( !(_.isEmpty(this.y_order)) ){
            res = this.y_order.split(',')
        }
        return res
    },
});


});


