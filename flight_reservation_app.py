import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class FlightReservationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Reservation System")
        
        window_width = 1000
        window_height = 700
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        x = (screen_width/2) - (window_width/2)
        y = (screen_height/2) - (window_height/2)
        self.root.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
        
        self.init_db()
        
        self.create_styles()
        
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        self.create_frames()
        
        self.show_frame("Home")
    
    def create_styles(self):
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('Header.TLabel', 
                        font=('Arial', 18, 'bold'), 
                        background='#f0f0f0',
                        foreground='#333333')
        style.configure('Normal.TLabel', 
                        font=('Arial', 12), 
                        background='#f0f0f0',
                        foreground='#333333')
        style.configure('TButton', 
                       font=('Arial', 12),
                       padding=5)
        style.configure('Treeview', 
                       font=('Arial', 11),
                       rowheight=25)
        style.configure('Treeview.Heading', 
                       font=('Arial', 12, 'bold'))
    
    def init_db(self):
        self.conn = sqlite3.connect('flights.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                flight_number TEXT NOT NULL,
                departure TEXT NOT NULL,
                destination TEXT NOT NULL,
                date TEXT NOT NULL,
                seat_number TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute("SELECT COUNT(*) FROM reservations")
        if self.cursor.fetchone()[0] == 0:
            sample_reservations = [
                ('John Doe', 'AA123', 'New York', 'Los Angeles', '2023-12-15', '15A'),
                ('Jane Smith', 'DL456', 'Chicago', 'Miami', '2023-12-16', '22B'),
                ('Robert Johnson', 'UA789', 'San Francisco', 'Seattle', '2023-12-17', '8C')
            ]
            self.cursor.executemany('''
                INSERT INTO reservations (name, flight_number, departure, destination, date, seat_number)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', sample_reservations)
            self.conn.commit()
    
    def create_frames(self):
        self.frames = {}
        
        self.frames["Home"] = ttk.Frame(self.main_container)
        self.create_home_frame()
        
        self.frames["Booking"] = ttk.Frame(self.main_container)
        self.create_booking_frame()
        
        self.frames["Reservations"] = ttk.Frame(self.main_container)
        self.create_reservations_frame()
        
        self.frames["Edit"] = ttk.Frame(self.main_container)
        self.create_edit_frame()
        
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")
    
    def create_home_frame(self):
        frame = self.frames["Home"]
        
        header = ttk.Label(frame, text="Flight Reservation System", style='Header.TLabel')
        header.pack(pady=40)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        book_btn = ttk.Button(btn_frame, text="Book Flight", 
                             command=lambda: self.show_frame("Booking"))
        book_btn.pack(pady=15, ipadx=30, ipady=10)
        
        view_btn = ttk.Button(btn_frame, text="View Reservations", 
                             command=lambda: self.show_frame("Reservations"))
        view_btn.pack(pady=15, ipadx=30, ipady=10)
        
        exit_btn = ttk.Button(btn_frame, text="Exit", 
                             command=self.root.quit)
        exit_btn.pack(pady=15, ipadx=30, ipady=10)
    
    def create_booking_frame(self):
        frame = self.frames["Booking"]
        
        header = ttk.Label(frame, text="Book a Flight", style='Header.TLabel')
        header.grid(row=0, column=0, columnspan=2, pady=20)
        
        fields = [
            ("Passenger Name", "name"),
            ("Flight Number", "flight_number"),
            ("Departure City", "departure"),
            ("Destination City", "destination"),
            ("Date (YYYY-MM-DD)", "date"),
            ("Seat Number", "seat_number")
        ]
        
        self.booking_entries = {}
        
        for i, (label, field) in enumerate(fields):
            ttk.Label(frame, text=label, style='Normal.TLabel').grid(row=i+1, column=0, padx=10, pady=5, sticky="e")
            entry = ttk.Entry(frame, font=('Arial', 12))
            entry.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
            self.booking_entries[field] = entry
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=len(fields)+2, column=0, columnspan=2, pady=20)
        
        submit_btn = ttk.Button(btn_frame, text="Submit", command=self.submit_booking)
        submit_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = ttk.Button(btn_frame, text="Back", 
                            command=lambda: self.show_frame("Home"))
        back_btn.pack(side=tk.LEFT, padx=10)
    
    def create_reservations_frame(self):
        frame = self.frames["Reservations"]
        
        header = ttk.Label(frame, text="All Reservations", style='Header.TLabel')
        header.pack(pady=20)
        
        self.reservations_tree = ttk.Treeview(frame, columns=('id', 'name', 'flight', 'departure', 'destination', 'date', 'seat'), show='headings')
        
        self.reservations_tree.heading('id', text='ID')
        self.reservations_tree.heading('name', text='Passenger Name')
        self.reservations_tree.heading('flight', text='Flight Number')
        self.reservations_tree.heading('departure', text='Departure')
        self.reservations_tree.heading('destination', text='Destination')
        self.reservations_tree.heading('date', text='Date')
        self.reservations_tree.heading('seat', text='Seat Number')
        
        self.reservations_tree.column('id', width=50, anchor='center')
        self.reservations_tree.column('name', width=150)
        self.reservations_tree.column('flight', width=100, anchor='center')
        self.reservations_tree.column('departure', width=120)
        self.reservations_tree.column('destination', width=120)
        self.reservations_tree.column('date', width=100, anchor='center')
        self.reservations_tree.column('seat', width=80, anchor='center')
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.reservations_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.reservations_tree.configure(yscrollcommand=scrollbar.set)
        
        self.reservations_tree.pack(fill='both', expand=True, padx=20, pady=10)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        edit_btn = ttk.Button(btn_frame, text="Edit", command=self.edit_reservation)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.Button(btn_frame, text="Delete", command=self.delete_reservation)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(btn_frame, text="Refresh", command=self.load_reservations)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn = ttk.Button(btn_frame, text="Back", 
                            command=lambda: self.show_frame("Home"))
        back_btn.pack(side=tk.LEFT, padx=5)
    
    def create_edit_frame(self):
        frame = self.frames["Edit"]
        self.current_reservation_id = None
        
        # Header
        header = ttk.Label(frame, text="Edit Reservation", style='Header.TLabel')
        header.grid(row=0, column=0, columnspan=2, pady=20)
        
        fields = [
            ("Passenger Name", "name"),
            ("Flight Number", "flight_number"),
            ("Departure City", "departure"),
            ("Destination City", "destination"),
            ("Date (YYYY-MM-DD)", "date"),
            ("Seat Number", "seat_number")
        ]
        
        self.edit_entries = {}
        
        for i, (label, field) in enumerate(fields):
            ttk.Label(frame, text=label, style='Normal.TLabel').grid(row=i+1, column=0, padx=10, pady=5, sticky="e")
            entry = ttk.Entry(frame, font=('Arial', 12))
            entry.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
            self.edit_entries[field] = entry
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=len(fields)+2, column=0, columnspan=2, pady=20)
        
        update_btn = ttk.Button(btn_frame, text="Update", command=self.update_reservation)
        update_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = ttk.Button(btn_frame, text="Back", 
                            command=lambda: self.show_frame("Reservations"))
        back_btn.pack(side=tk.LEFT, padx=10)
    
    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        
        if frame_name == "Reservations":
            self.load_reservations()
    
    def submit_booking(self):
        try:
            data = (
                self.booking_entries['name'].get(),
                self.booking_entries['flight_number'].get(),
                self.booking_entries['departure'].get(),
                self.booking_entries['destination'].get(),
                self.booking_entries['date'].get(),
                self.booking_entries['seat_number'].get()
            )
            
            if not all(data):
                raise ValueError("All fields are required")
            
            self.cursor.execute('''
                INSERT INTO reservations (name, flight_number, departure, destination, date, seat_number)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', data)
            self.conn.commit()
            
            messagebox.showinfo("Success", "Reservation created successfully!")
            
            for entry in self.booking_entries.values():
                entry.delete(0, tk.END)
            
            self.show_frame("Home")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load_reservations(self):
        for item in self.reservations_tree.get_children():
            self.reservations_tree.delete(item)
        
        self.cursor.execute("SELECT id, name, flight_number, departure, destination, date, seat_number FROM reservations ORDER BY created_at DESC")
        reservations = self.cursor.fetchall()
        
        for res in reservations:
            self.reservations_tree.insert('', 'end', values=res)
    
    def edit_reservation(self):
        selected = self.reservations_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a reservation to edit")
            return
        
        reservation_id = self.reservations_tree.item(selected[0])['values'][0]
        self.current_reservation_id = reservation_id
        
        self.cursor.execute("SELECT name, flight_number, departure, destination, date, seat_number FROM reservations WHERE id = ?", (reservation_id,))
        reservation = self.cursor.fetchone()
        
        if reservation:
            for field, value in zip(['name', 'flight_number', 'departure', 'destination', 'date', 'seat_number'], reservation):
                self.edit_entries[field].delete(0, tk.END)
                self.edit_entries[field].insert(0, value)
            
            self.show_frame("Edit")
    
    def update_reservation(self):
        try:
            if not self.current_reservation_id:
                raise ValueError("No reservation selected")
            
            data = (
                self.edit_entries['name'].get(),
                self.edit_entries['flight_number'].get(),
                self.edit_entries['departure'].get(),
                self.edit_entries['destination'].get(),
                self.edit_entries['date'].get(),
                self.edit_entries['seat_number'].get()
            )
            
            if not all(data):
                raise ValueError("All fields are required")
            
            self.cursor.execute('''
                UPDATE reservations 
                SET name = ?, flight_number = ?, departure = ?, destination = ?, date = ?, seat_number = ?
                WHERE id = ?
            ''', (*data, self.current_reservation_id))
            self.conn.commit()
            
            messagebox.showinfo("Success", "Reservation updated successfully!")
            
            self.show_frame("Reservations")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_reservation(self):
        selected = self.reservations_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a reservation to delete")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this reservation?"):
            return
        
        reservation_id = self.reservations_tree.item(selected[0])['values'][0]
        
        self.cursor.execute("DELETE FROM reservations WHERE id = ?", (reservation_id,))
        self.conn.commit()
        
        messagebox.showinfo("Success", "Reservation deleted successfully!")
        
        self.load_reservations()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlightReservationApp(root)
    root.mainloop()