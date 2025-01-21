from django import forms
from .models import Expense, Category



class ExpensesForm(forms.ModelForm):

    class Meta:
        model = Expense
        fields = ['date', 'category', 'amount', 'desc', 'is_delete']
        widgets = {
                    'date': forms.DateInput(attrs={'type': 'date'}),  # HTML5-виджет выбора даты
                }


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'is_archive']


class UploadFile(forms.Form):
    csv_file = forms.FileField(label='Upalod file')