from django.db import models

# Create your views here.


class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()


class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()


class Cart(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()


class Order(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()


class OrderItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
