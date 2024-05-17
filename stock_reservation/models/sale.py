# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import datetime
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class sale_order(models.Model):
    _inherit = 'sale.order'

    sale_type = fields.Selection([('reservation', 'Reservation'), ('quotation', 'Quotation')], string='Type')
    state = fields.Selection(selection_add=[('waiting', 'Waiting Availability'), ('avail', 'Available')])

    @api.model
    def create(self, vals):
        new_id = super(sale_order, self).create(vals)
        count = 0
        if not new_id.order_line:
            new_id.state = 'draft'
            return new_id
        else:
            for line_brw in new_id.order_line:
                if line_brw.product_id.type == 'product':
                    if line_brw.product_uom_qty > (line_brw.product_id.qty_available - line_brw.product_id.reserve_qty):
                        count += 1
        if count == 0:
            new_id.state = 'avail'
        else:
            new_id.state = 'waiting'
        if new_id.date_order:
            days_exp = self.env['res.config.settings'].sudo().search([], limit=1, order="id desc").resevation_exp_day
            new_id.validity_date = (fields.Date.from_string(new_id.date_order)) + datetime.timedelta(days=int(days_exp))
        return new_id


    def write(self, vals):
        super(sale_order, self).write(vals)
        count = 0
        if vals.get('order_line'):
            if not self.order_line:
                self.state = 'draft'
                return True
            else:
                for line_brw in self.order_line:
                    if line_brw.product_id.type == 'product':
                        if line_brw.product_uom_qty > (
                                    line_brw.product_id.qty_available - line_brw.product_id.reserve_qty):
                            count += 1
            if count == 0:
                self.state = 'avail'
            else:
                self.state = 'waiting'
        return True


    def button_force_avail(self):
        for record in self:
            record.state = 'avail'
        return True


    def button_chk_avail(self):
        count = 0
        for line_brw in self.order_line:
            if line_brw.product_id.type == 'product':
                if line_brw.product_uom_qty > (line_brw.product_id.qty_available - line_brw.product_id.reserve_qty):
                    count += 1
        if count == 0:
            self.state = 'avail'
        else:
            self.state = 'waiting'
        return True


    def _find_expired_order(self):
        search_order = self.search([('state', 'in', ['waiting', 'avail']), ('sale_type', '=', 'reservation')])
        for order in search_order:
            if (fields.Date.from_string(order.validity_date)) < datetime.datetime.today().date():
                order.action_cancel()
