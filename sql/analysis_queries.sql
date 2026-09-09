


SELECT
    SUM(Revenue) AS total_revenue,
    SUM(Cost) AS total_cost,
    SUM(Profit) AS total_profit,
    SUM(Profit) / NULLIF(SUM(Revenue), 0) AS profit_margin,
    COUNT(DISTINCT Order_ID) AS orders,
    SUM(Quantity) AS units
FROM sales_profitability;


SELECT
    EXTRACT(YEAR FROM Order_Date) AS year,
    EXTRACT(MONTH FROM Order_Date) AS month,
    SUM(Revenue) AS revenue,
    SUM(Profit) AS profit,
    SUM(Profit) / NULLIF(SUM(Revenue), 0) AS profit_margin
FROM sales_profitability
GROUP BY
    EXTRACT(YEAR FROM Order_Date),
    EXTRACT(MONTH FROM Order_Date)
ORDER BY
    year,
    month;


SELECT
    Category,
    SUM(Revenue) AS revenue,
    SUM(Profit) AS profit,
    SUM(Profit) / NULLIF(SUM(Revenue), 0) AS profit_margin,
    AVG(Discount) AS avg_discount
FROM sales_profitability
GROUP BY Category
ORDER BY profit DESC;


SELECT
    Region,
    Category,
    Channel,
    SUM(Revenue) AS revenue,
    SUM(Profit) AS profit,
    SUM(Profit) / NULLIF(SUM(Revenue), 0) AS profit_margin,
    AVG(Discount) AS avg_discount
FROM sales_profitability
GROUP BY
    Region,
    Category,
    Channel
HAVING
    SUM(Profit) / NULLIF(SUM(Revenue), 0) < 0.3260442
ORDER BY
    profit_margin;



SELECT
    CASE
        WHEN Discount <= 0.05 THEN '0-5%'
        WHEN Discount <= 0.10 THEN '5-10%'
        WHEN Discount <= 0.20 THEN '10-20%'
        WHEN Discount <= 0.30 THEN '20-30%'
        WHEN Discount <= 0.40 THEN '30-40%'
        ELSE '40-55%'
    END AS discount_band,

    SUM(Revenue) AS revenue,
    SUM(Profit) AS profit,
    SUM(Profit) / NULLIF(SUM(Revenue), 0) AS profit_margin,
    COUNT(DISTINCT Order_ID) AS orders

FROM sales_profitability

GROUP BY
    CASE
        WHEN Discount <= 0.05 THEN '0-5%'
        WHEN Discount <= 0.10 THEN '5-10%'
        WHEN Discount <= 0.20 THEN '10-20%'
        WHEN Discount <= 0.30 THEN '20-30%'
        WHEN Discount <= 0.40 THEN '30-40%'
        ELSE '40-55%'
    END;


SELECT
    Category,
    Subcategory,
    SUM(Revenue) AS revenue,
    SUM(Profit) AS profit,
    SUM(Profit) / NULLIF(SUM(Revenue), 0) AS profit_margin
FROM sales_profitability
GROUP BY
    Category,
    Subcategory
ORDER BY
    profit_margin DESC;


SELECT
    Channel,
    SUM(Revenue) AS revenue,
    SUM(Profit) AS profit,
    SUM(Profit) / NULLIF(SUM(Revenue), 0) AS profit_margin,
    AVG(Discount) AS avg_discount
FROM sales_profitability
GROUP BY Channel
ORDER BY profit DESC;



SELECT
    Region,
    SUM(Revenue) AS revenue,
    SUM(Profit) AS profit,
    SUM(Profit) / NULLIF(SUM(Revenue), 0) AS profit_margin
FROM sales_profitability
GROUP BY Region
ORDER BY profit DESC;
