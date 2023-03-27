odoo.define('pos_restaurant_options.models', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var _super_order = models.Order.prototype;

    models.Order = models.Order.extend({
        initialize: function(attr, options) {
            _super_order.initialize.apply(this,arguments);
        },

        /* Overwritten because the function has no return */

        add_product: function(product, options){
            _super_order.add_product.apply(this,arguments);
            if (options.selected_attribute_value_ids) {
                this.selected_orderline.set_selected_attribute_value_ids(options.selected_attribute_value_ids);
            }
        },

    })

    var _super_orderline = models.Orderline.prototype;

    models.Orderline = models.Orderline.extend({

        initialize: function(attr, options) {
            _super_orderline.initialize.call(this,attr,options);
            this.selected_attribute_value_ids = this.selected_attribute_value_ids || [];
        },

        get_selected_attribute_value_ids: function() {
            var selected_attribute_value_ids = this.selected_attribute_value_ids;
            return selected_attribute_value_ids;
        },

        set_selected_attribute_value_ids: function(value) {
            this.selected_attribute_value_ids = value;
            this.trigger('change', this);
        },

        export_as_JSON: function() {
            var json = _super_orderline.export_as_JSON.apply(this,arguments);
            json.selected_attribute_value_ids = this.selected_attribute_value_ids;
            return json;
        },

        init_from_JSON: function(json) {
            _super_orderline.init_from_JSON.apply(this,arguments);
            this.selected_attribute_value_ids = json.selected_attribute_value_ids;
        },

        apply_ms_data: function(data) {
            if (typeof data.selected_attribute_value_ids !== "undefined") {
                this.set_selected_attribute_value_ids(data.selected_attribute_value_ids);
            }
            this.trigger('change', this);
        },

    });

    models.load_fields('product.attribute.value', ['bom_product_id']);

    var existing_models = models.PosModel.prototype.models;
    var product_index = _.findIndex(existing_models, function (model) {
        return model.model === "product.template.attribute.value";
    });
    var product_model = existing_models[product_index];

    models.load_models([{
        model:  product_model.model,
        fields: product_model.fields,
        condition:  product_model.condition,
        domain: product_model.domain,
        context: product_model.context,
        loaded: function(self, ptavs, tmp) {
            self.attributes_by_ptal_id = {};
            _.map(ptavs, function (ptav) {
                if (!self.attributes_by_ptal_id[ptav.attribute_line_id[0]]){
                    self.attributes_by_ptal_id[ptav.attribute_line_id[0]] = {
                        id: ptav.attribute_line_id[0],
                        name: tmp.product_attributes_by_id[ptav.attribute_id[0]].name,
                        display_type: tmp.product_attributes_by_id[ptav.attribute_id[0]].display_type,
                        values: [],
                    };
                }
                self.attributes_by_ptal_id[ptav.attribute_line_id[0]].values.push({
                    id: ptav.product_attribute_value_id[0],
                    name: tmp.pav_by_id[ptav.product_attribute_value_id[0]].name,
                    is_custom: tmp.pav_by_id[ptav.product_attribute_value_id[0]].is_custom,
                    html_color: tmp.pav_by_id[ptav.product_attribute_value_id[0]].html_color,
                    price_extra: ptav.price_extra,
                    bom_product_id: tmp.pav_by_id[ptav.product_attribute_value_id[0]].bom_product_id,
                });
            });
        },
    }]);


});
