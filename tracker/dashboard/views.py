from django.shortcuts import render
from tracker_app.models import Expense, UserExpenses
from tracker_app.forms import ExpensesForm

import plotly.express as px
from django.db.models import F
import pandas as pd
from dash import html, dcc


# Create your views here.

def example_dashboard(request):

    category_filter = ExpensesForm()
    user_expense_data = UserExpenses.objects.filter(user=request.user)
    expense_data = Expense.objects.filter(pk__in=user_expense_data.values_list('expense', flat=True)).annotate(category_name=F('category__name')).values("date", "amount", "category_name")
    # df = [
    #     {
    #         "date": [expense.date for expense in expense_data],
    #         "amount": [expense.amount for expense in expense_data],
    #         "category": [expense.category for expense in expense_data]
    #     }
    # ]
    #
    # df = pd.DataFrame({
    #     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    #     "Amount": [4, 1, 2, 2, 4, 5],
    #     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    # })

    if category_filter:
        expense_data = expense_data.filter(category__in=category_filter)

    fig = px.bar(
        # df,
        expense_data,
        x = "date",
        y = "amount",
        color = "category_name",
        # x="Fruit", y="Amount", color="City",
        barmode = "group"
    )

    bar_dash = fig.to_html(
        # html.Br(),
        # html.Label('Multi-Select Dropdown'),
        # dcc.Dropdown(expense_data[2], multi=True)
    )

    context = {'bar_dash': bar_dash, 'category_filter_form': category_filter}

    return render(request, 'dashboard/expenses_example.html', context)