# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, api, tools


class IrUiMenu(models.Model):

    _inherit = "ir.ui.menu"

    @api.model
    @tools.ormcache('frozenset(self.env.user.groups_id.ids)', 'debug')
    def _visible_menu_ids(self, debug=False):
        """ Return the ids of the menu items visible to the user. """
        # retrieve all menus, and determine which ones are visible
        context = {'ir.ui.menu.full_list': True}
        menus = self.with_context(context).search([])

        groups = self.env.user.groups_id
        if not debug:
            groups = groups - self.env.ref('base.group_no_one')
        visible_apps = menus.filtered(lambda x: not x.parent_id and
                                      (not x.groups_id or
                                       x.groups_id & groups))
        # first discard all menus with groups the user does not have
        menus = self.with_context(context).search([('id', 'child_of',
                                                    visible_apps.ids)])
        menus = menus.filtered(
            lambda menu: not menu.groups_id or menu.groups_id & groups)

        # take apart menus that have an action
        action_menus = menus.filtered(lambda m: m.action and m.action.exists())
        folder_menus = menus - action_menus
        visible = self.browse()

        # process action menus, check whether their action is allowed
        access = self.env['ir.model.access']
        MODEL_GETTER = {
            'ir.actions.act_window': lambda action: action.res_model,
            'ir.actions.report': lambda action: action.model,
            'ir.actions.server': lambda action: action.model_id.model,
        }
        for menu in action_menus:
            get_model = MODEL_GETTER.get(menu.action._name)
            if not get_model or not get_model(menu.action) or \
                    access.check(get_model(menu.action), 'read', False):
                # make menu visible, and its folder ancestors, too
                ancestors = self.browse()
                ancestors += menu
                menu = menu.parent_id
                if menu and menu not in menus:
                    ancestors = self.browse()
                    menu = False
                while menu and menu in folder_menus and menu not in visible:
                    if menu in menus:
                        ancestors += menu
                        menu = menu.parent_id
                    else:
                        ancestors = self.browse()
                        menu = False
                visible += ancestors

        return set(visible.ids)
