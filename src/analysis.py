import pandas as pd
from pathlib import Path

# --------------------------------------------------
# File Paths
# --------------------------------------------------

DATA = Path(__file__).resolve().parents[1] / "data" / "sales_profitability.csv"
OUT = Path(__file__).resolve().parents[1] / "outputs"
OUT.mkdir(exist_ok=True)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = pd.read_csv(DATA, parse_dates=["Order_Date"])

# --------------------------------------------------
# Basic Data Checks
# --------------------------------------------------

print("Shape:", df.shape)

print("\nMissing values:")
print(df.isna().sum())

print("\nDuplicate orders:", df["Order_ID"].duplicated().sum())

# --------------------------------------------------
# 1. Overall KPIs
# --------------------------------------------------

total_revenue = df["Revenue"].sum()
total_cost = df["Cost"].sum()
total_profit = df["Profit"].sum()

kpis = pd.DataFrame({
    "Metric": [
        "Revenue",
        "Cost",
        "Profit",
        "Profit Margin",
        "Orders",
        "Units"
    ],
    "Value": [
        total_revenue,
        total_cost,
        total_profit,
        total_profit / total_revenue,
        df["Order_ID"].nunique(),
        df["Quantity"].sum()
    ]
})

kpis.to_csv(OUT / "kpis.csv", index=False)

# Overall profit margin used as benchmark
overall_margin = total_profit / total_revenue

# --------------------------------------------------
# 2. Monthly Performance
# --------------------------------------------------

monthly = (
    df.groupby(
        [
            df["Order_Date"].dt.year.rename("year"),
            df["Order_Date"].dt.month.rename("month")
        ]
    )
    .agg(
        revenue=("Revenue", "sum"),
        profit=("Profit", "sum")
    )
    .reset_index()
)

monthly["profit_margin"] = (
    monthly["profit"] / monthly["revenue"]
)

monthly = monthly.sort_values(["year", "month"])

monthly.to_csv(
    OUT / "monthly_performance.csv",
    index=False
)

# --------------------------------------------------
# 3. Category Analysis
# --------------------------------------------------

category = (
    df.groupby("Category")
    .agg(
        revenue=("Revenue", "sum"),
        profit=("Profit", "sum"),
        avg_discount=("Discount", "mean")
    )
    .reset_index()
)

category["profit_margin"] = (
    category["profit"] / category["revenue"]
)

category = category.sort_values(
    "profit",
    ascending=False
)

category.to_csv(
    OUT / "category_analysis.csv",
    index=False
)

# --------------------------------------------------
# 4. Region + Category + Channel
#    Below Overall Profit Margin
# --------------------------------------------------

low_margin = (
    df.groupby(
        ["Region", "Category", "Channel"]
    )
    .agg(
        revenue=("Revenue", "sum"),
        profit=("Profit", "sum"),
        avg_discount=("Discount", "mean")
    )
    .reset_index()
)

low_margin["profit_margin"] = (
    low_margin["profit"] / low_margin["revenue"]
)

low_margin = low_margin[
    low_margin["profit_margin"] < overall_margin
]

low_margin = low_margin.sort_values(
    "profit_margin"
)

low_margin.to_csv(
    OUT / "low_margin_areas.csv",
    index=False
)

# --------------------------------------------------
# 5. Discount Band Analysis
# --------------------------------------------------

bins = [
    -0.01,
    0.05,
    0.10,
    0.20,
    0.30,
    0.40,
    0.55
]

labels = [
    "0-5%",
    "5-10%",
    "10-20%",
    "20-30%",
    "30-40%",
    "40-55%"
]

df["Discount_Band"] = pd.cut(
    df["Discount"],
    bins=bins,
    labels=labels
)

discount = (
    df.groupby(
        "Discount_Band",
        observed=False
    )
    .agg(
        revenue=("Revenue", "sum"),
        profit=("Profit", "sum"),
        orders=("Order_ID", "nunique")
    )
    .reset_index()
)

discount["profit_margin"] = (
    discount["profit"] / discount["revenue"]
)

discount.to_csv(
    OUT / "discount_analysis.csv",
    index=False
)

# --------------------------------------------------
# 6. Category + Subcategory Analysis
# --------------------------------------------------

subcategory = (
    df.groupby(
        ["Category", "Subcategory"]
    )
    .agg(
        revenue=("Revenue", "sum"),
        profit=("Profit", "sum")
    )
    .reset_index()
)

subcategory["profit_margin"] = (
    subcategory["profit"] / subcategory["revenue"]
)

subcategory = subcategory.sort_values(
    "profit_margin",
    ascending=False
)

subcategory.to_csv(
    OUT / "subcategory_analysis.csv",
    index=False
)

# --------------------------------------------------
# 7. Channel Analysis
# --------------------------------------------------

channel = (
    df.groupby("Channel")
    .agg(
        revenue=("Revenue", "sum"),
        profit=("Profit", "sum"),
        avg_discount=("Discount", "mean")
    )
    .reset_index()
)

channel["profit_margin"] = (
    channel["profit"] / channel["revenue"]
)

channel = channel.sort_values(
    "profit",
    ascending=False
)

channel.to_csv(
    OUT / "channel_analysis.csv",
    index=False
)

# --------------------------------------------------
# 8. Region Analysis
# --------------------------------------------------

region = (
    df.groupby("Region")
    .agg(
        revenue=("Revenue", "sum"),
        profit=("Profit", "sum")
    )
    .reset_index()
)

region["profit_margin"] = (
    region["profit"] / region["revenue"]
)

region = region.sort_values(
    "profit",
    ascending=False
)

region.to_csv(
    OUT / "region_analysis.csv",
    index=False
)

# --------------------------------------------------
# Completion Message
# --------------------------------------------------

print("\nAnalysis completed successfully.")

print("\nOverall Profit Margin:",
      round(overall_margin * 100, 2), "%")

print("\nAnalysis files written to:")
print(OUT)
