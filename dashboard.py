import tkinter as tk
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.ui_helpers import create_heading

class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#eaf8e1")
        self.controller = controller

        tk.Label(self, text="Personal Finance Manager", bg="#eaf8e1", 
                 font=("Arial", 22, "bold"), fg="#2f4f4f").pack(pady=10)

        self.create_navbar(controller)

        tk.Label(self, text="Dashboard", bg="#eaf8e1", font=("Arial", 20, "bold"), fg="#64b969").pack(pady=10)

        self.refresh_pie_chart()

        self.show_savings()

    def create_navbar(self, controller):
        navbar = tk.Frame(self, bg="#8fbc8f", height=100)
        navbar.pack(fill="x", side="top")

        tk.Button(navbar, text="Dashboard", command=lambda: controller.show_frame("Dashboard"), font=("Arial", 14)).pack(side="left", padx=20, pady=5)
        tk.Button(navbar, text="Add Transaction", command=lambda: controller.show_frame("AddTransaction"), font=("Arial", 14)).pack(side="left", padx=20, pady=5)
        tk.Button(navbar, text="Transaction History", command=lambda: controller.show_frame("TransactionHistory"), font=("Arial", 14)).pack(side="left", padx=20, pady=5)
        tk.Button(navbar, text="Visual report", command=lambda: controller.show_frame("Charts"), font=("Arial", 14)).pack(side="left", padx=20, pady=5)
        
    def refresh_pie_chart(self):
        try:
            data = pd.read_csv("../data/transactions.csv")
            expense_data = data[data["Type"] == "Expense"]
            category_totals = expense_data.groupby("Category")["Amount"].sum()

            figure = Figure(figsize=(6, 4), dpi=120)
            subplot = figure.add_subplot(111)
            subplot.pie(
                category_totals,
                labels=category_totals.index,
                autopct="%1.1f%%",
                startangle=140,
            )
            subplot.set_title("Expenses by Category")

            canvas = FigureCanvasTkAgg(figure, self)
            canvas.get_tk_widget().pack(pady=10)
        except Exception as e:
            tk.Label(self, text="No Data Available for Pie Chart", bg="#eaf8e1", font=("Arial", 14)).pack(pady=10)

    def show_savings(self):
        try:
            data = pd.read_csv("../data/transactions.csv")
            total_income = data[data["Type"] == "Income"]["Amount"].sum()
            total_expense = data[data["Type"] == "Expense"]["Amount"].sum()
            savings = total_income - total_expense

            savings_text = f"Savings: ₹{savings:.2f}"
            tk.Label(self, text=savings_text, bg="#eaf8e1", font=("Arial", 16), fg="#2f4f4f").pack(pady=10)
        except Exception as e:
            tk.Label(self, text="Error Calculating Savings", bg="#eaf8e1", font=("Arial", 14)).pack(pady=10)
