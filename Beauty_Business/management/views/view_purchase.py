from django.shortcuts import render, redirect
from django.db import connection
from ..models import Category, Products, Mark, Purchases
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required
@staff_member_required()
def purchases(request):
    """
      The function "purchases" retrieves all marks, categories, purchases, and products from the database   and renders them in the "purchases.html" template.
      param request: The `request` parameter is an object that represents the HTTP request made by the
      client. It contains information such as the request method, headers, and body
      :return: a rendered HTML template called "management/purchases.html" with the following context
      variables: "all_marks", "all_categories", "all_purchases", and "all_products".
    """

    all_marks = Mark.objects.all()
    all_categories = Category.objects.all()
    all_purchases = Purchases.objects.all()
    all_products = Products.objects.all()
    return render(request, "management/purchases.html", {
        "all_marks": all_marks,
        "all_categories": all_categories,
        "all_purchases": all_purchases,
        "all_products": all_products
    })
