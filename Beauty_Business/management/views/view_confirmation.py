from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


def confirmation(request):
    return render(request, "management/confirmation.html", {
    })
