# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class product_template(models.Model):
    _inherit= 'product.template'

    def _compute_reserve_count(self):
        reserve_qty_count = 0.0
        order_line_obj = self.env['sale.order.line']
        for template in self:
            reserve_ids = order_line_obj.search([('product_id.product_tmpl_id', '=', template.id), ('state', '=' , 'avail')])
            reserve_qty_count = sum([x.product_uom_qty for x in reserve_ids])
            template.reserve_qty = reserve_qty_count


    def _reserved_quantity_count(self):
        for sale in self:
            sale_order_ids = self.env['sale.order.line'].search([('product_id.product_tmpl_id','=',sale.id),('order_id.state','=','avail')])
            count = len(sale_order_ids)

            sale.reserved_count = count

    reserve_qty = fields.Float(string='Reserved Quantity', compute="_compute_reserve_count")
    reserved_count = fields.Integer(compute='_reserved_quantity_count', string="Reserved")


    def see_reserved_qty(self):
        sale_order_ids = self.env['sale.order.line'].search([('product_id.product_tmpl_id','=',self.id),('order_id.state','=','avail')])
        order_id = [a.id for a in sale_order_ids ]
        imd = self.env['ir.model.data']
        action = self.env.ref('stock_reservation.template_action_reserved_qty')
        list_view_id = imd._xmlid_to_res_id('sale.view_order_line_tree')

        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [[list_view_id, 'tree']],
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
        }
        result['domain'] = "[('id','in',%s)]" % order_id
        return result

class product_product(models.Model):
    _inherit= 'product.product'

    reserved_count = fields.Integer(compute='_reserved_quantity_count', string="Reserved")

    def _reserved_quantity_count(self):

        for sale in self:
            sale_order_ids = self.env['sale.order.line'].search([('product_id','=',sale.id),('order_id.state','=','avail')])

            count = len(sale_order_ids)
            sale.reserved_count = count


    def _compute_reserve_count(self):

        reserve_qty_count = 0.0
        order_line_obj = self.env['sale.order.line']

        for product in self:
            reserve_ids = order_line_obj.search([('product_id', '=', product.id), ('state', '=' , 'avail')])
            reserve_qty_count = sum([x.product_uom_qty for x in reserve_ids])
            product.reserve_qty = reserve_qty_count

    reserve_qty = fields.Float(string='Reserved Quantity', compute="_compute_reserve_count")

