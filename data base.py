import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='flights.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        
    def create_tables(self):
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
        self.conn.commit()
    
    def create_reservation(self, data):
        query = '''
            INSERT INTO reservations (name, flight_number, departure, destination, date, seat_number)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(query, data)
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_all_reservations(self):
        self.cursor.execute('SELECT * FROM reservations ORDER BY created_at DESC')
        return self.cursor.fetchall()
    
    def get_reservation(self, reservation_id):
        self.cursor.execute('SELECT * FROM reservations WHERE id = ?', (reservation_id,))
        return self.cursor.fetchone()
    
    def update_reservation(self, reservation_id, data):
        query = '''
            UPDATE reservations 
            SET name = ?, flight_number = ?, departure = ?, destination = ?, date = ?, seat_number = ?
            WHERE id = ?
        '''
        self.cursor.execute(query, (*data, reservation_id))
        self.conn.commit()
    
    def delete_reservation(self, reservation_id):
        self.cursor.execute('DELETE FROM reservations WHERE id = ?', (reservation_id,))
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()