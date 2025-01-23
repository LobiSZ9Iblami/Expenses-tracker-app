# Expenses-tracker-app

Tracker Expenses is a web application designed to help users manage and analyze their expenses effectively. This project provides functionality to track daily expenses, categorize them, and generate visual insights via dashboards.

## Features

User Authentication: Secure login and registration system.

1. Expense Management:
   1. Add, edit, delete expenses.
   1. Categorize expenses.
2. Dashboards:
   1. View total, average, and recent expenses. 
   2. Visualize expenses by category and date.
3. Import/Export:
   1. Upload expenses from Excel or CSV files.
   2. Export CSV template.


## Installation

1. Clone the repository:
```
git clone https://github.com/your-username/tracker-expenses.git
cd tracker-expenses
```
2. Create and activate a virtual environment:
```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```
Apply migrations:
```
python manage.py migrate
```
Run the development server:
```
python manage.py runserver
```
Open the application in your browser:

http://127.0.0.1:8000


## Usage

1. Register a new account or log in with an existing account.
2. Add expenses manually or upload a CSV/Excel file.
3. Navigate to the dashboard to view insights.

## Contributing

1. Fork the repository.
2. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```
Commit your changes:
```bash
git commit -m "Add your message here"
```
Push to the branch:
```bash
git push origin feature/your-feature-name
```