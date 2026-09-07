"""
Expense Tracker
---------------
A simple command-line expense tracker that stores data in a CSV file
(expenses.csv, created automatically in the same folder as this script).

Features:
  1. Add an expense (date, category, amount, note)
  2. View all expenses
  3. View expenses filtered by category
  4. View monthly summary (total per month)
  5. View category-wise summary
  6. Delete an expense by its ID
  7. Exit

Run with:  python expense_tracker.py
"""

import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"
FIELDS = ["ID", "Date", "Category", "Amount", "Note"]


def init_file():
    """Create the CSV file with headers if it doesn't exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(FIELDS)


def read_expenses():
    """Return all expenses as a list of dicts."""
    with open(FILE_NAME, mode="r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_expenses(expenses):
    """Overwrite the CSV file with the given list of expense dicts."""
    with open(FILE_NAME, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(expenses)


def get_next_id(expenses):
    if not expenses:
        return 1
    return max(int(e["ID"]) for e in expenses) + 1


def add_expense():
    expenses = read_expenses()

    date_str = input("Date (YYYY-MM-DD) [leave blank for today]: ").strip()
    if date_str == "":
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Expense not added.")
            return

    category = input("Category (e.g., Food, Travel, Bills): ").strip() or "Uncategorized"

    try:
        amount = float(input("Amount: ").strip())
    except ValueError:
        print("Invalid amount. Expense not added.")
        return

    note = input("Note (optional): ").strip()

    new_expense = {
        "ID": str(get_next_id(expenses)),
        "Date": date_str,
        "Category": category,
        "Amount": f"{amount:.2f}",
        "Note": note,
    }

    expenses.append(new_expense)
    write_expenses(expenses)
    print(f"Expense added with ID {new_expense['ID']}.")


def view_all():
    expenses = read_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"\n{'ID':<5}{'Date':<12}{'Category':<15}{'Amount':<10}Note")
    print("-" * 60)
    total = 0.0
    for e in expenses:
        print(f"{e['ID']:<5}{e['Date']:<12}{e['Category']:<15}{e['Amount']:<10}{e['Note']}")
        total += float(e["Amount"])
    print("-" * 60)
    print(f"Total: {total:.2f}\n")


def view_by_category():
    expenses = read_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    category = input("Enter category to filter by: ").strip().lower()
    filtered = [e for e in expenses if e["Category"].lower() == category]

    if not filtered:
        print("No expenses found for that category.")
        return

    print(f"\n{'ID':<5}{'Date':<12}{'Category':<15}{'Amount':<10}Note")
    print("-" * 60)
    total = 0.0
    for e in filtered:
        print(f"{e['ID']:<5}{e['Date']:<12}{e['Category']:<15}{e['Amount']:<10}{e['Note']}")
        total += float(e["Amount"])
    print("-" * 60)
    print(f"Total for '{category}': {total:.2f}\n")


def monthly_summary():
    expenses = read_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    summary = {}
    for e in expenses:
        month = e["Date"][:7]  # YYYY-MM
        summary[month] = summary.get(month, 0.0) + float(e["Amount"])

    print(f"\n{'Month':<10}Total")
    print("-" * 25)
    for month in sorted(summary):
        print(f"{month:<10}{summary[month]:.2f}")
    print()


def category_summary():
    expenses = read_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    summary = {}
    for e in expenses:
        cat = e["Category"]
        summary[cat] = summary.get(cat, 0.0) + float(e["Amount"])

    print(f"\n{'Category':<15}Total")
    print("-" * 30)
    for cat in sorted(summary):
        print(f"{cat:<15}{summary[cat]:.2f}")
    print()


def delete_expense():
    expenses = read_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    exp_id = input("Enter ID of expense to delete: ").strip()
    new_expenses = [e for e in expenses if e["ID"] != exp_id]

    if len(new_expenses) == len(expenses):
        print("No expense found with that ID.")
        return

    write_expenses(new_expenses)
    print(f"Expense {exp_id} deleted.")


def main_menu():
    init_file()
    menu = """
==== EXPENSE TRACKER ====
1. Add expense
2. View all expenses
3. View expenses by category
4. Monthly summary
5. Category-wise summary
6. Delete an expense
7. Exit
==========================
"""
    actions = {
        "1": add_expense,
        "2": view_all,
        "3": view_by_category,
        "4": monthly_summary,
        "5": category_summary,
        "6": delete_expense,
    }

    while True:
        print(menu)
        choice = input("Choose an option (1-7): ").strip()
        if choice == "7":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
