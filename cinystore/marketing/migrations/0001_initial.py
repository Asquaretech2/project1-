# Generated by Django 4.2.7 on 2023-12-28 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import marketing.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cinystoreapp', '0003_alter_userinfo_profilephoto'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketingRegister',
            fields=[
                ('marketing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('username', models.CharField(max_length=45)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('email', models.CharField(max_length=100)),
                ('profile_image', models.ImageField(default='marketing/blank_profile.webp', null=True, upload_to=marketing.models.rename_marketing)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'Marketing_register',
            },
        ),
    ]
