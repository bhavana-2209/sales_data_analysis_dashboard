# sales_data_analysis_dashboard.py
# REALISTIC SALES DATA ANALYSIS FOR YEAR 2025

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==========================================
# STEP 1: PROJECT SETUP
# ==========================================

os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)

print("✅ Project folders created")

# ==========================================
# STEP 2: CREATE REALISTIC 2025 SALES DATA
# ==========================================

np.random.seed(42)

categories = {
    "Electronics": (300, 1200),
    "Clothing": (50, 300),
    "Home & Garden": (80, 500),
    "Books": (20, 150),
    "Sports": (40, 400)
}

products = {
    "Electronics": ["Laptop", "Phone", "Monitor", "Tablet"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Shoes"],
    "Home & Garden": ["Chair", "Table", "Lamp", "Plant"],
    "Books": ["Novel", "Cookbook", "Science Book", "Biography"],
    "Sports": ["Football", "Cricket Bat", "Yoga Mat", "Tennis Racket"]
}

monthly_multiplier = {
    1: 0.9,
    2: 0.8,
    3: 1.0,
    4: 1.15,
    5: 1.05,
    6: 1.0,
    7: 1.08,
    8: 1.12,
    9: 1.1,
    10: 1.2,
    11: 1.45,
    12: 1.35
}

data = []

for order_id in range(1, 4568):

    category = np.random.choice(
        list(categories.keys()),
        p=[0.38, 0.22, 0.18, 0.12, 0.10]
    )

    product = np.random.choice(products[category])

    quantity = np.random.randint(1, 5)

    customer_id = np.random.randint(1000, 2235)

    random_day = np.random.randint(0, 365)

    order_date = pd.Timestamp("2025-01-01") + pd.Timedelta(days=random_day)

    month = order_date.month

    low, high = categories[category]

    base_price = np.random.uniform(low, high)

    total_amount = (
        base_price *
        quantity *
        monthly_multiplier[month]
    )

    data.append([
        order_id,
        customer_id,
        np.random.randint(1, 568),
        product,
        category,
        quantity,
        round(total_amount, 2),
        order_date
    ])

df = pd.DataFrame(data, columns=[
    "order_id",
    "customer_id",
    "product_id",
    "product_name",
    "category",
    "quantity",
    "total_amount",
    "order_date"
])

# Save CSV
csv_path = "data/sales_data_2025.csv"

df.to_csv(csv_path, index=False)

print("✅ Realistic 2025 dataset generated")
print(f"📁 Dataset saved: {csv_path}")

# ==========================================
# STEP 3: DATA CLEANING
# ==========================================

print("\n🧹 Cleaning Data...")

before = len(df)

df.drop_duplicates(inplace=True)

after = len(df)

print(f"Removed {before - after} duplicate rows")

# Missing values handling
numeric_cols = df.select_dtypes(include=np.number).columns

for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

categorical_cols = df.select_dtypes(include="object").columns

for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

print("✅ Missing values handled")

# ==========================================
# STEP 4: BASIC ANALYSIS
# ==========================================

total_sales = df["total_amount"].sum()

total_orders = len(df)

avg_order = df["total_amount"].mean()

unique_customers = df["customer_id"].nunique()

unique_products = df["product_id"].nunique()

category_sales = (
    df.groupby("category")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

# ==========================================
# STEP 5: MONTHLY TRENDS
# ==========================================

df["month"] = df["order_date"].dt.month_name()

monthly_sales = (
    df.groupby(df["order_date"].dt.month)["total_amount"]
    .sum()
)

growth = monthly_sales.pct_change() * 100

highest_month = monthly_sales.idxmax()

lowest_month = monthly_sales.idxmin()

best_growth_month = growth.idxmax()

month_names = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

# ==========================================
# STEP 6: CUSTOMER INSIGHTS
# ==========================================

customer_orders = df["customer_id"].value_counts()

repeat_customers = (customer_orders > 1).sum()

repeat_percent = (
    repeat_customers / unique_customers
) * 100

customer_value = (
    df.groupby("customer_id")["total_amount"]
    .sum()
)

avg_customer_value = customer_value.mean()

top_10_customers = customer_value.nlargest(
    int(unique_customers * 0.10)
)

top_10_revenue_percent = (
    top_10_customers.sum() / total_sales
) * 100

# ==========================================
# STEP 7: VISUALIZATIONS
# ==========================================

print("\n📊 Creating Visualizations...")

# Monthly Sales Trend
plt.figure(figsize=(12, 6))

monthly_sales.plot(marker="o")

plt.title("Monthly Sales Trend - 2025")

plt.xlabel("Month")

plt.ylabel("Sales ($)")

plt.grid(True)

plt.tight_layout()

plt.savefig("output/monthly_sales_trend_2025.png")

plt.close()

# Category Pie Chart
plt.figure(figsize=(8, 8))

category_sales.plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.ylabel("")

plt.title("Sales by Category - 2025")

plt.tight_layout()

plt.savefig("output/category_pie_chart_2025.png")

plt.close()

# Monthly Sales Bar Chart
plt.figure(figsize=(12, 6))

monthly_sales.plot(kind="bar")

plt.title("Monthly Sales Bar Chart - 2025")

plt.xlabel("Month")

plt.ylabel("Sales ($)")

plt.tight_layout()

plt.savefig("output/monthly_bar_chart_2025.png")

plt.close()

print("✅ Charts saved in output folder")

# ==========================================
# STEP 8: EXPORT REPORT
# ==========================================

excel_path = "output/sales_report_2025.xlsx"

with pd.ExcelWriter(excel_path) as writer:

    df.to_excel(
        writer,
        sheet_name="Raw Data",
        index=False
    )

    category_sales.to_excel(
        writer,
        sheet_name="Category Analysis"
    )

    monthly_sales.to_excel(
        writer,
        sheet_name="Monthly Trends"
    )

print(f"✅ Excel report saved: {excel_path}")

# ==========================================
# FINAL REPORT OUTPUT
# ==========================================

print("\n📊 SALES DATA ANALYSIS REPORT")
print("===============================\n")

print("📅 Analysis Period: Jan 2025 - Dec 2025\n")

print("📈 BASIC STATISTICS:")

print(f"- Total Sales: ${total_sales:,.2f}")

print(f"- Total Orders: {total_orders:,}")

print(f"- Average Order Value: ${avg_order:,.2f}")

print(f"- Unique Customers: {unique_customers:,}")

print(f"- Unique Products: {unique_products:,}")

print("\n🏆 TOP PRODUCT CATEGORIES:")

for i, (cat, value) in enumerate(category_sales.items(), 1):

    percent = (value / total_sales) * 100

    print(
        f"{i}. {cat}: "
        f"${value:,.0f} "
        f"({percent:.1f}%)"
    )

print("\n📅 MONTHLY TRENDS:")

print(
    f"- Highest Sales Month: "
    f"{month_names[highest_month]} "
    f"(${monthly_sales.max():,.0f})"
)

print(
    f"- Lowest Sales Month: "
    f"{month_names[lowest_month]} "
    f"(${monthly_sales.min():,.0f})"
)

print(
    f"- Average Monthly Sales: "
    f"${monthly_sales.mean():,.2f}"
)

print(
    f"- Best Growth Month: "
    f"{month_names[best_growth_month]} "
    f"(+{growth.max():.1f}%)"
)

print("\n👥 CUSTOMER INSIGHTS:")

print(
    f"- Repeat Customers: "
    f"{repeat_customers} "
    f"({repeat_percent:.1f}%)"
)

print(
    f"- Average Customer Value: "
    f"${avg_customer_value:,.2f}"
)

print(
    f"- Top 10% Customers Generate: "
    f"{top_10_revenue_percent:.1f}% of revenue"
)

print("\n💰 RECOMMENDATIONS:")

top_category = category_sales.idxmax()

print(
    f"1. Focus marketing on {top_category} category"
)

print(
    "2. Improve customer retention programs"
)

print(
    "3. Consider seasonal promotions during peak months"
)

print(
    "4. Expand high-performing product categories"
)

print("\n✅ SALES ANALYSIS COMPLETED SUCCESSFULLY")