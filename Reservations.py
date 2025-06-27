import tkinter as tk
from tkinter import ttk, messagebox
from home import HomePage
from edit_reservation import EditReservationPage

class ReservationsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Treeview for reservations
        self.tree = ttk.Treeview(self, columns=('id', 'name', 'flight', 'departure', 'destination', 'date', 'seat'), show='headings')
        
        # Define headings
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Name')
        self.tree.heading('flight', text='Flight')
        self.tree.heading('departure', text='Departure')
        self.tree.heading('destination', text='Destination')
        self.tree.heading('date', text='Date')
        self.tree.heading('seat', text='Seat')
        
        # Set column widths
        self.tree.column('id', width=50)
        self.tree.column('name', width=120)
        self.tree.column('flight', width=80)
        self.tree.column('departure', width=100)
        self.tree.column('destination', width=100)
        self.tree.column('date', width=100)
        self.tree.column('seat', width=80)
        
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        edit_btn = ttk.Button(btn_frame, text="Edit", command=self.edit_reservation)
        edit_btn.pack(side='left', padx=5)
        
        delete_btn = ttk.Button(btn_frame, text="Delete", command=self.delete_reservation)
        delete_btn.pack(side='left', padx=5)
        
        back_btn = ttk.Button(btn_frame, text="Back", 
                             command=lambda: controller.show_frame(HomePage))
        back_btn.pack(side='left', padx=5)
    
    def on_show(self):
        """Refresh data when page is shown"""
        try:
            self.load_reservations()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load reservations: {str(e)}")
    
    def load_reservations(self):
        """Load reservations from database into the treeview"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Load from database
            reservations = self.controller.db.get_all_reservations()
            for res in reservations:
                self.tree.insert('', 'end', values=res)
        except AttributeError:
            messagebox.showerror("Error", "Database connection not available")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load reservations: {str(e)}")
    
    def edit_reservation(self):
        """Open edit page for selected reservation"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a reservation to edit")
            return
        
        try:
            reservation_id = self.tree.item(selected[0])['values'][0]
            # Check if EditReservationPage exists in controller
            if EditReservationPage not in self.controller.frames:
                messagebox.showerror("Error", "Edit page not available")
                return
                
            self.controller.show_frame(EditReservationPage)
            edit_page = self.controller.frames[EditReservationPage]
            if hasattr(edit_page, 'load_reservation'):
                edit_page.load_reservation(reservation_id)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit reservation: {str(e)}")
    
    def delete_reservation(self):
        """Delete selected reservation"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a reservation to delete")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this reservation?"):
            return
        
        try:
            reservation_id = self.tree.item(selected[0])['values'][0]
            self.controller.db.delete_reservation(reservation_id)
            self.load_reservations()
            messagebox.showinfo("Success", "Reservation deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete reservation: {str(e)}")