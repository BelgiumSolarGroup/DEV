# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "Website Product Booking(Reservation) Odoo",
    "version" : "17.0.0.0",
    "category" : "eCommerce",
    "depends" : ['website','website_sale', 'stock_reservation'],
    "author": "BrowseInfo",
    "summary": 'online Stock reservation for customer stock reservation online stock booking sales reservation stock LAYAWAYS stock lay-by product reservation product stock reservation Stock Booking website Product Booking item reservation website stock reservation',
    "description": """
This module use to Product Booking, Stock Booking by the customer and based on that check the available stock on the warehouse also shows the available stock after the reservation.
        It has following features.  prodcut LAYAWAYS /LAY-BY in odoo
        Sales Stock Booking, Sales Product Booking, Stock Reservation by Customer, Product Reservation, Show available stock after the reservation, Show reserved Stock by customer.
        product reservation, inventory reservation, sales reservation,
        product reserved quantity, product reserved qty, product reserved stock. 

        item reservation,warehouse reservation, reservation stock,
        item reserved quantity, item reserved qty, item reserved stock. 
 Odoo LAYAWAYS /LAY-BY booking product booking stock booking item 
        odoo Sales Stock Booking Sales Product Booking Stock Reservation by Customer Product Reservations
        odoo Show available stock after the reservation Show reserved Stock by customer 
        odoo product reservation inventory reservation sales reservation odoo
        odoo product reserved quantity product reserved qty product reserved stock item reservation warehouse reservation
        odoo reservation stock item reserved quantity item reserved qty item reserved stock. 
        odoo product catalog reservation inventory catalog reservation sales catalog reservation
        odoo product catalog reserved quantity product catalog reserved qty product catalog reserved stock. 


        This module use to Product Booking, Stock Booking by the customer and based on that check the available stock on the warehouse also shows the available stock after the reservation.
        It has following features.  prodcut LAYAWAYS /LAY-BY in odoo
        Sales Stock Booking, Sales Product Booking, Stock Reservation by Customer, Product Reservation, Show available stock after the reservation, Show reserved Stock by customer.
        product reservation, inventory reservation, sales reservation,
        product reserved quantity, product reserved qty, product reserved stock. 

        item reservation,warehouse reservation, reservation stock,
        item reserved quantity, item reserved qty, item reserved stock. 
        product catalog reservation, inventory catalog reservation, sales catalog reservation,
        product catalog reserved quantity, product catalog reserved qty, product catalog reserved stock. 
        Website product reservation,Website inventory reservation,Website sales reservation,
        Website product reserved quantity,Webite product reserved qty,Website product reserved stock. 

        Website item reservation,Website warehouse reservation,Website reservation stock,
        Website item reserved quantity,Website item reserved qty,Website item reserved stock. 

        Website product catalog reservation,Website inventory catalog reservation,Website sales catalog reservation,
        Website product catalog reserved quantity,Website product catalog reserved qty,Website product catalog reserved stock. 


Este módulo se utiliza para la Reserva de productos, Reservas de stock por parte del cliente y, en función de ese control, las existencias disponibles en el almacén también muestran el stock disponible después de la reserva.
        Tiene las siguientes características.
        Reserva de venta de valores, Reserva de productos de venta, Reserva de existencias por parte del cliente, Reserva de productos, Mostrar stock disponible después de la reserva, Mostrar stock reservado por cliente.
        reserva de producto, reserva de inventario, reserva de venta,
        cantidad reservada del producto, cantidad reservada del producto, stock reservado del producto.

        reserva de artículo, reserva de almacén, stock de reserva,
        artículo cantidad reservada, artículo reservado cantidad, artículo stock reservado.

        reserva del catálogo de productos, reserva del catálogo de inventario, reserva del catálogo de ventas,
        cantidad reservada del catálogo de productos, catálogo de productos cantidad reservada, inventario de productos reservados.
        Reserva de productos del sitio web, reserva de inventario del sitio web, reserva de ventas del sitio web,
        Cantidad reservada del producto del sitio web, cantidad de productos reservados de Webite, stock reservado del producto del sitio web.

        La reserva de un sitio web, la reserva del sitio web del almacén, el stock de reservas del sitio web,
        Cantidad reservada del artículo del sitio web, cantidad reservada del artículo del sitio web, stock reservado del artículo del sitio web.

        Reserva del catálogo de productos del sitio web, reserva del catálogo del inventario del sitio web, reserva del catálogo de ventas del sitio web,
        Cantidad reservada del catálogo del sitio web, cantidad reservada del catálogo del sitio web, stock reservado del catálogo del sitio web.

Ce module est utilisé pour la réservation de produits, la réservation de stock par le client et, sur la base de ce contrôle, le stock disponible sur l'entrepôt indique également le stock disponible après la réservation.
        Il a les caractéristiques suivantes.
        Vente Stock Réservation, Vente Produit Réservation, Stock Réservation par le client, Réservation de produit, Afficher stock disponible après la réservation, Afficher réservé Stock par le client.
        réservation de produit, réservation d'inventaire, réservation de vente,
        produit quantité réservée, produit réservé quantité, produit réservé stock.

        réservation d'articles, réservation d'entrepôt, stock de réservation,
        article quantité réservée, article réservé quantité, article réservé stock.

        réservation de catalogue de produits, réservation de catalogue d'inventaire, réservation de catalogue de vente,
        catalogue de produits quantité réservée, catalogue de produits quantité réservée, catalogue de produits réserve réservée.
        Réservation de produit de site Web, réservation d'inventaire de site Web, réservation de vente de site Web,
        Site web produit quantité réservée, site web produit quantité réservée, site web produit stock réservé.

        Réservation d'un élément de site Web, réservation d'un site Web, stock de réservation de site Web,
        Quantité de site Web réservée, Quantité de site Web réservée, Objet de site Web réservé.

        Réservation de catalogue de produits sur le site Web, réservation de catalogue d'inventaire de site Web, réservation de catalogue de vente de site Web,
        Site internet produit catalogue quantité réservée, site internet catalogue de produits quantité réservée, site internet catalogue de produits stock réservé.

   
    """,
    "website" : "https://www.browseinfo.com",
    'price': '20',
    'license': 'OPL-1',
    'currency': "EUR",
    "data": [
        'data/data.xml',
        'views/product_view.xml',
        'views/templates.xml',
    ],
    "auto_install": False,
    "application": True,
    "installable": True,
    "live_test_url":'https://youtu.be/obNbSsMiQr0',
    "images":['static/description/Banner.gif']
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
