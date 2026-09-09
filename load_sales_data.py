import csv
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="sales_profitability_db",
    user="postgres",
    password=input("Enter your PostgreSQL password: ")
)

cursor = conn.cursor()

csv_file = r"C:\Users\saraj\OneDrive\Desktop\sales_profitability.csv"

# Make sure the table is empty
cursor.execute("TRUNCATE TABLE sales_profitability;")

with open(csv_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header

    for row in reader:
        cursor.execute("""
            INSERT INTO sales_profitability (
                Order_ID, Order_Date, Region, City, Segment, Channel,
                Category, Subcategory, Product_ID, Customer_ID,
                Quantity, Unit_Price, Discount, Revenue, Cost,
                Profit, Profit_Margin, Year, Month, Month_Name, Quarter
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, row)

conn.commit()

cursor.execute("SELECT COUNT(*) FROM sales_profitability;")
count = cursor.fetchone()[0]

print(f"Successfully inserted {count} rows.")

cursor.close()
conn.close()