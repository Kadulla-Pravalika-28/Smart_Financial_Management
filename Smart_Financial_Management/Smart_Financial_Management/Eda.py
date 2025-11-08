# save_plots.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------
# Paths
# --------------------------
DATA_PATH = os.path.join("data", "ExpenseTracker_dataset.csv")
ASSETS_PATH = "Outputs"

# Create assets folder if not exists
os.makedirs(ASSETS_PATH, exist_ok=True)

# --------------------------
# Load data
# --------------------------
df = pd.read_csv(DATA_PATH)
df['Date'] = pd.to_datetime(df['Date'])

# --------------------------
# 1. Expenses by Category (Bar)
# --------------------------
category_data = df.groupby('Category')['Amount'].sum().reset_index()
plt.figure(figsize=(8,5))
sns.barplot(x='Category', y='Amount', data=category_data, hue='Category', dodge=False, legend=False)
plt.xticks(rotation=45)
plt.title("Expenses by Category")
plt.tight_layout()
plt.savefig(os.path.join(ASSETS_PATH, "expenses_by_category.png"))
plt.close()

# --------------------------
# 2. Monthly Spending Trend (Line)
# --------------------------
df['Month'] = df['Date'].dt.to_period('M')
monthly_summary = df.groupby('Month')['Amount'].sum().reset_index()
plt.figure(figsize=(10,5))
plt.plot(monthly_summary['Month'].astype(str), monthly_summary['Amount'], marker='o', color='blue')
plt.xticks(rotation=45)
plt.title("Monthly Spending Trend")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.tight_layout()
plt.savefig(os.path.join(ASSETS_PATH, "monthly_spending_trend.png"))
plt.close()

# --------------------------
# 3. Top 5 Payees (Bar)
# --------------------------
top_payees = df.groupby('Payee')['Amount'].sum().sort_values(ascending=False).head(5).reset_index()
plt.figure(figsize=(8,5))
sns.barplot(x='Payee', y='Amount', data=top_payees, hue='Payee', dodge=False, legend=False)
plt.xticks(rotation=45)
plt.title("Top 5 Payees")
plt.tight_layout()
plt.savefig(os.path.join(ASSETS_PATH, "top_5_payees.png"))
plt.close()

# --------------------------
# 4. Expenses by Payment Mode (Pie)
# --------------------------
payment_data = df.groupby("ModeOfPayment")["Amount"].sum().reset_index()
plt.figure(figsize=(6,6))
plt.pie(payment_data['Amount'], labels=payment_data['ModeOfPayment'], autopct='%1.1f%%', startangle=140)
plt.title("Expenses by Payment Mode")
plt.tight_layout()
plt.savefig(os.path.join(ASSETS_PATH, "expenses_by_payment_mode.png"))
plt.close()

# --------------------------
# 5. Daily Spending Trend (Line)
# --------------------------
daily_data = df.groupby('Date')['Amount'].sum().reset_index()
plt.figure(figsize=(10,5))
plt.plot(daily_data['Date'], daily_data['Amount'], marker='o', color='purple')
plt.xticks(rotation=45)
plt.title("Daily Spending Trend")
plt.xlabel("Date")
plt.ylabel("Amount Spent")
plt.tight_layout()
plt.savefig(os.path.join(ASSETS_PATH, "daily_spending_trend.png"))
plt.close()

# --------------------------
# 6. Category-wise Spending (Pie)
# --------------------------
plt.figure(figsize=(6,6))
plt.pie(category_data['Amount'], labels=category_data['Category'], autopct='%1.1f%%', startangle=140)
plt.title("Category-wise Spending")
plt.tight_layout()
plt.savefig(os.path.join(ASSETS_PATH, "category_pie_chart.png"))
plt.close()

# --------------------------
# 7. Top 5 Categories (Bar)
# --------------------------
top_categories = category_data.sort_values(by="Amount", ascending=False).head(5)
plt.figure(figsize=(8,5))
sns.barplot(x='Category', y='Amount', data=top_categories, hue='Category', dodge=False, legend=False)
plt.xticks(rotation=45)
plt.title("Top 5 Expense Categories")
plt.tight_layout()
plt.savefig(os.path.join(ASSETS_PATH, "top_5_categories.png"))
plt.close()

# --------------------------
# 8. Cumulative Spending Over Time (Line)
# --------------------------
cumulative_data = df.sort_values('Date')
cumulative_data['Cumulative'] = cumulative_data['Amount'].cumsum()
plt.figure(figsize=(10,5))
plt.plot(cumulative_data['Date'], cumulative_data['Cumulative'], marker='o', color='darkgreen')
plt.xticks(rotation=45)
plt.title("Cumulative Spending Over Time")
plt.xlabel("Date")
plt.ylabel("Cumulative Amount")
plt.tight_layout()
plt.savefig(os.path.join(ASSETS_PATH, "cumulative_spending.png"))
plt.close()

print("✅ All plots saved in the 'Outputs/' folder!")