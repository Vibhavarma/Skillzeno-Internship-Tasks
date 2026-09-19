import csv
import json
import webbrowser
from pathlib import Path
from collections import defaultdict

# ============================================================
# TASK 4 - BUSINESS ANALYTICS REPORT
# ============================================================

BASE_DIR = Path(__file__).parent

CSV_FILE = BASE_DIR / "Supermart Grocery Sales - Retail Analytics Dataset.csv"
OUTPUT_FILE = BASE_DIR / "business_analytics_report.html"


# ------------------------------------------------------------
# 1. READ CSV DATA
# ------------------------------------------------------------

if not CSV_FILE.exists():
    print("Dataset file not found!")
    print("Make sure the CSV file is inside the Task_4_Business_Analytics folder.")
    input("Press Enter to exit...")
    raise SystemExit

with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

if not rows:
    print("No data found in the CSV file.")
    input("Press Enter to exit...")
    raise SystemExit


# ------------------------------------------------------------
# 2. FIND IMPORTANT COLUMNS
# ------------------------------------------------------------

def find_column(possible_names):
    for column in rows[0].keys():
        clean = column.strip().lower().replace(" ", "").replace("_", "")
        for name in possible_names:
            target = name.lower().replace(" ", "").replace("_", "")
            if clean == target:
                return column
    return None


sales_col = find_column(["sales", "sale"])
profit_col = find_column(["profit"])
category_col = find_column(["category"])
region_col = find_column(["region"])
city_col = find_column(["city"])
order_col = find_column(["orderid", "order id", "order"])


# ------------------------------------------------------------
# 3. CONVERT NUMERIC VALUES
# ------------------------------------------------------------

def number(value):
    try:
        value = str(value).replace(",", "").replace("₹", "").strip()
        return float(value)
    except:
        return 0.0


for row in rows:
    row["_sales"] = number(row.get(sales_col, 0)) if sales_col else 0
    row["_profit"] = number(row.get(profit_col, 0)) if profit_col else 0


# ------------------------------------------------------------
# 4. BASIC KPIs
# ------------------------------------------------------------

total_sales = sum(row["_sales"] for row in rows)
total_profit = sum(row["_profit"] for row in rows)

if order_col:
    unique_orders = set(
        str(row.get(order_col, "")).strip()
        for row in rows
        if str(row.get(order_col, "")).strip()
    )
    total_orders = len(unique_orders)
else:
    total_orders = len(rows)

average_sales = total_sales / total_orders if total_orders else 0
profit_margin = (total_profit / total_sales * 100) if total_sales else 0


# ------------------------------------------------------------
# 5. CATEGORY ANALYSIS
# ------------------------------------------------------------

category_sales = defaultdict(float)
category_profit = defaultdict(float)

for row in rows:
    category = str(row.get(category_col, "Unknown")).strip() if category_col else "Unknown"
    if not category:
        category = "Unknown"

    category_sales[category] += row["_sales"]
    category_profit[category] += row["_profit"]


# ------------------------------------------------------------
# 6. REGION ANALYSIS
# ------------------------------------------------------------

region_sales = defaultdict(float)
region_profit = defaultdict(float)

for row in rows:
    region = str(row.get(region_col, "Unknown")).strip() if region_col else "Unknown"
    if not region:
        region = "Unknown"

    region_sales[region] += row["_sales"]
    region_profit[region] += row["_profit"]


# ------------------------------------------------------------
# 7. CITY ANALYSIS
# ------------------------------------------------------------

city_sales = defaultdict(float)

for row in rows:
    city = str(row.get(city_col, "Unknown")).strip() if city_col else "Unknown"
    if not city:
        city = "Unknown"

    city_sales[city] += row["_sales"]


# ------------------------------------------------------------
# 8. FIND TOP PERFORMERS
# ------------------------------------------------------------

top_category = max(category_sales, key=category_sales.get) if category_sales else "N/A"
top_category_sales = category_sales.get(top_category, 0)

top_profit_category = (
    max(category_profit, key=category_profit.get)
    if category_profit else "N/A"
)

top_region = max(region_sales, key=region_sales.get) if region_sales else "N/A"
top_region_sales = region_sales.get(top_region, 0)

top_city = max(city_sales, key=city_sales.get) if city_sales else "N/A"
top_city_sales = city_sales.get(top_city, 0)


# ------------------------------------------------------------
# 9. LOW PERFORMERS
# ------------------------------------------------------------

lowest_category = (
    min(category_sales, key=category_sales.get)
    if category_sales else "N/A"
)

lowest_region = (
    min(region_sales, key=region_sales.get)
    if region_sales else "N/A"
)


# ------------------------------------------------------------
# 10. SORT DATA FOR CHARTS
# ------------------------------------------------------------

