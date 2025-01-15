from tabnanny import verbose
from tkinter.constants import CASCADE
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.db import models

# Create your models here.

class Category(models.Model):

    name = models.CharField('category', max_length=250, unique=True)
    is_archive = models.BooleanField(default=False)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


def validate_positiv_decimal(value):
    if value < 0:
        raise ValidationError(f"{value} can`t be lower than 0")

class Expense(models.Model):

    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positiv_decimal])
    desc = models.TextField(blank=True, null=True)
    time_update = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return f'category - {self.category}, amount - {self.amount} on {self.date}, updated - {self.time_update}'

    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'

class UserExpenses(models.Model):

    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.expense} - {self.user}'
