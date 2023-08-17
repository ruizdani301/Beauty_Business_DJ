from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from ..models import Category, Products, Mark
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages


@login_required
@staff_member_required()
def product_register(request):
    """
      The function `product_register` saves a new product to the database based on the data received in a
      POST request.

      :param request: The `request` parameter is an object that represents the HTTP request made by the
      client. It contains information such as the HTTP method used (GET, POST, etc.), the data sent in the
      request, and other metadata
      :return: The code is not returning anything.
    """

    if request.method == "POST":
        try:
            product_name = request.POST.get("name_product")
            mark = request.POST.get("mark")
            category = request.POST.get("category")
        except ValueError:
            print("Value Error")
    else:
        return render(request, "management/error_handling.html", {
        })

    last_product = Products.objects.all().last()
    if last_product is None:
        last_product_id = 1
    else:
        last_product_id = last_product.product_id + 1
    mark_obj = get_object_or_404(Mark, pk=mark)
    category_obj = get_object_or_404(Category, pk=category)
    new_product = Products(product_id=last_product_id,
                           name_product=product_name,
                           category_id=category_obj,
                           mark_id=mark_obj)

    new_product.save()

    if isinstance(new_product, Products):
        response = redirect('/management/confirmation')
        return response
    else:
        return render(request, "management/error_handling.html", {
        })
