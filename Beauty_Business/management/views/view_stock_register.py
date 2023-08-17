from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from ..models import Stock, Products, Purchases
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required
@staff_member_required()
def stock_register(request):
    """
      The `stock_register` function is a view that handles the creation of a new stock register entry, and
      the `confirmation` function renders a confirmation page.

      :param request: The request object, which contains information about the current HTTP request
      :return: The code is returning a redirect response to the '/management/confirmation' URL if the
      new_stock_register object is an instance of the Stock class. Otherwise, it is rendering the
      'management/error_handling.html' template.
    """

    if request.method == "POST":
        try:
            purchase = request.POST.get("factura")
            product = request.POST.get("product")
            purchase_price = int(request.POST.get("purchase_price"))
            sales_price = int(request.POST.get("sales_price"))
            amount = int(request.POST.get("amount"))
        except ValueError:
            print("Value Error")
    else:
        return render(request, "management/error_handling.html", {
        })
    last_stock_register = Stock.objects.all().last()
    if last_stock_register is None:
        last_stock_register_id = 1
    else:
        last_stock_register_id = last_stock_register.stock_id + 1
    purchase_obj = get_object_or_404(Purchases, pk=purchase)
    product_obj = get_object_or_404(Products, pk=product)
    new_stock_register = Stock(stock_id=last_stock_register_id,
                               purchase_id=purchase_obj,
                               product_id=product_obj,
                               purchase_price=purchase_price,
                               sales_price=sales_price,
                               total=amount,
                               amount=amount,
                               sales_st=0)
    new_stock_register.save()

    if isinstance(new_stock_register, Stock):
        response = redirect('/management/confirmation')
        return response
    else:
        return render(request, "management/error_handling.html", {
        })


def confirmation(request):
    return render(request, "management/confirmation.html", {
    })


def stock(request):

    all_purchase = Purchases.objects.all()
    return render(request, "management/register_stock.html/",
                  {"all_purchases": all_purchase})
