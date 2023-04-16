from django.db import models
from validate_email import validate_email
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)



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

    class Meta:
        ordering = ['id']

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
   
