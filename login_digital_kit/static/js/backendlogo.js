/*  # © 2023 Comunitea
    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).   */

odoo.define('login_digital_kit.backendlogo', function (require) {
    "use strict";

    const AppsMenu = require("web.AppsMenu");

    require("web.dom_ready");    
    var core = require('web.core');
    var session = require('web.session');
    var _t = core._t;

    AppsMenu.include({        
        init: function (parent, menuData) {
            this._super.apply(this, arguments);
        },

        /**
         * @override
         */
        start: function () {
            this._is_enabled_logo(session.user_context.allowed_company_ids[0]);
            return this._super.apply(this, arguments);
        },

        _is_enabled_logo: function (company_id) {
            var self = this;
            var def = $.Deferred();company_id
            var params = {
                model: 'res.company',
                method: 'search_read',
                domain: [['id', '=', company_id]],
                fields: ['show_backend_logo'],
            };
            return self._rpc(params).then(function (result) {
                if (result.length > 0 && result[0].show_backend_logo) {
                    $('#backend_company_logo').attr('src', '/web/image?model=res.company&id=' + company_id + '&field=logo');
                } else {
                    $('#backend_company_logo_row').removeClass().addClass('d-none');
                }
            });
        },

    });
    
    
}); 