category_labels = list(category_sales.keys())
category_sales_values = [category_sales[x] for x in category_labels]
category_profit_values = [category_profit[x] for x in category_labels]

region_labels = list(region_sales.keys())
region_sales_values = [region_sales[x] for x in region_labels]
region_profit_values = [region_profit[x] for x in region_labels]

top_cities_sorted = sorted(
    city_sales.items(),
    key=lambda x: x[1],
    reverse=True
)[:10]

city_labels = [x[0] for x in top_cities_sorted]
city_values = [x[1] for x in top_cities_sorted]


# ------------------------------------------------------------
# 11. BUSINESS RECOMMENDATIONS
# ------------------------------------------------------------

recommendations = [
    f"Focus on the {top_category} category because it generates the highest sales among the analyzed categories.",
    f"Continue strengthening sales performance in the {top_region} region, which records the highest regional sales.",
    f"Review the performance of the {lowest_category} category to identify opportunities for pricing, promotion or product-mix improvement.",
    f"Use the performance of {top_city} as a reference when planning sales strategies for other cities.",
    f"Monitor profitability along with sales so that growth decisions consider both revenue and profit."
]


# ------------------------------------------------------------
# 12. FORMAT FUNCTIONS
# ------------------------------------------------------------

def money(value):
    return "₹{:,.2f}".format(value)


def json_data(value):
    return json.dumps(value)


# ------------------------------------------------------------
# 13. CREATE HTML REPORT
# ------------------------------------------------------------

html = f"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Task 4 - Business Analytics Report</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f6f8;
    color: #222;
}}

.header {{
    background: #1f2937;
    color: white;
    padding: 28px;
    text-align: center;
}}

.header h1 {{
    margin: 0 0 8px 0;
}}

.header p {{
    margin: 0;
    opacity: 0.9;
}}

.container {{
    width: 92%;
    max-width: 1200px;
    margin: 25px auto;
}}

.kpis {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    margin-bottom: 25px;
}}

.card {{
    background: white;
    border-radius: 12px;
    padding: 22px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}}

.kpi-title {{
    font-size: 14px;
    color: #666;
    margin-bottom: 8px;
}}

.kpi-value {{
    font-size: 25px;
    font-weight: bold;
}}

.section {{
    background: white;
    padding: 24px;
    border-radius: 12px;
    margin-bottom: 22px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.06);
}}

.section h2 {{
    margin-top: 0;
}}

.grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 22px;
}}

.insight {{
    padding: 13px;
    margin: 9px 0;
    background: #f7f7f7;
    border-left: 4px solid #444;
    border-radius: 5px;
}}

.recommendation {{
    padding: 14px;
    margin: 10px 0;
    background: #f7f7f7;
    border-radius: 6px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    padding: 10px;
    border-bottom: 1px solid #ddd;
    text-align: left;
}}

th {{
    background: #f0f0f0;
}}

.chart {{
    width: 100%;
    overflow-x: auto;
}}

.bar-row {{
    display: flex;
    align-items: center;
    margin: 12px 0;
}}

.bar-label {{
    width: 140px;
    font-size: 14px;
}}

.bar-container {{
    flex: 1;
    background: #e5e7eb;
    height: 25px;
    border-radius: 5px;
    overflow: hidden;
}}

.bar {{
    height: 100%;
    background: #374151;
}}

.bar-value {{
    width: 110px;
    text-align: right;
    font-size: 13px;
    margin-left: 10px;
}}

.footer {{
    text-align: center;
    padding: 25px;
    color: #666;
}}

@media (max-width: 800px) {{
    .kpis {{
        grid-template-columns: 1fr 1fr;
    }}

    .grid {{
        grid-template-columns: 1fr;
    }}
}}

</style>

</head>

<body>

<div class="header">

<h1>Business Analytics Report</h1>

<p>Supermart Grocery Sales Analysis | Skillzeno Internship - Task 4</p>

</div>


<div class="container">


<div class="kpis">

<div class="card">
<div class="kpi-title">Total Sales</div>
<div class="kpi-value">{money(total_sales)}</div>
</div>

<div class="card">
<div class="kpi-title">Total Profit</div>
<div class="kpi-value">{money(total_profit)}</div>
</div>

<div class="card">
<div class="kpi-title">Total Orders</div>
<div class="kpi-value">{total_orders:,}</div>
</div>

<div class="card">
<div class="kpi-title">Profit Margin</div>
<div class="kpi-value">{profit_margin:.2f}%</div>
</div>

</div>


<div class="section">

<h2>1. Business Problem</h2>

<p>
The objective of this analysis is to understand supermarket sales and
profitability performance across product categories, regions and cities.
The analysis aims to identify important business patterns and provide
data-backed recommendations that can support better sales and business
decisions.
</p>

