import tkinter as tk
from tkinter import ttk
import pandas as pd
from utils.ui_helpers import create_heading

class AddTransaction(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#eaf8e1")
        self.controller = controller

        tk.Label(
            self, text="Personal Finance Manager", bg="#f9f9f9",
            font=("Arial", 18, "bold"), fg="#2f4f4f"
        ).pack(pady=10)

        self.create_navbar(controller)

        self.create_form()

    def create_navbar(self, controller):
        navbar = tk.Frame(self, bg="#8fbc8f", height=50)
        navbar.pack(fill="x", side="top")

        tk.Button(navbar, text="Dashboard", command=lambda: controller.show_frame("Dashboard"), font=("Arial", 14)).pack(side="left", padx=20)
        tk.Button(navbar, text="Add Transaction", command=lambda: controller.show_frame("AddTransaction"), font=("Arial", 14)).pack(side="left", padx=20)
        tk.Button(navbar, text="Transaction History", command=lambda: controller.show_frame("TransactionHistory"), font=("Arial", 14)).pack(side="left", padx=20)
        tk.Button(navbar, text="Visual report", command=lambda: controller.show_frame("Charts"), font=("Arial", 14)).pack(side="left", padx=20)

    def create_form(self):
        form_frame = tk.Frame(self, bg="#f9f9f9")
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Date (YYYY-MM-DD):", bg="#f9f9f9", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.date_entry = tk.Entry(form_frame, font=("Arial", 14))
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Type:", bg="#f9f9f9", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.type_var = tk.StringVar(value="Select Type")
        self.type_dropdown = ttk.Combobox(form_frame, textvariable=self.type_var, values=["Income", "Expense"], font=("Arial", 14), state="readonly")
        self.type_dropdown.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Category:", bg="#f9f9f9", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.category_entry = tk.Entry(form_frame, font=("Arial", 14))
        self.category_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Amount:", bg="#f9f9f9", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.amount_entry = tk.Entry(form_frame, font=("Arial", 14))
        self.amount_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Description:", bg="#f9f9f9", font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.description_entry = tk.Entry(form_frame, font=("Arial", 14))
        self.description_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Button(
            self, text="Add Transaction", bg="#6b8e23", fg="white", font=("Arial", 14),
            command=self.save_transaction
        ).pack(pady=10)

    def save_transaction(self):
        date = self.date_entry.get()
        txn_type = self.type_var.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        description = self.description_entry.get()

        if not date or txn_type == "Select Type" or not category or not amount:
            tk.Label(self, text="Please fill all fields!", bg="#f9f9f9", fg="red", font=("Arial", 14)).pack(pady=5)
            return

        try:
            amount = float(amount)  
        except ValueError:
            tk.Label(self, text="Invalid amount entered!", bg="#f9f9f9", fg="red", font=("Arial", 14)).pack(pady=5)
            return

        try:
            new_transaction = pd.DataFrame({
                "Date": [date],
                "Type": [txn_type],
                "Category": [category],
                "Amount": [amount],
                "Description": [description]
            })

            csv_file = "C:/Users/vidhi/OneDrive/Desktop/Projects/PersonalFinanceManager/data/transactions.csv"

            try:
                existing_data = pd.read_csv(csv_file)
                updated_data = pd.concat([existing_data, new_transaction], ignore_index=True)
            except FileNotFoundError:
                updated_data = new_transaction

            updated_data['Date'] = pd.to_datetime(updated_data['Date'], format='%Y-%m-%d')

            updated_data = updated_data.sort_values(by='Date', ascending=False).reset_index(drop=True)

            updated_data.to_csv(csv_file, index=False)

            success_label = tk.Label(self, text="Transaction added successfully!", bg="#f9f9f9", fg="green", font=("Arial", 14))
            success_label.pack(pady=5)

            self.after(30000, success_label.destroy)  

            self.clear_form()
        except Exception as e:
            tk.Label(self, text=f"Error saving transaction: {e}", bg="#f9f9f9", fg="red", font=("Arial", 14)).pack(pady=5)

    def clear_form(self):
        self.date_entry.delete(0, tk.END)
        self.type_var.set("Select Type")
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
