import sqlite3
import pandas as pd

# Connect to SQLite database
connector = sqlite3.connect('ExpenseTracker.db')
cursor = connector.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS ExpenseTracker (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Date TEXT,
    Payee TEXT,
    Description TEXT,
    Amount REAL,
    ModeOfPayment TEXT,
    Category TEXT
)
''')
connector.commit()

# Optional: Load CSV into SQLite
csv_file = 'data/ExpenseTracker_dataset.csv'
try:
    df = pd.read_csv(csv_file)
    df.to_sql('ExpenseTracker', connector, if_exists='append', index=False)
except Exception as e:
    print(f"Error loading CSV: {e}")