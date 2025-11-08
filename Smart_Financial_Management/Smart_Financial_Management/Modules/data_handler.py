import sqlite3

def get_connection():
    return sqlite3.connect('ExpenseTracker.db')

def add_expense(date, payee, description, amount, mode, category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment, Category)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (date, payee, description, amount, mode, category))
    conn.commit()
    conn.close()

def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM ExpenseTracker WHERE ID=?', (expense_id,))
    conn.commit()
    conn.close()

def fetch_expenses():
    conn = get_connection()
    df = pd.read_sql_query('SELECT * FROM ExpenseTracker', conn)
    conn.close()
    return df