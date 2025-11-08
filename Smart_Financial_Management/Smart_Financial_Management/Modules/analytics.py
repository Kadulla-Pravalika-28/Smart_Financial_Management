import pandas as pd

def total_expense(df):
    return df['Amount'].sum()

def category_summary(df):
    return df.groupby('Category')['Amount'].sum().reset_index()

def monthly_trends(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')
    return df.groupby('Month')['Amount'].sum().reset_index()