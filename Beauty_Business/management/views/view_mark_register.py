from django.shortcuts import render, redirect
from ..models import Mark
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages


@login_required
@staff_member_required()
def mark_register(request):
    if request.method == "POST":
        """ obtenemos el id del producto vendido, la cantidad casteados como enteros y el precio """
        try:
            mark_name = request.POST.get("new_mark")
        except ValueError:
            print("Value Error")
    else:
        return render(request, "management/error_handling.html", {
        })

    last_mark = Mark.objects.all().last() + 1
    if last_mark is None:
        last_mark_id = 1
    else:
        last_mark_id = last_mark.mark_id + 1
    new_mark = Mark(mark_id=last_mark_id, name_mark=mark_name)
    new_mark.save()

    if isinstance(new_mark, Mark):
        response = redirect('/management/confirmation')
        return response
    else:
        messages.warning(request, "No hay existencias en stock")
        return redirect('/management/')

    return render(request, "management/error_handling.html", {
    })
