import pandas as pd

# 1. Load datasets
customers = pd.read_csv("customer_details_70.csv")
sales = pd.read_csv("loyalty_rules.csv")

# 2. Convert date column
sales["transaction_date"] = pd.to_datetime(sales["transaction_date"])

# 3. Calculate RFM metrics
rfm = (
    sales
    .groupby("customer_id")
    .agg(
        frequency=("transaction_id", "count"),
        monetary=("total_amount", "sum"),
        last_purchase_date=("transaction_date", "max")
    )
    .reset_index()
)

# 4. Calculate recency
today = pd.to_datetime("2025-01-01")
rfm["recency_days"] = (today - rfm["last_purchase_date"]).dt.days

# 5. Join with loyalty data
customer_rfm = rfm.merge(
    customers[["customer_id", "total_loyalty_points"]],
    on="customer_id",
    how="left"
)

# 6. Customer segmentation
customer_rfm["segment"] = "Regular"

# High-Spenders (Top 10%)
monetary_threshold = customer_rfm["monetary"].quantile(0.90)
customer_rfm.loc[
    customer_rfm["monetary"] >= monetary_threshold,
    "segment"
] = "High-Spender"

# At-Risk customers
customer_rfm.loc[
    (customer_rfm["recency_days"] > 60) &
    (customer_rfm["total_loyalty_points"] > 0),
    "segment"
] = "At-Risk"

# 7. Save output
customer_rfm.to_csv("customer_segments.csv", index=False)

print("Customer segmentation completed successfully!")
