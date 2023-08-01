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
            $('#backend_company_logo').attr('src', '/web/image/res.company/'+session.user_companies.current_company[0]+'/logo_web');
            return this._super.apply(this, arguments);
        },

    });
    
    
}); 
