
import plotly.express as px

PAPER = "#fbf8f0"
INK = "#203c30"
TERRACOTTA = "#bd6848"
GOLD = "#c49a43"
OLIVE = "#858b72"


def style_chart(fig, height=320):
    fig.update_layout(
        height=height,
        paper_bgcolor=PAPER,
        plot_bgcolor=PAPER,
        font=dict(
            family="DM Sans, sans-serif",
            color=INK,
            size=12,
        ),
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#d8d1c3",
        zeroline=False,
    )

    fig.update_yaxes(
        gridcolor="#e4ded2",
        zeroline=False,
    )

    return fig


def revenue_trend(df):
    monthly = df.copy()
    monthly["month"] = (
        monthly["order_date"].dt.to_period("M").dt.to_timestamp()
    )

    monthly = (
        monthly.groupby("month", as_index=False)["sales"]
        .sum()
        .sort_values("month")
    )

    fig = px.line(
        monthly,
        x="month",
        y="sales",
        markers=True,
        labels={"month": "Month", "sales": "Revenue"},
    )

    fig.update_traces(
        line=dict(color=INK, width=3),
        marker=dict(size=8, color=TERRACOTTA),
        hovertemplate="%{x|%b %Y}<br>Revenue: $%{y:,.2f}<extra></extra>",
    )

    return style_chart(fig)


def top_products(df):
    products = (
        df.groupby("product", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=True)
        .tail(10)
    )

    fig = px.bar(
        products,
        x="sales",
        y="product",
        orientation="h",
        labels={"sales": "Revenue", "product": "Product"},
        color_discrete_sequence=[TERRACOTTA],
    )

    fig.update_traces(
        hovertemplate="%{y}<br>Revenue: $%{x:,.2f}<extra></extra>"
    )

    return style_chart(fig)


def sales_by_region(df):
    regions = (
        df.groupby("region", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    fig = px.pie(
        regions,
        names="region",
        values="sales",
        hole=0.58,
        color_discrete_sequence=[
            INK, TERRACOTTA, GOLD, OLIVE, "#b8b5a8"
        ],
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate="%{label}<br>$%{value:,.2f}<extra></extra>",
    )

    return style_chart(fig)


def sales_by_category(df):
    categories = (
        df.groupby("category", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    fig = px.bar(
        categories,
        x="category",
        y="sales",
        labels={"category": "Category", "sales": "Revenue"},
        color_discrete_sequence=[INK],
    )

    fig.update_traces(
        hovertemplate="%{x}<br>Revenue: $%{y:,.2f}<extra></extra>"
    )

    return style_chart(fig)
