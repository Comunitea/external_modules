openerp.hr_attendance_apk = function(instance, local) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    local.WidgetGoogleMaps = instance.web.form.FormWidget.extend({
        start: function() {
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

    instance.web.form.custom_widgets.add('googlemaps', 'instance.hr_attendance_apk.WidgetGoogleMaps');
}