# personal-finance-manager
Desktop personal finance manager built with Python, Tkinter and Matplotlib.

## About

The application allows users to:

* add income and expenses;
* select transaction categories;
* manage multiple users;
* view transaction history;
* calculate income, expenses, and balance;
* analyze expenses by category;
* display financial statistics;
* visualize expenses using a pie chart.
This project was developed as a university project during the third year of university.

## Object-oriented Structure

The application is organized into several classes:

* Category - manages income and expense categories. Income categories includes salary, gifts, investments, other. Expense categories includes food, transport, entertainment, housing, health, other.
* Expense - represents an income or expense transaction. Each transaction stores date, amount, description, category, transaction type.
* RecurringExpense - extends the Expense class and represents recurring expenses. It additionally stores the frequency of the expense.
* User - represents an application user and stores their transaction history.
* FinanceApp - controls the graphical interface and connects the user interface with the financial data.

## Key Variables

* income_categories - list of income categories;
* expense_categories - list of expense categories;
* transactions - list of user transactions;
* date - transaction date and time;
* amount - transaction amount;
* description - transaction description;
* category - transaction category;
* transaction_type - income or expense;
* frequency - recurring expense frequency;
* users - collection of application users;
* current_user - currently selected user;
* category_manager - category management object;
* user_var - selected user variable;
* type_var - selected transaction type;
* category_var - selected category;
* amount_entry - amount input field;
* desc_entry - description input field;
* history_tree - transaction history table;
* stats_text - financial statistics text area;
* expense_categories - expense totals grouped by category;
* stats - calculated financial statistics;
* categories - chart category names;
* amounts - expense amounts used for the chart.

## How to Run

1. Clone the repository

```bash
git clone https://github.com/dolzhkris/personal-finance-manager.git
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

The graphical application window will open. The user can then select or create a user, add financial transactions, view the transaction history, and analyze financial statistics.


GitHub: [@dolzhkris](https://github.com/dolzhkris)
