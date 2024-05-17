# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import json
import datetime
from odoo import _
from odoo import http, SUPERUSER_ID
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.website_sale.controllers.main import WebsiteSale
PPG = 20  # Products Per Page
PPR = 4   # Products Per Row

class WebsiteSaleStockReservation(WebsiteSale):

    @http.route(['/reservation/update'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def reservation_update(self, product_id, add_qty=1, set_qty=0, **kw):
        product_custom_attribute_values = None
        if kw.get('product_custom_attribute_values'):
            product_custom_attribute_values = json.loads(kw.get('product_custom_attribute_values'))

        request.website.sale_get_order(force_create=1)._cart_update(
            product_id=int(product_id),
            add_qty=float(add_qty),
            set_qty=float(set_qty),
            product_custom_attribute_values=product_custom_attribute_values
        )
        
        # if product is reserve_products, click on Reserve Button
        if kw.get('sale_type') == 'reservation':
            request.website.sale_get_order().sale_type = 'reservation';
                    
        return request.redirect("/shop/cart")

    @http.route(['/shop/confirm_order'], type='http', auth="public", website=True)
    def confirm_order(self, **post):
        order = request.website.sale_get_order()
        
        # if product is reserve_products
        if order.sale_type == 'reservation':
            order.action_quotation_send()
            order.button_chk_avail()
            request.website.sale_reset()
            return request.render("website_stock_reservation.reservation_thankyou", {'order': order})
            
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        order._onchange_partner_shipping_id()
        order.order_line._compute_tax_id()
        request.session['sale_last_order_id'] = order.id
        request.website.sale_get_order(update_pricelist=True)
        extra_step = request.env.ref('website_sale.extra_info')
        if extra_step.active:
            return request.redirect("/shop/extra_info")

        return request.redirect("/shop/payment")
                
        
class WebsiteStockReservation(http.Controller):
    @http.route(['/reservation','/reservation/page/<int:page>'], type='http', auth="public", website=True)
    def reservation(self,page=1,ppg=False,**post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        values = {}
        
        
        context = dict(request.env.context or {})
        context.update({'from': 'yes'})
        
        ProductObj = request.env['product.template']

        domain = []

        domain += [('reserve_products','=',True),("website_published", "=", True)]

        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG


        product_count = ProductObj.sudo().search_count(domain)
        pager = request.website.pager(
            url="/reservation",
            total=product_count,
            page=page,
            scope=7,
            step=ppg

        )

        products = ProductObj.sudo().search(domain, limit=ppg, offset=pager['offset'])
        request.session['my_reserve_products'] = products.ids[:100]
        request.session['from_reserve_pro'] = 'yes'
        values.update({
            'products': products,
            'page_name': 'Reserve Products',
            'pager': pager,
            'default_url': '/reservation',
            })

        return request.render("website_stock_reservation.reservation",values)
        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
