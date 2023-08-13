from django.shortcuts import render
from django.db import connection
from ..models import Stock
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page


@login_required
#@cache_page(60 * 15)
def get_stock_all_items(request):
    '''Get all products available in stock'''
    stock_available = Stock.objects.raw(
        '''SELECT 1 AS stock_id, s.product_id_id,
            sum(s.amount) AS total,
            MAX(s.sales_price) AS price,
            p.name_product AS nombre,
            s.sales_price AS precio
        FROM stock AS s
        INNER JOIN products AS p ON s.product_id_id = p.product_id
        WHERE s.amount > 0
        GROUP BY s.product_id_id, p.name_product, s.sales_price ORDER BY s.product_id_id'''
    )
    return render(request, "management/stock.html", {
        'stock_available': stock_available,

    })


@login_required
def get_stock_by_name(request, name):
    '''Get all products available in stock by name'''
    stock_available = Stock.objects.raw(
        '''SELECT 1 AS stock_id, s.product_id_id,
            sum(s.amount) AS total,
            MAX(s.sales_price) AS price,
            p.name_product AS nombre,
            s.sales_price AS precio
        FROM stock AS s
        INNER JOIN products AS p ON s.product_id_id = p.product_id
        WHERE s.amount > 0 AND p.name_product LIKE %s
        GROUP BY s.product_id_id, p.name_product, s.sales_price
        ORDER BY s.product_id_id''', [name + '%']
    )
    return render(request, "management/stock.html", {
        'stock_available': stock_available,

    })


@login_required
def get_stock_by_id(request, id):
    '''Get all products available in stock by ID'''
    stock_available = Stock.objects.raw(
        '''SELECT 1 AS stock_id, s.product_id_id,
            sum(s.amount) AS total,
            MAX(s.sales_price) AS price,
            p.name_product AS nombre
        FROM stock AS s
        INNER JOIN products AS p ON s.product_id_id = p.product_id
        WHERE s.amount > 0 AND s.product_id_id = %s
        GROUP BY s.product_id_id, p.name_product
        ORDER BY s.product_id_id''', [id]

    )
    return render(request, "management/stock.html", {
        'stock_available': stock_available,

    })
