from django.shortcuts import render
from tracker_app.models import Expense, UserExpenses
import plotly.express as px
from django.db.models import F
import pandas as pd


# Create your views here.

def example_dashboard(request):

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

    fig = px.bar(
        # df,
        expense_data,
        x = "date",
        y = "amount",
        color = "category_name",
        # x="Fruit", y="Amount", color="City",
        barmode = "group"
    )

    bar_dash = fig.to_html()

    context = {'bar_dash': bar_dash}

    return render(request, 'dashboard/expenses_example.html', context)