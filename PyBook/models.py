from django.db import models
__author__ = 'jbpeng'

class Book(models.Model):
    title = models.CharField(max_length=1000)
    img = models.URLField()
    rating = models.FloatField()
    rating_amount = models.CharField(max_length=20)
    tag = models.CharField(max_length=100)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

class SubCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(Category)