</div>


<div class="grid">


<div class="section">

<h2>2. Category Performance</h2>

<p><b>Top Sales Category:</b> {top_category}</p>

<p><b>Highest Profit Category:</b> {top_profit_category}</p>

<p><b>Lowest Sales Category:</b> {lowest_category}</p>

</div>


<div class="section">

<h2>3. Regional Performance</h2>

<p><b>Top Region by Sales:</b> {top_region}</p>

<p><b>Highest Regional Sales:</b> {money(top_region_sales)}</p>

<p><b>Lowest Sales Region:</b> {lowest_region}</p>

</div>

</div>


<div class="section">

<h2>4. Sales by Category</h2>

<div class="chart">

"""

# Category bars
max_category_value = max(category_sales_values) if category_sales_values else 1

for label, value in zip(category_labels, category_sales_values):

    width = (value / max_category_value) * 100

    html += f"""
    <div class="bar-row">
        <div class="bar-label">{label}</div>
        <div class="bar-container">
            <div class="bar" style="width:{width:.2f}%"></div>
        </div>
        <div class="bar-value">{money(value)}</div>
    </div>
    """


html += """

</div>

</div>


<div class="section">

<h2>5. Profit by Category</h2>

<table>

<tr>
<th>Category</th>
<th>Sales</th>
<th>Profit</th>
</tr>

"""


for category in category_labels:

    html += f"""
    <tr>
        <td>{category}</td>
        <td>{money(category_sales[category])}</td>
        <td>{money(category_profit[category])}</td>
    </tr>
    """


html += """

</table>

</div>


<div class="section">

<h2>6. Sales by Region</h2>

<div class="chart">

"""


max_region_value = max(region_sales_values) if region_sales_values else 1

for label, value in zip(region_labels, region_sales_values):

    width = (value / max_region_value) * 100

    html += f"""
    <div class="bar-row">
        <div class="bar-label">{label}</div>
        <div class="bar-container">
            <div class="bar" style="width:{width:.2f}%"></div>
        </div>
        <div class="bar-value">{money(value)}</div>
    </div>
    """


html += """

</div>

</div>


<div class="section">

<h2>7. Top Cities by Sales</h2>

<table>

<tr>
<th>Rank</th>
<th>City</th>
<th>Sales</th>
</tr>

"""


for index, (city, value) in enumerate(top_cities_sorted, start=1):

    html += f"""
    <tr>
        <td>{index}</td>
        <td>{city}</td>
        <td>{money(value)}</td>
    </tr>
    """


html += """

</table>

</div>


<div class="section">

<h2>8. Key Business Insights</h2>

<div class="insight">
The overall business generated <b>""" + money(total_sales) + """</b>
in sales with total profit of <b>""" + money(total_profit) + """</b>.
</div>

<div class="insight">
The <b>""" + top_category + """</b> category generated the highest sales
among the analyzed categories.
</div>

<div class="insight">
The <b>""" + top_region + """</b> region recorded the highest sales
among the analyzed regions.
</div>

<div class="insight">
The city with the highest sales was <b>""" + top_city + """</b>,
with sales of <b>""" + money(top_city_sales) + """</b>.
</div>

<div class="insight">
The overall profit margin was approximately
<b>""" + f"{profit_margin:.2f}%" + """</b>.
</div>

</div>


<div class="section">

<h2>9. Data-Backed Recommendations</h2>

"""


for recommendation in recommendations:

    html += f"""
    <div class="recommendation">
        • {recommendation}
    </div>
    """


html += """

</div>


<div class="section">

<h2>10. Conclusion</h2>

<p>
The analysis provides a structured view of supermarket sales and
profitability performance. By examining categories, regions and cities,
the business can identify areas of strong performance and areas that
require further attention. The findings can support decisions related
to product focus, regional strategy, promotions and performance
monitoring.
</p>

</div>


<div class="footer">

<p>Created for Skillzeno Internship – Task 4</p>

</div>


</div>

</body>

</html>
"""


# ------------------------------------------------------------
# 14. SAVE REPORT
# ------------------------------------------------------------

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write(html)


print()
print("=" * 55)
print("TASK 4 BUSINESS ANALYTICS REPORT CREATED")
print("=" * 55)
print()
print("Dataset rows:", len(rows))
print("Total Sales:", money(total_sales))
print("Total Profit:", money(total_profit))
print("Total Orders:", total_orders)
print("Profit Margin:", f"{profit_margin:.2f}%")
print()
print("Report saved as:")
print(OUTPUT_FILE)
print()

# Open report in browser
webbrowser.open(OUTPUT_FILE.resolve().as_uri())

input("Press Enter to exit...")