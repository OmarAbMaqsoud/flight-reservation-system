import tkinter as tk
from tkinter import ttk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        content_frame = ttk.Frame(self)
        content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        label = ttk.Label(
            content_frame, 
            text="Flight Reservation System", 
            font=("Arial", 18, "bold")
        )
        label.pack(pady=(20, 40))
        
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack()
        
        book_btn = ttk.Button(
            btn_frame, 
            text="Book Flight", 
            command=lambda: controller.show_frame("BookingPage"),
            width=20
        )
        book_btn.pack(pady=10, ipady=10, fill=tk.X)
        
        view_btn = ttk.Button(
            btn_frame, 
            text="View Reservations", 
            command=lambda: controller.show_frame("ReservationsPage"),
            width=20
        )
        view_btn.pack(pady=10, ipady=10, fill=tk.X)