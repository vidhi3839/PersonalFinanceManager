import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from fpdf import FPDF
import os


class TransactionHistory(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#eaf8e1")
        self.controller = controller

        self.data_file = "../data/transactions.csv"

        tk.Label(
            self, text="Personal Finance Manager", bg="#f9f9f9",
            font=("Arial", 18, "bold"), fg="#2f4f4f"
        ).pack(pady=10)

        self.create_navbar(controller)

        tk.Label(
            self, text="Transaction History", bg="#f9f9f9",
            font=("Arial", 20, "bold"), fg="#6b8e23"
        ).pack(pady=10)

        filter_frame = tk.Frame(self, bg="#f9f9f9")
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Search:", bg="#f9f9f9", font=("Arial", 14)).pack(side="left", padx=5)
        self.search_entry = tk.Entry(filter_frame)
        self.search_entry.pack(side="left", padx=5)

        tk.Button(
            filter_frame, text="Apply", command=self.apply_filter, bg="#6b8e23", fg="white", font=("Arial", 14)
        ).pack(side="left", padx=5)

        self.transaction_table = ttk.Treeview(
            self,
            columns=("Amount", "Date", "Category", "Type", "Description"),
            show="headings"
        )
        self.transaction_table.heading("Amount", text="Amount")
        self.transaction_table.heading("Date", text="Date")
        self.transaction_table.heading("Category", text="Category")
        self.transaction_table.heading("Type", text="Type")
        self.transaction_table.heading("Description", text="Description")
        self.transaction_table.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_transaction_data()

        # Buttons
        button_frame = tk.Frame(self, bg="#f9f9f9")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Edit", command=self.edit_transaction, bg="#6b8e23", fg="white", font=("Arial", 14)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete", command=self.delete_transaction, bg="#6b8e23", fg="white", font=("Arial", 14)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Download PDF", command=self.download_pdf, bg="#6b8e23", fg="white", font=("Arial", 14)).pack(side="left", padx=5)
        
    def create_navbar(self, controller):
        navbar = tk.Frame(self, bg="#8fbc8f", height=50)
        navbar.pack(fill="x", side="top")

        tk.Button(navbar, text="Dashboard", command=lambda: controller.show_frame("Dashboard"), font=("Arial", 14)).pack(side="left", padx=20)
        tk.Button(navbar, text="Add Transaction", command=lambda: controller.show_frame("AddTransaction"), font=("Arial", 14)).pack(side="left", padx=20)
        tk.Button(navbar, text="Transaction History", command=lambda: controller.show_frame("TransactionHistory"), font=("Arial", 14)).pack(side="left", padx=20)
        tk.Button(navbar, text="Visual report", command=lambda: controller.show_frame("Charts"), font=("Arial", 14)).pack(side="left", padx=20)

    def load_transaction_data(self):
        try:
            # Read data from CSV
            self.data = pd.read_csv(self.data_file)
            self.update_transaction_table(self.data)
        except FileNotFoundError:
            tk.Label(
                self, text="No transaction data available!", bg="#f9f9f9",
                fg="red", font=("Arial", 14)
            ).pack(pady=10)

    def update_transaction_table(self, data):
        for row in self.transaction_table.get_children():
            self.transaction_table.delete(row)

        for _, row in data.iterrows():
            self.transaction_table.insert("", "end", values=tuple(row))

    def apply_filter(self):
        query = self.search_entry.get().lower()
        filtered_data = self.data[
            self.data.apply(
                lambda row: row.astype(str).str.contains(query, case=False).any(),
                axis=1
            )
        ]
        self.update_transaction_table(filtered_data)

    def edit_transaction(self):
        selected_item = self.transaction_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No transaction selected!")
            return

        item = self.transaction_table.item(selected_item[0])
        values = item['values']

        selected_index = int(selected_item[0][1:], 16) - 1  

        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Transaction")
        edit_window.geometry("400x400")

        tk.Label(edit_window, text="Amount").pack(pady=5)
        amount_entry = tk.Entry(edit_window, width=50)
        amount_entry.insert(0, values[0])
        amount_entry.pack()

        tk.Label(edit_window, text="Date").pack(pady=5)
        date_entry = tk.Entry(edit_window, width=50)
        date_entry.insert(0, values[1])
        date_entry.pack()

        tk.Label(edit_window, text="Category").pack(pady=5)
        category_entry = tk.Entry(edit_window, width=50)
        category_entry.insert(0, values[2])
        category_entry.pack()

        tk.Label(edit_window, text="Type").pack(pady=5)
        type_entry = tk.Entry(edit_window, width=50)
        type_entry.insert(0, values[3])
        type_entry.pack()

        tk.Label(edit_window, text="Description").pack(pady=5)
        desc_entry = tk.Entry(edit_window, width=50)
        desc_entry.insert(0, values[4])
        desc_entry.pack()

        def save_changes():
            self.data.iloc[selected_index] = [
                amount_entry.get(),
                date_entry.get(),
                category_entry.get(),
                type_entry.get(),
                desc_entry.get()
            ]
            self.data.to_csv(self.data_file, index=False)
            self.load_transaction_data()
            edit_window.destroy()

        tk.Button(edit_window, text="Save", command=save_changes, bg="#6b8e23", fg="white").pack(pady=10)


    def delete_transaction(self):
        selected_item = self.transaction_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No transaction selected!")
            return

        idx = self.transaction_table.index(selected_item[0])
        self.data = self.data.drop(index=idx)
        self.data.to_csv(self.data_file, index=False)
        self.load_transaction_data()
        messagebox.showinfo("Success", "Transaction deleted successfully!")

    def download_pdf(self):
        try:
            data = pd.read_csv(self.data_file).fillna("")
            data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
            data = data.sort_values(by="Date").fillna("")

            # Generate PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.set_font("Arial", style="B", size=16)
            pdf.cell(200, 10, "Transaction History", ln=True, align="C")
            pdf.ln(10)

            pdf.set_font("Arial", style="B", size=14)
            pdf.cell(40, 10, "Amount", 1)
            pdf.cell(40, 10, "Date", 1)
            pdf.cell(40, 10, "Category", 1)
            pdf.cell(40, 10, "Type", 1)
            pdf.cell(60, 10, "Description", 1)
            pdf.ln()

            
            pdf.set_font("Arial", size=14)
            for _, row in data.iterrows():
                pdf.cell(40, 10, str(row['Amount']), 1)
                pdf.cell(40, 10, str(row["Date"].date()) if pd.notnull(row["Date"]) else "", 1)
                pdf.cell(40, 10, str(row["Category"]), 1)
                pdf.cell(40, 10, str(row["Type"]), 1)
                pdf.cell(60, 10, str(row["Description"]), 1)
                pdf.ln()

            # Save PDF
            pdf_dir = "../pdf_files/"
            os.makedirs(pdf_dir, exist_ok=True)
            pdf_file = os.path.join(pdf_dir, "Transaction_History.pdf")
            pdf.output(pdf_file)

            messagebox.showinfo("Success", f"PDF saved successfully at {pdf_file}")

        except Exception as e:
            messagebox.showerror("Error", f"Error generating PDF: {e}")
