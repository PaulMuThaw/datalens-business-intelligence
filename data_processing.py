
import pandas as pd

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "product",
    "category",
    "region",
    "quantity",
    "unit_price",
]


def clean_sales_data(uploaded_file):
    """Read, validate and clean sales data."""

    # Accept a DataFrame or an uploaded CSV file.
    if isinstance(uploaded_file, pd.DataFrame):
        df = uploaded_file.copy()
    else:
        df = pd.read_csv(uploaded_file)

    # Standardise column names.
    df.columns = df.columns.str.strip().str.lower()

    # Check required columns.
    missing = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing)
        )

    # Convert columns to the correct data types.
    df["order_date"] = pd.to_datetime(
        df["order_date"], errors="coerce"
    )
    df["quantity"] = pd.to_numeric(
        df["quantity"], errors="coerce"
    )
    df["unit_price"] = pd.to_numeric(
        df["unit_price"], errors="coerce"
    )

    # Handle discounts.
    if "discount" in df.columns:
        df["discount"] = pd.to_numeric(
            df["discount"], errors="coerce"
        ).fillna(0)
    else:
        df["discount"] = 0.0

    # Remove rows with missing required values.
    df = df.dropna(subset=REQUIRED_COLUMNS)

    # Remove invalid quantities, prices and discounts.
    df = df[
        (df["quantity"] > 0)
        & (df["unit_price"] >= 0)
        & (df["discount"] >= 0)
        & (df["discount"] <= 1)
    ].copy()

    if df.empty:
        raise ValueError(
            "No valid sales records were found in this CSV."
        )

    # Calculate revenue after discount.
    df["sales"] = (
        df["quantity"]
        * df["unit_price"]
        * (1 - df["discount"])
    ).round(2)

    return df


def calculate_kpis(df):
    """Calculate the main dashboard figures."""

    total_revenue = df["sales"].sum()
    total_orders = df["order_id"].nunique()
    units_sold = df["quantity"].sum()

    average_order_value = (
        total_revenue / total_orders
        if total_orders else 0
    )

    return {
        "revenue": total_revenue,
        "orders": total_orders,
        "units": units_sold,
        "average_order_value": average_order_value,
    }
