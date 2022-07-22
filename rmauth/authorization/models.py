from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .managers import CustomUserManager
from .token_generators import generate_jwt


# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Адрес электронной почты', unique=True)
    is_staff = models.BooleanField(default=False)
    refresh_token = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def access_token(self):
        return generate_jwt(self.pk)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    '''Nothing, Renter, Owner, Developer'''
    role = models.CharField(max_length=30, default='Nothing')
    avatar = models.ImageField(upload_to='images/', blank=True, null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Requisites(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    inn = models.CharField(max_length=13)
    payment = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=150)
    bik = models.CharField(max_length=11)
    city = models.CharField(max_length=20)
    cor_payment = models.CharField(max_length=22)
