#coding:utf-8
__author__ = 'jbpeng'
from django.http import HttpResponse, Http404
from PyBook import douban
import datetime
from django.shortcuts import render_to_response
def hello(request):
    return HttpResponse("Hello world")

def current_time(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def time_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()

    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def show_books(request, tag, amount):
    try:
        amount = int(amount)
    except ValueError:
        raise Http404()
    books = douban.gethotbooks(tag, amount)
    return render_to_response("books.html", locals())