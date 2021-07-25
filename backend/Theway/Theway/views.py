
from django.http.response import HttpResponse
from .getData import data_scrap



def getData(request):
    data_scrap()
    return HttpResponse("Hello")
