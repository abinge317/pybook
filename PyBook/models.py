from django.db import models
__author__ = 'jbpeng'

class Book(models.Model):
    title = models.CharField(max_length=1000)
    img = models.URLField()
    rating = models.FloatField()
    rating_amount = models.CharField(max_length=20)
    tag = models.CharField(max_length=100)
