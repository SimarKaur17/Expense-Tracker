import json
import os
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner

# File path (mobile safe)
FILE_NAME = "/storage/emulated/0/Download/expenses.json"


# Load expenses
def load_expenses():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except:
            return []
    return []


# Save expenses
def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


class ExpenseApp(App):
    def build(self):
        self.title = "Expense Tracker"

        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Title
        title = Label(text="💰 Expense Tracker", font_size=24, size_hint_y=None, height=50)
        main_layout.add_widget(title)

        # Inputs
        self.name_input = TextInput(hint_text="Expense Name", size_hint_y=None, height=50)
        main_layout.add_widget(self.name_input)

        self.amount_input = TextInput(hint_text="Amount", input_filter="float", size_hint_y=None, height=50)
        main_layout.add_widget(self.amount_input)

        self.category = Spinner(
            text="Select Category",
            values=("Food", "Travel", "Shopping", "Bills", "Other"),
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(self.category)

        # Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)

        add_btn = Button(text="Add")
        add_btn.bind(on_press=self.add_expense)

        view_btn = Button(text="View")
        view_btn.bind(on_press=self.view_expenses)

        total_btn = Button(text="Total")
        total_btn.bind(on_press=self.total_expense)

        btn_layout.add_widget(add_btn)
        btn_layout.add_widget(view_btn)
        btn_layout.add_widget(total_btn)

        main_layout.add_widget(btn_layout)

        # Output (FIXED)
        self.output = Label(
            size_hint_y=None,
            text="",
            halign="left",
            valign="top",
            text_size=(350, None)  # ⭐ important fix
        )

        self.output.bind(texture_size=self.update_height)

        scroll = ScrollView()
        scroll.add_widget(self.output)

        main_layout.add_widget(scroll)

        return main_layout

    def update_height(self, instance, value):
        instance.height = instance.texture_size[1]

    # Add Expense
    def add_expense(self, instance):
        name = self.name_input.text.strip()
        amount = self.amount_input.text.strip()
        category = self.category.text

        if not name or not amount or category == "Select Category":
            self.output.text = "❌ Fill all fields properly!"
            return

        try:
            amount = float(amount)
        except:
            self.output.text = "❌ Enter valid amount!"
            return

        expense = {
            "name": name,
            "amount": amount,
            "category": category,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M")
        }

        expenses = load_expenses()
        expenses.append(expense)
        save_expenses(expenses)

        self.output.text = "✅ Expense Added!"

        # Clear inputs
        self.name_input.text = ""
        self.amount_input.text = ""
        self.category.text = "Select Category"

    # View Expenses (FIXED SAFE VERSION)
    def view_expenses(self, instance):
        expenses = load_expenses()

        if not expenses:
            self.output.text = "⚠️ No expenses found!"
            return

        text = "📋 Expense List:\n\n"
        for i, exp in enumerate(expenses, 1):
            text += (
                f"{i}. {exp.get('name','')} - ₹{exp.get('amount','')} "
                f"({exp.get('category','')})\n📅 {exp.get('date','')}\n\n"
            )

        self.output.text = text

    # Total Expense
    def total_expense(self, instance):
        expenses = load_expenses()
        total = sum(exp.get("amount", 0) for exp in expenses)

        self.output.text = f"💰 Total Expense: ₹{total}"


if __name__ == "__main__":
    ExpenseApp().run()
