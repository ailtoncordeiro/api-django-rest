from django.db import models
from users .models import Users

class TimeStamp(models.Model):
    """ Abstract class for creation and change registration """

    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updatedAt = models.DateTimeField(auto_now=True, verbose_name='updated')

    class Meta:
        abstract = True

class Addresses(TimeStamp):
    """ Class addresses """

    userID = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='User')
    description = models.CharField(max_length=255, blank=False, null=False, verbose_name='Description')
    postalCode = models.CharField(max_length=10, blank=False, null=False, verbose_name='Postal Code')
    street = models.CharField(max_length=255, blank=False, null=False, verbose_name='Street')
    complement = models.CharField(max_length=255, blank=True, null=True, verbose_name='Complement')
    neighborhood = models.CharField(max_length=255, blank=False, null=False, verbose_name='Neighborhood')
    city = models.CharField(max_length=255, blank=False, null=False, verbose_name='City')
    state = models.CharField(max_length=255, blank=False, null=False, verbose_name='State')

    class Meta:
        ordering = ['id']

class Categories(TimeStamp):
    """ Class categories """

    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Name')

    class Meta:
        ordering = ['id']

class Products(TimeStamp):
    """ class products """

    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Name')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')

    class Meta:
        ordering = ['id']


class ProductsCategories(TimeStamp):
    """ Class products categories """

    productID = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Products')
    categoriesID = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Categories')

    class Meta:
        ordering = ['id']

class Orders(TimeStamp):
    """ class orders """

    STATUS_CHOICES = (
        ("PENDENTE", "Pendente"),
        ("PAGO", "Pago"),
        ("Enviado", "Enviado"),
        ("ENTREGUE", "Entregue"),
        ("CANCELADO", "Cancelado")
    )

    userID = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='User')
    addressesID = models.ForeignKey(Addresses, on_delete=models.CASCADE, verbose_name='Address')
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, verbose_name='Status')
    orderDate = models.TimeField(auto_now_add=True, verbose_name='Order Date')

    class Meta:
        ordering = ['id']

class OrderItems(TimeStamp):
    """ Class orders items """

    orderID = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name='Order')
    productID = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Products')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    quantity = models.IntegerField(verbose_name='Quantity')

    class Meta:
        ordering = ['id']