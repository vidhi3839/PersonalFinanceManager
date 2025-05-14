import tkinter as tk

def create_heading(parent, text, row, color, pady=0):
    label = tk.Label(parent, text=text, bg=parent["bg"], fg=color, font=("Arial", 18, "bold"))
    label.grid(row=row, column=0, columnspan=3, pady=pady, sticky="w")
