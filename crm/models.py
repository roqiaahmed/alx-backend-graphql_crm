from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True, null=False)
    phone = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField()
    stock = models.IntegerField(default=0)


class Order(models.Model):
    STATUS = {
        "INPROGRESS": "inprogress",
        "DONE": "done",
        "CANCELED": "canceled",
    }
    status = models.CharField(max_length=15, default="INPROGRESS", choices=STATUS)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name="orders")
    total_amount = models.FloatField()
    order_date = models.DateTimeField(auto_now=True)
