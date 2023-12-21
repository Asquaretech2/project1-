from django import forms
from .models import *
from django.forms import Textarea
from captcha.fields import CaptchaField, CaptchaTextInput


class ContactForm(forms.ModelForm):
    captcha = CaptchaField(
        widget=CaptchaTextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Contact
        fields = ['Name', 'Email', 'Subject', 'Message']

        widgets = {
            'Message': forms.Textarea(attrs={'rows': 4, 'cols': 100}),
        }