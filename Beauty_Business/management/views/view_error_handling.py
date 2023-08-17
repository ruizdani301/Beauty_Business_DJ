from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def error_handling(request):
    return render(request, "management/error_handling.html", {
    })
