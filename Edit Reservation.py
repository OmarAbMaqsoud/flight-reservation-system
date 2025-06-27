import tkinter as tk
from tkinter import ttk, messagebox

class EditReservationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.reservation_id = None
        
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
        
        update_btn = ttk.Button(btn_frame, text="Update", command=self.update)
        update_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = ttk.Button(btn_frame, text="Back", 
                            command=lambda: controller.show_frame("ReservationsPage"))
        back_btn.pack(side=tk.LEFT, padx=10)
    
    def load_reservation(self, reservation_id):
        """Load reservation data into form fields"""
        self.reservation_id = reservation_id
        reservation = self.controller.db.get_reservation(reservation_id)
        
        if reservation:
            for field, value in zip(['name', 'flight_number', 'departure', 
                                   'destination', 'date', 'seat_number'], 
                                   reservation[1:7]):
                self.entries[field].delete(0, tk.END)
                self.entries[field].insert(0, value)
    
    def update(self):
        """Update reservation in database"""
        try:
            if not self.reservation_id:
                raise ValueError("No reservation selected")
            
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
            
            self.controller.db.update_reservation(self.reservation_id, data)
            messagebox.showinfo("Success", "Reservation updated successfully!")
            
            self.controller.show_frame("ReservationsPage")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))