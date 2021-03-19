from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def food(request):
    return HttpResponse('This is food page.')


def who(request):
    return HttpResponse('This is who page.')


def result(request):
    return HttpResponse('This is result page.')


def home(request):
    return render(request, 'home.html')


def terms_of_service(request):
    return render(request, "terms_of_service.html")
