# -*- coding: utf-8 -*-
#################################################################################
# Author      : CFIS (<https://www.cfis.store/>)
# Copyright(c): 2017-Present CFIS.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://www.cfis.store/>
#################################################################################

{
    "name": "Create Quotation from Portal | Portal Sale Quotation Create | Portal Quick Quotation | Quick Quotation | Portal Create Quotation",
    "summary": """
        This module allows your clients to generate quotations by filling out a products form from portal and submitting it.
    """,
    "version": "17.1",
    "description": """
        This module allows your clients to generate quotations by filling out a products form from portal and submitting it.
        Create Quotation from Portal
        Portal Sale Quotation Create
        Project Quick Quotation
        Quick Quotation
    """,    
    "author": "CFIS",
    "maintainer": "CFIS",
    "license" :  "Other proprietary",
    "website": "https://www.cfis.store",
    "images": ["images/portal_quick_quotation.png"],
    "category": "Project",
    "depends": [
        "base",
        "sale",
        "product",
        "sale_management",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_portal_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "/portal_quick_quotation/static/src/css/*.css",
            "/portal_quick_quotation/static/src/js/*.js",
        ],
    },
    "installable": True,
    "application": True,
    "price"                 :  75,
    "currency"              :  "EUR",
    "pre_init_hook"         :  "pre_init_check",
}
