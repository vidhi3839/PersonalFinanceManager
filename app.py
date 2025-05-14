import tkinter as tk
from add_transaction import AddTransaction
from dashboard import Dashboard
from transaction_history import TransactionHistory
from charts import Charts 

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance Manager")
        self.geometry("900x600")
        self.frames = {}

        for F in (Dashboard, AddTransaction, TransactionHistory, Charts):  
            frame = F(parent=self, controller=self)
            self.frames[F.__name__] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("Dashboard")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
