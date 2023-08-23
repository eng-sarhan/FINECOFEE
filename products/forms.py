from django import forms
from .models import Category, Product, Company


class MycategForm(forms.ModelForm):
    class Meta:
        model = Category
        # fields='__all__'

        fields = [
            'categ',
            'catParent',

        ]
        widgets = {
            'categ': forms.TextInput(attrs={'class': 'form-control'})

        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        # fields='__all__'

        fields = [
            'comp',
        ]
        widgets = {
            'comp': forms.TextInput(attrs={'class': 'form-control'})
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields='__all__'

        fields = [

            'name',
            'description'
            'price',
            'photo',
            'is_active',
            'publish_date',
            'categ',
            'comp',

        ]
        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'price'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.TextInput(attrs={'class': 'form-control'}),
            'publish_date': forms.TextInput(attrs={'class': 'form-control'}),
            'categ': forms.Select(attrs={'class': 'form-control'}),
            'comp': forms.Select(attrs={'class': 'form-control'}),
        }
