import json
import os

FILE_NAME = "expenses.json"

# Load expenses from file
def load_expenses():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

# Save expenses to file
def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)

# Add expense
def add_expense():
    name = input("Enter expense name: ")
    amount = float(input("Enter amount: "))

    expense = {"name": name, "amount": amount}

    expenses = load_expenses()
    expenses.append(expense)
    save_expenses(expenses)

    print("Expense added successfully!\n")

# View expenses
def view_expenses():
    expenses = load_expenses()

    if not expenses:
        print("No expenses found.\n")
        return

    print("\n--- Expense List ---")
    for i, exp in enumerate(expenses, 1):
        print(f"{i}. {exp['name']} - ₹{exp['amount']}")

    print()

# Total expense
def total_expense():
    expenses = load_expenses()
    total = sum(exp["amount"] for exp in expenses)
    print(f"\nTotal Expense: ₹{total}\n")

# Main menu
def main():
    while True:
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Expense")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            total_expense()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice\n")

if __name__ == "__main__":
    main()