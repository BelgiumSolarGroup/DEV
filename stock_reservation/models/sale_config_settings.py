# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class sale_configuration_settings(models.TransientModel):
    _inherit = "res.config.settings"


    resevation_exp_day = fields.Char(string='Reservation Expired Days',default='14')

    @api.model
    def default_get(self, fields_list):
        res = super(sale_configuration_settings, self).default_get(fields_list)
        if self.search([], limit=1, order="id desc").resevation_exp_day:
            resevation_exp_day = self.search([], limit=1, order="id desc").resevation_exp_day
            res.update({
                        'resevation_exp_day':resevation_exp_day
                      })
            
        return res
