import tkinter as tk
from tkinter import ttk, messagebox

class BookingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        fields = [
            ("Name", "name"),
            ("Flight Number", "flight_number"),
            ("Departure", "departure"),
            ("Destination", "destination"),
            ("Date (YYYY-MM-DD)", "date"),
            ("Seat Number", "seat_number")
        ]
        
        self.entries = {}
        
        for i, (label, field) in enumerate(fields):
            ttk.Label(self, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = ttk.Entry(self)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.entries[field] = entry
        
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        submit_btn = ttk.Button(btn_frame, text="Submit", command=self.submit)
        submit_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = ttk.Button(btn_frame, text="Back", 
                            command=lambda: controller.show_frame("HomePage"))
        back_btn.pack(side=tk.LEFT, padx=10)
    
    def submit(self):
        try:
            data = (
                self.entries['name'].get(),
                self.entries['flight_number'].get(),
                self.entries['departure'].get(),
                self.entries['destination'].get(),
                self.entries['date'].get(),
                self.entries['seat_number'].get()
            )
            
            if not all(data):
                raise ValueError("All fields are required")
            
            self.controller.db.create_reservation(data)
            messagebox.showinfo("Success", "Reservation created successfully!")
            
            for entry in self.entries.values():
                entry.delete(0, tk.END)
            
            self.controller.show_frame("HomePage")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))