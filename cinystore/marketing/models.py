from django.contrib.auth.models import AbstractUser
from django.db import models
from cinystoreapp.models import User
from phonenumber_field.modelfields import PhoneNumberField
from uuid import uuid4
import os
from datetime import datetime
from django.utils import timezone




def rename_marketing(instance, filename):
    upload_to = 'marketing/'
    ext = filename.split('.')[-1]
    # username = user.username
    if instance.profile_image:
        filename = '{}_{}.{}'.format(instance.username,datetime.now(), ext)
    else:
        filename ='{}_{}.{}'.format(uuid4.hex, datetime.now(), ext)
    return os.path.join(upload_to, filename)



class MarketingRegister(models.Model):
    marketing = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    username = models.CharField(max_length=45)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField() 
    email = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to=rename_marketing, default='marketing/blank_profile.webp', null=True)
    last_login = models.DateTimeField(verbose_name='last login', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Marketing_register'

