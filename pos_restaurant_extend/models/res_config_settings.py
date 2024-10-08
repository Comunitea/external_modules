from odoo import _, api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    pos_service_level = fields.Integer(
        related='pos_config_id.service_level',
        readonly=False
    )

    pos_service_level_default = fields.Boolean(
        related='pos_config_id.service_level_default',
        readonly=False
    )

    pos_service_level_categories = fields.Many2many(related='pos_config_id.service_level_categories', readonly=False)

    pos_receipt_logo = fields.Binary(
        related='pos_config_id.receipt_logo',
        readonly=False
    )

    pos_receipt_company_label_1 = fields.Char(
        related='pos_config_id.receipt_company_label_1',
        readonly=False
    )

    pos_receipt_company_label_2 = fields.Char(
        related='pos_config_id.receipt_company_label_2',
        readonly=False
    )

    pos_receipt_company_vat = fields.Char(
        related = 'pos_config_id.receipt_company_vat',
        readonly=False
    )

    pos_receipt_company_address_1 = fields.Char(
        related='pos_config_id.receipt_company_address_1',
        readonly=False
    )

    pos_receipt_company_address_2 = fields.Char(
        related='pos_config_id.receipt_company_address_2',
        readonly=False
    )

    pos_receipt_company_phone = fields.Char(
        related='pos_config_id.receipt_company_phone',
        readonly=False
    )

    pos_print_address = fields.Boolean(
        related='pos_config_id.print_address',
        readonly=False
    )

    #Se puede convertir en json
    pos_floor_facility_ids = fields.Json(
        string='Floor facility',
        related='pos_config_id.floor_facility_ids',
        readonly=False
    )

    pos_show_guests_popup = fields.Boolean(
        related='pos_config_id.show_guests_popup',
        readonly=False
    )

    pos_session_close_send = fields.Boolean(
        related='pos_config_id.session_close_send',
        readonly=False)
    
    pos_session_close_partner = fields.Many2one(
        related='pos_config_id.session_close_partner',
        readonly=False)
    
    pos_iface_not_autoprint_cash = fields.Boolean(
        related='pos_config_id.iface_not_autoprint_cash',
        readonly=False)