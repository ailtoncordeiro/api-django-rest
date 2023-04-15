from django.db import models
from validate_email import validate_email
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class TimeStamp(models.Model):
    """ Abstract class for creation and change registration """

    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updatedAt = models.DateTimeField(auto_now=True, verbose_name='updated')

    class Meta:
        abstract = True

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, name=None):
        """ Create and saver User with name, email and password """

        if not validate_email(email):
            raise ValueError('Users must have an email address')

        user = self.model(
            email = email,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password=None, name=None):
        """ Creates and saves a superuser with the given email and password. """
        user = self.create_user(
            email=email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    """ Class user """

    name = models.CharField(max_length=255, blank=True, verbose_name='Name')
    email = models.EmailField(blank=False, null=False, unique=True, verbose_name='e-mail')
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
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

class Categories(TimeStamp):
    """ Class categories """

    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Name')

class Products(TimeStamp):
    """ class products """

    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Name')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')


class ProductsCategories(TimeStamp):
    """ Class products categories """

    productID = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Products')
    categoriesID = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Categories')

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

class OrderItems(TimeStamp):
    """ Class orders items """

    orderID = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name='Order')
    productID = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Products')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    quantity = models.IntegerField(verbose_name='Quantity')