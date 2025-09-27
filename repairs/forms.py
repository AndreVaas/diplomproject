from django import forms
from .models import Apartment, Room, Work, Material


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['name', 'address', 'total_area', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'total_area': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название',
            'address': 'Адрес',
            'total_area': 'Общая площадь (м²)',
            'image': 'Фото (план проекта)',
        }


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['name', 'description', 'cost', 'date', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'cost': 'Стоимость (руб.)',
            'date': 'Дата',
            'image': 'Фото выполненной работы',
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'area']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название',
            'area': 'Площадь (кв.м)',
        }


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'quantity', 'unit', 'cost']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название',
            'quantity': 'Количество',
            'unit': 'Единица измерения',
            'cost': 'Стоимость за единицу (руб.)',
        }
