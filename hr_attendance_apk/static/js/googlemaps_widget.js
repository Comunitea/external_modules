odoo.define('hr_attendance_apk.googlemaps', function (require) {
    'use strict';

    var core = require('web.core');
    var Widget = require('web.Widget');


    var WidgetGoogleMaps = Widget.extend({
        start: function () {
            this._super();
            this.field_manager.on("field_changed:id", this, this.display_map);
            this.display_map();
        },
        display_map: function() {
            this.$el.html(QWeb.render("WidgetGoogleMaps", {
                "id": this.field_manager.get_field_value("id") || 0,
            }));
        }
    });

    core.action_registry.add(
        "googlemaps",
        WidgetGoogleMaps
    );
    return WidgetGoogleMaps;
});