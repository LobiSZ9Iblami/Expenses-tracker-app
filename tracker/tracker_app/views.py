from http.client import responses
from imghdr import test_webp
from tokenize import Exponent

from django.contrib.admin import action
from django.db.models.expressions import result
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.template.context_processors import request
from django.views import View
from unicodedata import category

from .forms import ExpensesForm, CategoryForm, UploadFileCSV
from .models import Expense, Category, UserExpenses
from django.views.generic import CreateView
from django.apps import apps

import csv
import pandas as pd
import datetime

# Create your views here.

def index(request):
    return render(request, 'tracker_app/home.html')


def decorator(func):

    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(self, request,  *args, **kwargs)
        else:
            return redirect('users:login')
    return wrapper


class Expenses(View):

    # def get_filters(self, filter_category, filter_type, expenses_for_auth):
    #
    #     filters = {'id__in': expenses_for_auth}
    #
    #     if filter_category:
    #         try:
    #             filter_category = int(filter_category)
    #             filters['category'] = filter_category
    #         except ValueError:
    #             filter_category = None
    #
    #     if filter_type == 'active':
    #         filters['is_delete'] = False
    #     elif filter_type == 'deleted':
    #         filters['is_delete'] = True
    #
    #     return filters


    @decorator
    def get(self, request, pk=None):

        filter_type = request.GET.get('filter', 'active')
        filter_category = request.GET.get('filter_category', None)
        # filter_date = request.Get.get('filter_date', None)

        if filter_category:
            try:
                filter_category = int(filter_category)
            except ValueError:
                filter_category = None

        categories = Category.objects.all()
        list_for_auth = UserExpenses.objects.filter(user=request.user.id)
        expenses_for_auth = list_for_auth.values_list('expense', flat=True)
        today = datetime.date.today()

        if pk is None:
            if filter_category:
                exp_list = Expense.objects.filter(id__in=expenses_for_auth, category=filter_category)
            else:
                exp_list = Expense.objects.filter(id__in=expenses_for_auth)
            if filter_type == 'active':
                exp_list = exp_list.filter(is_delete=False)
            elif filter_type == 'deleted':
                exp_list = exp_list.filter(is_delete=True)
            # if filter_date:
            #     exp_list = Expense.objects.filter(id__in=expenses_for_auth, date=filter_date)
            # else:
            #     exp_list = Expense.objects.filter(id__in=expenses_for_auth)
            return render(request, 'tracker_app/expenses.html', {
                'exp_list': exp_list,
                'filter_type': filter_type,
                'filter_category': filter_category,
                'categories': categories,
                'today': today
            })

        else:
            exp = get_object_or_404(Expense, pk=pk)
            form = ExpensesForm(instance=exp)
            return render(request, 'tracker_app/expenses_edit.html', {'form': form, 'exp': exp, 'today': today})


    # def get_date(self, request):



    def post(self, request, pk=None):
        action = request.POST.get('action', 'create_expense')

        if action == 'edit_expense':
            return self.edit_expense(request, pk)
        elif action == 'delete_expense':
            return self.delete_expense(request, pk)
        elif action == 'archive_expense':
            return self.archive_expense(request, pk)
        else:
            return self.create_expense(request)

    def create_expense(self, request):
        form = ExpensesForm(request.POST)
        if form.is_valid():
            expense = form.save()
            UserExpenses.objects.create(user=request.user, expense=expense)
            return redirect('tracker:expense')
        else:
            return render(request, 'tracker_app/create_expense.html', {'form': form})


    def edit_expense(self, request, pk):

        expense = get_object_or_404(Expense, pk=pk)
        form = ExpensesForm(request.POST, instance=expense)

        if form.is_valid():
            form.save()
            return redirect('tracker:expense')
        else:
            return render(request, 'tracker_app/expenses_edit.html', {'expense': expense, 'form': form})

    def delete_expense(self, request, pk):

        expense = get_object_or_404(Expense, pk=pk)
        expense.delete()
        return redirect('tracker:expense')

    def archive_expense(self, request, pk):

        expense = get_object_or_404(Expense, pk=pk)
        expense.is_delete = True
        expense.save()
        return redirect('tracker:expense')



