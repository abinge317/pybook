#coding:utf-8
__author__ = 'jbpeng'
from django.http import HttpResponse, Http404
from PyBook import douban
from PyBook.models import Book
import datetime
import hashlib
from django.shortcuts import render_to_response
from django.core.cache import cache

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

def show_books(request, tag='编程', amount='10'):
    try:
        amount = int(amount)
    except ValueError:
        raise Http404()
    key = 'all_books'+hashlib.md5(tag.encode('utf8')).hexdigest()
    all_books = cache.get(key)
    if not all_books:
        all_books = Book.objects.filter(tag=tag).order_by('-rating')
        if len(all_books) == 0:
            douban.gethotbooks(tag)
            all_books = Book.objects.filter(tag=tag).order_by('-rating')
        cache.set(key, all_books)
    books = all_books[:amount]
    amount = len(books)
    all_tags = Book.objects.values('tag').distinct()

    return render_to_response("books.html", locals())
