# DataLens — Business Intelligence Toolkit

A Python-based sales analytics dashboard that transforms raw sales data into clear, interactive business insights.

## Overview

DataLens helps users explore sales performance through key performance indicators, interactive charts, data filtering, and CSV exports.

## Features

- Upload and analyse CSV sales data
- Validate required columns and clean invalid records
- Calculate revenue, order count, units sold, and average order value
- Explore monthly revenue trends
- Compare products, categories, and regions
- Filter results by date, region, and category
- Download filtered sales data as a CSV file
- Responsive dashboard with a custom editorial-inspired design

## Technology Stack

- Python
- Streamlit
- Pandas
- Plotly
- Git and GitHub

## Project Structure

- `app.py` — dashboard and user interface
- `data_processing.py` — data validation, cleaning, and KPI calculations
- `charts.py` — interactive charts
- `styles.css` — custom styling
- `.streamlit/config.toml` — application theme
- `requirements.txt` — Python dependencies

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/datalens-business-intelligence.git
cd datalens-business-intelligence
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

## Expected CSV Columns

The dataset should include:

`order_id`, `order_date`, `product`, `category`, `region`, `quantity`, and `unit_price`.

An optional `discount` column accepts decimal values, such as `0.10` for a 10% discount.

Revenue is calculated as quantity multiplied by unit price after discount. Revenue is not the same as profit.

## Data Privacy

Use fictional or appropriately anonymised sales records. Do not upload confidential business data.

## Future Improvements

- Automated data-quality reports
- Unit testing with pytest
- Sales growth comparisons
- Forecasting and trend analysis
- Deployment as a public web application

## Author

Developed as a portfolio project to demonstrate Python programming, data processing, data visualisation, and dashboard development.
