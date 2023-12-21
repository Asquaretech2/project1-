from django.contrib.auth.models import AbstractUser
from django.db import models
from cinystoreapp.models import User
from phonenumber_field.modelfields import PhoneNumberField


class MarketingRegister(models.Model):
    marketing = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    username = models.CharField(max_length=45)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField() 
    email = models.CharField(max_length=100)
    last_login = models.DateTimeField(verbose_name='last login', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Marketing_register'
