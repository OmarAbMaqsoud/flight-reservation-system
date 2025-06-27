import tkinter as tk
from tkinter import ttk
from home import HomePage
from database import Database

class FlightReservationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flight Reservation System")
        self.geometry("800x600")
        self.resizable(False, False)
        
        # Initialize database
        self.db = Database()
        
        # Container for all frames
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Dictionary to hold all frames
        self.frames = {}
        
        # Initialize all pages
        for F in (HomePage, BookingPage, ReservationsPage, EditReservationPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(HomePage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

if __name__ == "__main__":
    app = FlightReservationApp()
    app.mainloop()