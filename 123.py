import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class FlightReservationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Reservation System")
        self.root.geometry("800x600")
        
        # Initialize database
        self.init_db()
        
        # Create GUI
        self.create_widgets()
        
        # Load flights
        self.load_flights()
        
    def init_db(self):
        self.conn = sqlite3.connect('flight_reservation.db')
        self.cursor = self.conn.cursor()
        
        # Create tables if they don't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS flights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_number TEXT NOT NULL,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                departure_time TEXT NOT NULL,
                arrival_time TEXT NOT NULL,
                price REAL NOT NULL,
                seats_available INTEGER NOT NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_id INTEGER NOT NULL,
                passenger_name TEXT NOT NULL,
                passenger_email TEXT NOT NULL,
                seats_reserved INTEGER NOT NULL,
                reservation_time TEXT NOT NULL,
                FOREIGN KEY (flight_id) REFERENCES flights (id)
            )
        ''')
        
        # Insert sample flights if the table is empty
        self.cursor.execute("SELECT COUNT(*) FROM flights")
        if self.cursor.fetchone()[0] == 0:
            sample_flights = [
                ('AA123', 'New York', 'Los Angeles', '2025-6-01 08:00', '2025-6-27 11:00', 299.99, 150),
                ('DL456', 'Chicago', 'Miami', '2025-6-27 10:30', '2025-6-27 14:15', 249.99, 120),
                ('UA789', 'San Francisco', 'Seattle', '2025-6-27 07:45', '2025-6-27 09:30', 199.99, 100),
                ('SW234', 'Denver', 'Las Vegas', '2025-6-27 13:20', '2025-6-27 15:10', 159.99, 80),
                ('BA567', 'London', 'Paris', '2025-6-27 09:15', '2025-6-27 11:30', 349.99, 200),
            ]
            self.cursor.executemany('''
                INSERT INTO flights (flight_number, origin, destination, departure_time, arrival_time, price, seats_available)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', sample_flights)
            self.conn.commit()
    
    def create_widgets(self):
        # Create main frames
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Flight List Frame
        self.flight_frame = ttk.LabelFrame(self.main_frame, text="Available Flights", padding="10")
        self.flight_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Treeview for flights
        self.flight_tree = ttk.Treeview(self.flight_frame, columns=('id', 'flight_number', 'origin', 'destination', 'departure', 'arrival', 'price', 'seats'), show='headings')
        self.flight_tree.heading('id', text='ID')
        self.flight_tree.heading('flight_number', text='Flight Number')
        self.flight_tree.heading('origin', text='Origin')
        self.flight_tree.heading('destination', text='Destination')
        self.flight_tree.heading('departure', text='Departure')
        self.flight_tree.heading('arrival', text='Arrival')
        self.flight_tree.heading('price', text='Price ($)')
        self.flight_tree.heading('seats', text='Seats Available')
        
        self.flight_tree.column('id', width=40, anchor='center')
        self.flight_tree.column('flight_number', width=100, anchor='center')
        self.flight_tree.column('origin', width=100, anchor='center')
        self.flight_tree.column('destination', width=100, anchor='center')
        self.flight_tree.column('departure', width=120, anchor='center')
        self.flight_tree.column('arrival', width=120, anchor='center')
        self.flight_tree.column('price', width=80, anchor='center')
        self.flight_tree.column('seats', width=80, anchor='center')
        
        self.flight_tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.flight_tree, orient="vertical", command=self.flight_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.flight_tree.configure(yscrollcommand=scrollbar.set)
        
        # Reservation Frame
        self.reservation_frame = ttk.LabelFrame(self.main_frame, text="Make Reservation", padding="10")
        self.reservation_frame.pack(fill=tk.X, pady=5)
        
        # Reservation form
        ttk.Label(self.reservation_frame, text="Flight ID:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.flight_id_entry = ttk.Entry(self.reservation_frame, width=10)
        self.flight_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(self.reservation_frame, text="Passenger Name:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.passenger_name_entry = ttk.Entry(self.reservation_frame, width=30)
        self.passenger_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(self.reservation_frame, text="Passenger Email:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.passenger_email_entry = ttk.Entry(self.reservation_frame, width=30)
        self.passenger_email_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(self.reservation_frame, text="Number of Seats:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.seats_entry = ttk.Spinbox(self.reservation_frame, from_=1, to=10, width=5)
        self.seats_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        
        self.reserve_button = ttk.Button(self.reservation_frame, text="Make Reservation", command=self.make_reservation)
        self.reserve_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # View Reservations Button
        self.view_reservations_button = ttk.Button(self.main_frame, text="View Reservations", command=self.view_reservations)
        self.view_reservations_button.pack(pady=5)
        
        # Bind flight selection to auto-fill flight ID
        self.flight_tree.bind('<<TreeviewSelect>>', self.on_flight_select)
    
    def load_flights(self):
        # Clear existing data
        for item in self.flight_tree.get_children():
            self.flight_tree.delete(item)
        
        # Fetch flights from database
        self.cursor.execute("SELECT id, flight_number, origin, destination, departure_time, arrival_time, price, seats_available FROM flights")
        flights = self.cursor.fetchall()
        
        # Add flights to treeview
        for flight in flights:
            self.flight_tree.insert('', 'end', values=flight)
    
    def on_flight_select(self, event):
        selected_item = self.flight_tree.focus()
        if selected_item:
            flight_data = self.flight_tree.item(selected_item)['values']
            self.flight_id_entry.delete(0, tk.END)
            self.flight_id_entry.insert(0, flight_data[0])
    
    def make_reservation(self):
        try:
            flight_id = int(self.flight_id_entry.get())
            passenger_name = self.passenger_name_entry.get().strip()
            passenger_email = self.passenger_email_entry.get().strip()
            seats = int(self.seats_entry.get())
            
            # Validate inputs
            if not passenger_name:
                messagebox.showerror("Error", "Please enter passenger name")
                return
            if not passenger_email or '@' not in passenger_email:
                messagebox.showerror("Error", "Please enter a valid email address")
                return
            if seats < 1:
                messagebox.showerror("Error", "Please enter at least 1 seat")
                return
            
            # Check flight availability
            self.cursor.execute("SELECT seats_available FROM flights WHERE id=?", (flight_id,))
            result = self.cursor.fetchone()
            
            if not result:
                messagebox.showerror("Error", "Invalid Flight ID")
                return
                
            seats_available = result[0]
            
            if seats > seats_available:
                messagebox.showerror("Error", f"Only {seats_available} seats available")
                return
            
            # Create reservation
            reservation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute('''
                INSERT INTO reservations (flight_id, passenger_name, passenger_email, seats_reserved, reservation_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (flight_id, passenger_name, passenger_email, seats, reservation_time))
            
            # Update available seats
            self.cursor.execute('''
                UPDATE flights SET seats_available = seats_available - ? WHERE id = ?
            ''', (seats, flight_id))
            
            self.conn.commit()
            
            messagebox.showinfo("Success", "Reservation created successfully!")
            
            # Clear form
            self.passenger_name_entry.delete(0, tk.END)
            self.passenger_email_entry.delete(0, tk.END)
            self.seats_entry.delete(0, tk.END)
            self.seats_entry.insert(0, 1)
            
            # Refresh flight list
            self.load_flights()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for Flight ID and Seats")
    
    def view_reservations(self):
        # Create a new window for reservations
        reservations_window = tk.Toplevel(self.root)
        reservations_window.title("Reservations")
        reservations_window.geometry("900x500")
        
        # Treeview for reservations
        reservation_tree = ttk.Treeview(reservations_window, columns=('id', 'flight_number', 'passenger_name', 'passenger_email', 'seats', 'reservation_time'), show='headings')
        reservation_tree.heading('id', text='Reservation ID')
        reservation_tree.heading('flight_number', text='Flight Number')
        reservation_tree.heading('passenger_name', text='Passenger Name')
        reservation_tree.heading('passenger_email', text='Passenger Email')
        reservation_tree.heading('seats', text='Seats Reserved')
        reservation_tree.heading('reservation_time', text='Reservation Time')
        
        reservation_tree.column('id', width=80, anchor='center')
        reservation_tree.column('flight_number', width=100, anchor='center')
        reservation_tree.column('passenger_name', width=150, anchor='center')
        reservation_tree.column('passenger_email', width=150, anchor='center')
        reservation_tree.column('seats', width=80, anchor='center')
        reservation_tree.column('reservation_time', width=150, anchor='center')
        
        reservation_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(reservation_tree, orient="vertical", command=reservation_tree.yview)
        scrollbar.pack(side="right", fill="y")
        reservation_tree.configure(yscrollcommand=scrollbar.set)
        
        # Fetch reservations with flight details
        self.cursor.execute('''
            SELECT r.id, f.flight_number, r.passenger_name, r.passenger_email, r.seats_reserved, r.reservation_time
            FROM reservations r
            JOIN flights f ON r.flight_id = f.id
            ORDER BY r.reservation_time DESC
        ''')
        reservations = self.cursor.fetchall()
        
        # Add reservations to treeview
        for reservation in reservations:
            reservation_tree.insert('', 'end', values=reservation)
        
        # Close button
        close_button = ttk.Button(reservations_window, text="Close", command=reservations_window.destroy)
        close_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FlightReservationApp(root)
    root.mainloop()