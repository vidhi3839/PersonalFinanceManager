# Personal Finance Manager
A desktop-based application built with Tkinter for managing personal finances. Users can add income and expenses, visualize spending habits, view transaction history, and generate PDF reports — all in one place.

## Features
- Add Transactions: Record income or expenses with date, category, and description.
- Dashboard: View overall savings and category-wise expense breakdown using pie charts.
- Transaction History: Filter, edit, delete, and download transactions in a printable PDF format.
- Visual Reports: Analyze monthly spending patterns with a calendar heatmap view.
- Persistent Storage: All transactions are stored in a CSV file and loaded across sessions.

## GUI Overview
|Screen	|Description|
|-------|-----------|
|Dashboard	|Shows current savings and a pie chart of expenses.|
|Add Transaction	|Form to input new income or expense.|
|Transaction History	|Filterable list with options to edit, delete, or export as PDF.|
|Visual Report	|Heatmap view of monthly expenses with year navigation.|

## Tech Stack
- Frontend & Backend: Python Tkinter
- Data Handling: pandas
- Visualization: matplotlib, seaborn
- PDF Generation: FPDF
- File Format: CSV for persistent data storage

## Getting Started
1. Clone the Repository
2. Install Dependencies: pip install pandas matplotlib seaborn fpdf
3. Run the App: python app.py
