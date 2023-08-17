/** @odoo-module **/

import { NavBar } from '@web/webclient/navbar/navbar';
import { session } from "@web/session";
import { registry } from "@web/core/registry";
import { patch } from 'web.utils';
import { buildQuery } from 'web.rpc';
import ajax from 'web.ajax';

const websiteSystrayRegistry = registry.category('website_systray');
const { useEffect } = owl;

patch(NavBar.prototype, 'backendlogo', {
    dependencies: ["rpc"],
    setup() {
        this._super();
        console.log("session => ", session);
        console.log("session.company_id => ", session.company_id);
        this._is_enabled_logo(session.user_companies.current_company);
    },

    _is_enabled_logo: async function (company_id) {
        var self = this;
        var def = $.Deferred();

        var params = {
            model: 'res.company',
            method: 'search_read',
            domain: [['id', '=', company_id]],
            fields: ['show_backend_logo'],
        };

        const query = buildQuery(params);
        ajax.rpc(query.route, query.params).then(function (result) {
            if (result.length > 0 && result[0].show_backend_logo) {
                $('#backend_company_logo').attr('src', '/web/image?model=res.company&id=' + company_id + '&field=logo');
            } else {
                $('#backend_company_logo_row').removeClass().addClass('d-none');
            }
        });
    },
});
