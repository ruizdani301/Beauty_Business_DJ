from django.shortcuts import render, redirect
from django.db.models import Max
from django.db import connection
from ..models import Providers
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required
@staff_member_required()
def provider_register(request):
    """
      The function `provider_register` registers a new provider by retrieving the provider's name, phone
      number, and address from a POST request, creating a new `Providers` object, and saving it to the
      database.

      :param request: The `request` parameter is an object that represents the HTTP request made by the
      client. It contains information such as the HTTP method used (e.g., GET or POST), the headers, the
      body of the request, and other metadata
      :return: The code is returning a response object. If the new_provider object is an instance of
      Providers, it redirects the user to the '/management/confirmation' URL. Otherwise, it renders the
      'management/error_handling.html' template.
    """

    if request.method == "POST":
        """ obtenemos el id del producto vendido, la cantidad casteados como enteros y el precio """
        try:
            provider_name = request.POST.get("name_provider")
            phone = request.POST.get("phone")
            addres = request.POST.get("addres")
        except ValueError:
            print("Value Error")
    else:
        return render(request, "management/error_handling.html", {
        })

    last_provider = Providers.objects.all().last()
    last_provider_id = last_provider.provider_id + 1
    new_provider = Providers(provider_id=last_provider_id,
                             provider_name=provider_name,
                             phone=phone,
                             provider_address=addres)
    new_provider.save()

    if isinstance(new_provider, Providers):
        response = redirect('/management/confirmation')
        return response
    else:
        return render(request, "management/error_handling.html", {
        })


def provider(request):
    return render(request, "management/provider.html")
