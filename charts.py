import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

class Charts(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f9f9f9")
        self.controller = controller
        self.data_file = "../data/transactions.csv"
        
        self.selected_year = None  # Variable to track the selected year

        # Heading
        tk.Label(
            self, text="Spending Heatmap", bg="#f9f9f9",
            font=("Arial", 18, "bold"), fg="#2f4f4f"
        ).pack(pady=10)

        # Navigation Bar
        self.create_navbar(controller)

        # Year navigation buttons
        button_frame = tk.Frame(self, bg="#f9f9f9")
        button_frame.pack(pady=20)

        # Left arrow to go to previous year
        self.left_arrow = tk.Button(button_frame, text="<", command=self.show_previous_year, bg="#6b8e23", fg="white")
        self.left_arrow.pack(side="left", padx=10)

        # Right arrow to go to next year
        self.right_arrow = tk.Button(button_frame, text=">", command=self.show_next_year, bg="#6b8e23", fg="white")
        self.right_arrow.pack(side="left", padx=10)

        # Chart Display Area
        self.chart_frame = tk.Frame(self, bg="#f9f9f9")
        self.chart_frame.pack(fill="both", expand=True)

        # Load data and initialize the first year
        self.df = self.load_data()
        if self.df is not None:
            self.initialize_year()

    def create_navbar(self, controller):
        navbar = tk.Frame(self, bg="#8fbc8f", height=50)
        navbar.pack(fill="x", side="top")

        tk.Button(navbar, text="Dashboard", command=lambda: controller.show_frame("Dashboard"), font=("Arial",14)).pack(side="left", padx=20)
        tk.Button(navbar, text="Add Transaction", command=lambda: controller.show_frame("AddTransaction"), font=("Arial", 14)).pack(side="left", padx=20)
        tk.Button(navbar, text="Transaction History", command=lambda: controller.show_frame("TransactionHistory"), font=("Arial", 14)).pack(side="left", padx=20)
        tk.Button(navbar, text="Visual report", command=lambda: controller.show_frame("Charts"), font=("Arial", 14)).pack(side="left", padx=20)

    def load_data(self):
        try:
            df = pd.read_csv(self.data_file)
            df['Date'] = pd.to_datetime(df['Date'])
            df['Month'] = df['Date'].dt.strftime('%b')  # Show month as Jan, Feb, etc.
            df['Year'] = df['Date'].dt.year
            df['Day'] = df['Date'].dt.day
            return df
        except FileNotFoundError:
            tk.messagebox.showerror("Error", "Transaction data not found!")
            return None

    def clear_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

    def initialize_year(self):
        # Get the available years from the data
        years = self.df['Year'].unique()
        self.selected_year = years[-1]  
        self.show_heatmap()  

    def show_previous_year(self):
        # Show the previous year when left arrow is clicked
        years = sorted(self.df['Year'].unique())
        current_index = years.index(self.selected_year)
        if current_index > 0:
            self.selected_year = years[current_index - 1]
            self.show_heatmap()

    def show_next_year(self):
        # Show the next year when right arrow is clicked
        years = sorted(self.df['Year'].unique())
        current_index = years.index(self.selected_year)
        if current_index < len(years) - 1:
            self.selected_year = years[current_index + 1]
            self.show_heatmap()

    def show_heatmap(self):
        self.clear_chart()

        if self.df is None or self.selected_year is None:
            return

    # Filter data for the selected year
        year_data = self.df[self.df['Year'] == self.selected_year]

   
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        year_data['Month'] = pd.Categorical(year_data['Month'], categories=month_order, ordered=True)

        heatmap_data = year_data.pivot_table(index='Day', columns='Month', values='Amount', aggfunc='sum')
        heatmap_data.fillna(0, inplace=True)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap='YlGnBu', cbar_kws={'label': 'Spending Amount'}, ax=ax)
        ax.set_title(f"Spending Heatmap for {self.selected_year}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Day of Month')

        ax.set_xticklabels(heatmap_data.columns, rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()
