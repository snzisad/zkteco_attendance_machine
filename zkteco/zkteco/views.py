from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.shortcuts import redirect, render

def index(request):
    return render(request, "home.html")