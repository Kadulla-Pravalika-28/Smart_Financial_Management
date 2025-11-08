import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --------------------------
# Database setup
# --------------------------
conn = sqlite3.connect("ExpenseTracker.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS ExpenseTracker (
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Date DATETIME,
    Payee TEXT,
    Description TEXT,
    Amount FLOAT,
    ModeOfPayment TEXT,
    Category TEXT
)
''')
conn.commit()

# --------------------------
# Streamlit layout
# --------------------------
st.set_page_config(page_title="Smart Financial Management", 
                   page_icon="💰", 
                   layout="wide",           
                   initial_sidebar_state="collapsed")

st.markdown("<h1 style='text-align: center;'>💰 Smart Financial Management - Expense Tracker</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Smart Tracking for Smarter Spending..!</h3>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --------------------------
# Initialize session state for current session expenses
# --------------------------
if 'session_expenses' not in st.session_state:
    st.session_state['session_expenses'] = pd.DataFrame(columns=["Date", "Payee", "Description", "Amount", "ModeOfPayment", "Category"])

# --------------------------
# Add Expense Form (Main Page)
# --------------------------
st.subheader("📝 Record Your Spending")
with st.form(key="expense_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        date = st.date_input("Date", value=datetime.today())
    with col2:
        payee = st.text_input("Payee")
    with col3:
        description = st.text_input("Description")
    
    col4, col5, col6 = st.columns(3)
    with col4:
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
    with col5:
        mode_of_payment = st.selectbox("Mode of Payment", ["Cash", "Credit Card", "Debit Card", "UPI", "Other"])
    with col6:
        category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"])
    
    submit_button = st.form_submit_button(label="Add Expense")

    errors = []
    if not payee.strip():
        errors.append("Payee cannot be empty.")
    if amount <= 0:
        errors.append("Amount must be greater than 0.")

    if submit_button:
        if errors:
            for e in errors:
                st.markdown(f"<p style='color:red; font-weight:bold;'>⚠ {e}</p>", unsafe_allow_html=True)
        else:
            # Store in database
            cursor.execute('''
            INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment, Category)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (date, payee, description, amount, mode_of_payment, category))
            conn.commit()
            
            # Store in session state
            st.session_state['session_expenses'] = pd.concat([
                st.session_state['session_expenses'],
                pd.DataFrame([{
                    "Date": date, 
                    "Payee": payee, 
                    "Description": description, 
                    "Amount": amount, 
                    "ModeOfPayment": mode_of_payment, 
                    "Category": category
                }])
            ], ignore_index=True)

            st.success(f"Expense of ₹{amount} added successfully!")

# --------------------------
# Display session expenses
# --------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📊 Recent Expenses (Current Session)")
st.dataframe(st.session_state['session_expenses'].tail(5))

# --------------------------
# Quick Overview for current session
# --------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📈 Quick Overview (Current Session)")
session_df = st.session_state['session_expenses']

if not session_df.empty:
    total_expense = session_df["Amount"].sum()
    total_entries = len(session_df)
    last_expense = session_df.iloc[-1]["Amount"]

    col1, col2, col3 = st.columns(3)
    col1.metric("💵 Total Expense", f"₹{total_expense:,.2f}")
    col2.metric("🗂 Total Entries", f"{total_entries}")
    col3.metric("📝 Last Expense", f"₹{last_expense:,.2f}")

# --------------------------
# View All Past Expenses (Optional)
# --------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📂 Past Expenses (All Stored Data)")

if st.checkbox("Show All Past Expenses"):
    # Reconnect to DB
    conn = sqlite3.connect("ExpenseTracker.db")
    df_all = pd.read_sql_query("SELECT * FROM ExpenseTracker", conn)
    df_all['Date'] = pd.to_datetime(df_all['Date'])
    st.dataframe(df_all.head(5))
    conn.close()

# --------------------------
# Close connection
# --------------------------
conn.close()