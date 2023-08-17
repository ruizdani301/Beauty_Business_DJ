from django.shortcuts import render
from django.db import connection
from ..models import Stock, Products
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
# @cache_page(60 * 15)
def index(request):
    products_available = Stock.objects.raw(
        '''SELECT 1 AS stock_id, s.product_id_id,
            sum(s.amount) AS total,
            MAX(s.sales_price) AS price,
            p.name_product AS nombre
        FROM stock AS s
        INNER JOIN products AS p ON s.product_id_id = p.product_id
        WHERE s.amount > 0
        GROUP BY s.product_id_id, p.name_product ORDER BY s.product_id_id'''
    )
    latest_Products = Products.objects.all()

    return render(request, "management/index.html", {
        "latest_Products": latest_Products,
        "products_available": products_available,
        "username": request.user.username
    })