class CategoryView(View):

    @decorator
    def get(self, request, pk=None):
        """
        Если pk is None
        Вызвращаем весь список експенсов

        Если pk указан
        Вызвращаем только тот експенс, айди которого передали
        """
        if pk is None:
            # category_list = Category.objects.all()
            text_query = request.GET.get('search', '')
            category_list = self.get_filter_input(request, text_query)
            return render(request, 'tracker_app/category.html', {'category_list': category_list, 'text_query': text_query})

        else:
            categ = get_object_or_404(Category, pk=pk)
            form = CategoryForm( instance=categ)
            return render(request, 'tracker_app/category_edit.html', {'categ': categ, 'form': form})

    def get_filter_input(self, request, text_query):

        if text_query.strip():
            return Category.objects.filter(name__icontains=text_query.strip())
        return Category.objects.all()


    def post(self, request, pk=None):
        action = request.POST.get('action', 'create_category')

        if action == 'edit_category':
            return self.edit_category(request, pk)
        elif action == 'delete_category':
            return self.delete_category(request, pk)
        elif action == 'archive_category':
            return self.archive_category(request, pk)
        else:
            return self.create_category(request)


    def create_category(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracker:category')
        else:
            return render(request, 'tracker_app/category.html', {'form': form})


    def edit_category(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('tracker:category')
        else:
            return render(request, 'tracker_app/category_edit.html', {'form': form, 'category': category})

    def delete_category(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect('tracker:category')

    def archive_category(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.is_archive = True
        category.save()
        return redirect('tracker:category')




def dictionary(request):

    all_models = apps.get_models(include_auto_created=True, include_swapped=True)
    data = []

    for p in all_models:
        if 'tracker_app' in p._meta.app_label and 'user' not in p.__name__.lower():
            # data.append(f"tracker:{p.__name__.lower()}")
            data.append({
                'url': f"tracker:{p.__name__.lower()}",
                'name': p.__name__
            })

    return render(request, 'tracker_app/dict.html', {'data': data})


class FileExportImport(View):

    def templatecsv(self, request):

        fields = [
            ['date', 'category', 'amount', 'desc'],
        ]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="expenses_template.csv"'

        writer = csv.writer(response)
        writer.writerows(fields)

        return response

    def readcsv(self, request):

        if request.method == 'POST':
            form = UploadFileCSV(request.POST, request.FILES)
            file = []
            if form.is_valid():
                raw_data = form.cleaned_data['csv_file']
                decoded_file = raw_data.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                for fields in reader:
                    fields['date'] = convert_date(fields['date'])
                    fields['amount'] = fields['amount'].replace(',', '.')
                    category, category_created = Category.objects.get_or_create(name__iexact=fields['category'].strip())
                    expenses, expenses_created = Expense.objects.get_or_create(date=fields['date'],
                                                                      category=category,
                                                                      amount=fields['amount'],
                                                                      desc=fields['desc'])
                    expenses_user, expenses_user_created = UserExpenses.objects.get_or_create(user=request.user, expense=expenses)
                    file.append({'date': expenses.date, 'category': expenses.category, 'amount': expenses.amount, 'desc': expenses.desc, 'created': expenses_created})
                return HttpResponse(file)
            else:
                form = UploadFileCSV()
            return render(request, 'tracker_app/expenses.html', {'csv_form': form})


def convert_date(date_str):
    if datetime.datetime.strptime(date_str,"%d.%m.%Y"):
        from_str_to_date = datetime.datetime.strptime(date_str,"%d.%m.%Y").strftime("%Y-%m-%d")
        return from_str_to_date
    elif datetime.datetime.strptime(date_str, "%d-%m-%Y"):
        from_str_to_date = datetime.datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
        return from_str_to_date

