from django.contrib.auth.models import AbstractUser
from django.db import models
from cinystoreapp.models import User


class CorporateRegister(models.Model):
    producer = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    username = models.CharField(max_length=45)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    production_house = models.CharField(max_length=100)
    website = models.CharField(max_length=50)
    country_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    company_brief = models.CharField(max_length=2000)
    last_login = models.DateTimeField(verbose_name='last login', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'CorporateRegister'


class IndividualRegister(models.Model):
    producer = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    username = models.CharField(max_length=45)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    production_house = models.CharField(max_length=100)
    website = models.CharField(max_length=50)
    country_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    company_brief = models.CharField(max_length=2000)
    last_login = models.DateTimeField(verbose_name='last login', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'IndividualRegister'

class OttRegister(models.Model):
    producer = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    username = models.CharField(max_length=45)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    production_house = models.CharField(max_length=100)
    website = models.CharField(max_length=50)
    country_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    company_brief = models.CharField(max_length=2000)
    last_login = models.DateTimeField(verbose_name='last login', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'OttRegister'


class AgencyRegister(models.Model):
    producer = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    username = models.CharField(max_length=45)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    production_house = models.CharField(max_length=100)
    website = models.CharField(max_length=50)
    country_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    company_brief = models.CharField(max_length=2000)
    last_login = models.DateTimeField(verbose_name='last login', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'AgencyRegister'

