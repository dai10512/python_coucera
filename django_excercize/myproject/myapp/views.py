from django.http import HTTPResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    text = '''Hogehoge'''
    return HTTPResponse(text)


