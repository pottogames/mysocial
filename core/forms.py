# forms.py

from django import forms
from .models import Product
from .models import Category
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'photo', 'description']


class PayPalForm(forms.Form):
    user_email = forms.EmailField(label='Your PayPal Email')



