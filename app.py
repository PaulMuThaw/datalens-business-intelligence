
from pathlib import Path

import pandas as pd
import streamlit as st

from data_processing import clean_sales_data, calculate_kpis
from charts import (
    revenue_trend,
    top_products,
    sales_by_region,
    sales_by_category,
)

st.set_page_config(
    page_title="DataLens | Sales Analytics",
    page_icon="D",
    layout="wide",
)

# Load the custom design.
css_path = Path(__file__).parent / "styles.css"

if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


# Sidebar
with st.sidebar:
    st.markdown(
        "<h1 style='font-size:2.2rem'>DataLens</h1>",
        unsafe_allow_html=True,
    )
    st.caption("SALES ANALYTICS")
    st.divider()

    st.markdown("### Your workspace")
    st.write("A clearer view of your business.")

    uploaded_file = st.file_uploader(
        "Upload sales CSV",
        type=["csv"],
        help="Upload a CSV containing your sales records.",
    )

    st.divider()
    st.caption("DATA TO DECISIONS")
    st.caption("Version 1.0 · Portfolio Project")


# Page heading
st.markdown(
    '<p class="eyebrow">BUSINESS INTELLIGENCE TOOLKIT</p>',
    unsafe_allow_html=True,
)
st.title("Sales overview")
st.markdown(
    '<p class="subtitle">Understand performance, '
    'spot trends, and explore your sales data.</p>',
    unsafe_allow_html=True,
)


# Load uploaded data or provide sample data.
if uploaded_file is not None:
    try:
        df = clean_sales_data(uploaded_file)
        st.success("Your CSV was loaded and validated.")
    except (ValueError, pd.errors.ParserError, UnicodeDecodeError) as error:
        st.error(f"Could not process this CSV: {error}")
        st.stop()
else:
    st.info(
        "Upload a CSV in the sidebar to analyse your own sales. "
        "A small demonstration dataset is shown below until then."
    )

    sample = {
        "order_id": [
            "A001", "A002", "A003", "A004", "A005", "A006",
            "A007", "A008", "A009", "A010", "A011", "A012",
        ],
        "order_date": [
            "2026-01-05", "2026-01-12", "2026-01-18",
            "2026-02-03", "2026-02-11", "2026-02-19",
            "2026-03-04", "2026-03-10", "2026-03-21",
            "2026-04-02", "2026-04-14", "2026-04-25",
        ],
        "product": [
            "Laptop", "Mouse", "Keyboard", "Monitor",
            "Laptop", "Headphones", "Mouse", "Monitor",
            "Keyboard", "Laptop", "Webcam", "Headphones",
        ],
        "category": [
            "Computers", "Accessories", "Accessories", "Displays",
            "Computers", "Audio", "Accessories", "Displays",
            "Accessories", "Computers", "Accessories", "Audio",
        ],
        "region": [
            "North", "South", "East", "West", "East", "South",
            "North", "West", "South", "North", "West", "East",
        ],
        "quantity": [1, 3, 2, 1, 1, 2, 5, 2, 3, 2, 2, 1],
        "unit_price": [900, 25, 45, 220, 950, 80, 25, 210, 45, 900, 60, 85],
        "discount": [0.05, 0, 0.10, 0.05, 0.10, 0, 0.10, 0.05, 0, 0.05, 0.10, 0.05],
    }

    df = clean_sales_data(pd.DataFrame(sample))


# Filters
st.markdown("### Explore your data")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    start_date = st.date_input(
        "From",
        value=df["order_date"].min().date(),
        key="start_date",
    )

with filter_col2:
    end_date = st.date_input(
        "To",
        value=df["order_date"].max().date(),
        key="end_date",
    )

with filter_col3:
    regions = sorted(df["region"].dropna().unique().tolist())
    selected_regions = st.multiselect(
        "Regions",
        options=regions,
        default=regions,
    )

categories = sorted(df["category"].dropna().unique().tolist())
selected_categories = st.multiselect(
    "Categories",
    options=categories,
    default=categories,
)

if start_date > end_date:
    st.error("'From' date must be on or before 'To' date.")
    st.stop()

filtered = df[
    (df["order_date"].dt.date >= start_date)
    & (df["order_date"].dt.date <= end_date)
    & (df["region"].isin(selected_regions))
    & (df["category"].isin(selected_categories))
].copy()


# KPI cards
kpis = calculate_kpis(filtered)

st.markdown("### Performance at a glance")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total revenue", f"${kpis['revenue']:,.2f}")
k2.metric("Total orders", f"{kpis['orders']:,}")
k3.metric("Units sold", f"{kpis['units']:,.0f}")
k4.metric("Average order value", f"${kpis['average_order_value']:,.2f}")

st.caption(
    "Revenue is calculated after discounts. "
    "Average order value = revenue ÷ unique order IDs."
)


if filtered.empty:
    st.warning("No records match your filters. Try a wider date range.")
else:
    # Main charts
    left, right = st.columns([1.25, 1])

    with left:
        st.markdown("### Revenue trend")
        st.plotly_chart(
            revenue_trend(filtered),
            use_container_width=True,
        )

    with right:
        st.markdown("### Top products")
        st.plotly_chart(
            top_products(filtered),
            use_container_width=True,
        )

    # Secondary charts
    left, right = st.columns(2)

    with left:
        st.markdown("### Sales by region")
        st.plotly_chart(
            sales_by_region(filtered),
            use_container_width=True,
        )

    with right:
        st.markdown("### Sales by category")
        st.plotly_chart(
            sales_by_category(filtered),
            use_container_width=True,
        )

    # Automatic summary
    best_product = (
        filtered.groupby("product")["sales"].sum().idxmax()
    )
    best_region = (
        filtered.groupby("region")["sales"].sum().idxmax()
    )

    st.markdown("### Notes from the numbers")
    st.markdown(
        f"""
        <div class="insight-note">
        <strong>Leading product:</strong> {best_product}<br>
        <strong>Leading region:</strong> {best_region}<br>
        <strong>Records analysed:</strong> {len(filtered):,}<br>
        These results describe the selected data and filters.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Data table and download
    st.markdown("### Sales records")
    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
    )

    csv_bytes = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download filtered CSV",
        data=csv_bytes,
        file_name="datalens_filtered_sales.csv",
        mime="text/csv",
    )
