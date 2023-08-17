from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count, Sum, Max
from django.db import connection
from ..models import Stock, Category, Products, Sales, Mark, Providers, Purchases
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages


@login_required
# @cache_page(60 * 15)
def sales_record(request):
    """ primero verificamos si es un metodo post """
    if request.method == "POST":
        """ obtenemos el id del producto vendido, la cantidad casteados como enteros y el precio """
        try:
            sold_product_id = int(request.POST.get("product_sale"))
            amount = int(request.POST.get("amount"))
            price = int(request.POST.get("price"))
        except ValueError:
            print("Value Error")
            response = redirect('/management/')
            return response
    else:
        response = redirect('/management/')
        return response

    """ Vamos a validar si hay unidades suficientes para efectuar la venta """
    sales_units = Stock.objects.filter(
        product_id_id=sold_product_id, amount__gt=0).aggregate(total=Sum('amount'))

    if sales_units['total'] == None:
        messages.warning(request, "No hay existencias en stock")
        return redirect('/management/')

    elif sales_units['total'] < amount:
        messages.warning(
            request, "No existen suficientes unidades para realizar la venta")
        return redirect('/management/')

    """ ahora buscamos los lotes de producto en el inventario 'stock' para descontar los vendido """
    product_in_stock = Stock.objects.filter(
        product_id_id=sold_product_id, amount__gt=0).values()

    if product_in_stock:
        for i in product_in_stock:
            if amount > 0:
                stock_id = i['stock_id']
                stock_discharge = get_object_or_404(Stock, pk=stock_id)

                if amount >= i['amount']:
                    stock_discharge.deduct_in_stock(i['amount'])
                    last_sale = Sales.objects.all().last()
                    last_sale_id = last_sale.sale_id + 1

                    sold_product = get_object_or_404(
                        Products, pk=sold_product_id)
                    sale = Sales(sale_id=last_sale_id, stock_id=stock_discharge, product_id=sold_product,
                                 amount=i['amount'], price=price, user_id=request.user.id)
                    sale.save()
                    amount -= i['amount']
                elif amount < i['amount']:
                    stock_discharge.deduct_in_stock(amount)
                    last_sale = Sales.objects.all().last()
                    last_sale_id = last_sale.sale_id + 1
                    sold_product = get_object_or_404(
                        Products, pk=sold_product_id)
                    sale = Sales(sale_id=last_sale_id, stock_id=stock_discharge,
                                 product_id=sold_product, amount=amount, price=price, user_id=request.user.id)
                    sale.save()
                    amount -= amount
                elif amount == 0:
                    break

        messages.success(request, "La venta fue realizada con exito")
        return redirect('/management/')

    messages.success(request, "La venta fue realizada con exito")
    return redirect('/management/')
