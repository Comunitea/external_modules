# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class SignenCreateUser(models.TransientModel):

    _name = "signen.create.user"

    username = fields.Char(required=True)
    password = fields.Char(required=True)
    company_id = fields.Many2one("res.company", "Company", required=True)

    def create_user(self):
        user = self.env["signen.configuration.user"].create(
            {
                "username": self.username,
                "password": self.password,
                "company_id": self.company_id.id,
            }
        )
        user.with_delay().signen_create_user()
