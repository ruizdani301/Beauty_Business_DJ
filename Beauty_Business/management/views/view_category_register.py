from django.shortcuts import render, redirect
from ..models import Category
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required
@staff_member_required()
def category_register(request):
    """
      The function `category_register` registers a new category based on the user's input and returns a
      confirmation message or an error message.

      :param request: The `request` parameter is an object that represents the HTTP request made by the
      client. It contains information such as the method used (GET, POST, etc.), the data sent in the
      request, and other metadata
      :return: a response object. If the new_category is an instance of the Category model, it redirects
      the user to the '/management/confirmation' URL. Otherwise, it renders the
      'management/error_handling.html' template.
    """
    if request.method == "POST":

        try:
            category_name = request.POST.get("new_category")
        except ValueError:
            print("Value Error")
    else:
        return render(request, "management/error_handling.html", {
        })

    last_category = Category.objects.all().last()
    if last_category is None:
        last_category_id = 1
    else:
        last_category_id = last_category.category_id + 1
    new_category = Category(category_id=last_category_id,
                            name_category=category_name)
    print(new_category.name_category)
    new_category.save()

    if isinstance(new_category, Category):
        response = redirect('/management/confirmation')
        return response
    else:
        return render(request, "management/error_handling.html", {
        })
