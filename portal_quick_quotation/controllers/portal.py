import json
import base64

from odoo import http, _, SUPERUSER_ID
from odoo.tools import consteq

from odoo.exceptions import AccessError, MissingError, UserError
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request

class PortalQuickQuotation (http.Controller):

    @http.route('/portal_quick_quotation/get_salespersons_data', type='json', auth='public', website=True)
    def get_salespersons_data(self, **kw):
        domain = [('groups_id', '=', [request.env.ref('sales_team.group_sale_salesman').id]),('share', '=', False),('company_ids', '=', request.env.company.id)]
        salespersons = request.env['res.users'].sudo().search_read(domain, ['name', 'id'])
        return salespersons
    
    @http.route('/portal_quick_quotation/get_products_data', type='json', auth='public', website=True)
    def get_products_data(self, **kw):
        products = request.env['product.product'].sudo().search_read([], ['display_name', 'id' , 'uom_id'])
        return products
    
    @http.route('/portal_quick_quotation/submit_quick_quotation', type='json', auth='public', website=True)
    def submit_quick_quotation(self, data, salesperson, **kw):
        lines = []
        if not data or not salesperson:
            return
        
        if not request.env.user.partner_id.id:
            return

        sale_sudo = request.env['sale.order'].sudo()
        
        for d in data:
            val= {
                'product_id': d['product_id'],
                'product_uom_qty': d['qty'],
            }
            lines.append((0,0,val))
            
        vals = {
            'partner_id': int(request.env.user.partner_id.id),
            'user_id': int(salesperson),
            'order_line': lines,
        }
        sale_order = sale_sudo.create(vals)
        sale_order.action_quotation_sent()
        return sale_order.id

class QuoationCustomerPortal(CustomerPortal):

    @http.route(['/my/quotes/create_new'], type='http', auth="user", website=True)
    def create_new_quotation(self, access_token=None):
        if not request.session.uid:
            return {'error': 'anonymous_user'}
        
        values = {
            'page_name': 'create_new_quotation',
            'logged_partner': request.env.user.partner_id,
        }
        return request.render("portal_quick_quotation.create_new_quotation", values)