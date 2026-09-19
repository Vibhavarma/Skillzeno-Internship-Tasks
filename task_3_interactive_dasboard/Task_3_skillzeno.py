import csv
import json
import webbrowser
from pathlib import Path

# -----------------------------
# 1. LOAD DATASET
# -----------------------------

csv_file = Path("Supermart Grocery Sales - Retail Analytics Dataset.csv")

with open(csv_file, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    data = list(reader)

columns = reader.fieldnames


# -----------------------------
# 2. FIND REQUIRED COLUMNS
# -----------------------------

def find_column(possible_names):
    for name in possible_names:
        for col in columns:
            if col.strip().lower() == name.lower():
                return col

    for name in possible_names:
        for col in columns:
            if name.lower() in col.lower():
                return col

    return None


sales_col = find_column(["Sales", "Sale", "Revenue"])
profit_col = find_column(["Profit"])
category_col = find_column(["Category"])
region_col = find_column(["Region"])
city_col = find_column(["City"])
order_col = find_column(["Order ID", "OrderID"])


def number(value):
    try:
        return float(
            str(value)
            .replace(",", "")
            .replace("₹", "")
            .strip()
        )
    except:
        return 0


# -----------------------------
# 3. PREPARE DATA FOR JAVASCRIPT
# -----------------------------

js_data = []

for row in data:
    js_data.append({
        "sales": number(row.get(sales_col, 0)),
        "profit": number(row.get(profit_col, 0)),
        "category": row.get(category_col, "Unknown"),
        "region": row.get(region_col, "Unknown"),
        "city": row.get(city_col, "Unknown"),
        "order": row.get(order_col, "")
    })

data_json = json.dumps(js_data)


# -----------------------------
# 4. CREATE DASHBOARD
# -----------------------------

html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>Supermart Grocery Sales Dashboard</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background: #f4f6f8;
    margin: 0;
    padding: 25px;
    color: #222;
}}

h1 {{
    text-align: center;
    margin-bottom: 5px;
}}

.subtitle {{
    text-align: center;
    color: #666;
    margin-bottom: 30px;
}}

.cards {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    margin-bottom: 25px;
}}

.card {{
    background: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 2px 8px #ddd;
}}

.card h3 {{
    color: #666;
    margin: 5px;
}}

.card p {{
    font-size: 24px;
    font-weight: bold;
    margin: 10px;
}}

.section {{
    background: white;
    padding: 22px;
    margin-bottom: 22px;
    border-radius: 12px;
    box-shadow: 0 2px 8px #ddd;
}}

.filters {{
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
}}

select {{
    padding: 10px;
    min-width: 180px;
    border-radius: 6px;
    border: 1px solid #bbb;
}}

.chart {{
    margin-top: 15px;
}}

.bar {{
    margin: 13px 0;
}}

.label {{
    font-weight: bold;
    margin-bottom: 5px;
}}

.bar-bg {{
    height: 25px;
    background: #e5e7eb;
    border-radius: 8px;
}}

.bar-fill {{
    height: 25px;
    background: #4f46e5;
    border-radius: 8px;
}}

.insight {{
    background: #f8fafc;
    padding: 14px;
    margin: 10px 0;
    border-left: 5px solid #4f46e5;
}}

@media(max-width:800px) {{
    .cards {{
        grid-template-columns: repeat(2, 1fr);
    }}
}}

</style>

</head>


<body>


<h1>Supermart Grocery Sales Dashboard</h1>

<div class="subtitle">
Interactive Retail Sales Analysis
</div>


<!-- KPI CARDS -->

<div class="cards">

<div class="card">
<h3>Total Sales</h3>
<p id="sales">₹0</p>
</div>

<div class="card">
<h3>Total Profit</h3>
<p id="profit">₹0</p>
</div>

<div class="card">
<h3>Total Orders</h3>
<p id="orders">0</p>
</div>

<div class="card">
<h3>Average Sales</h3>
<p id="average">₹0</p>
</div>

</div>


<!-- FILTERS -->

<div class="section">

<h2>Filters</h2>

<div class="filters">

<select id="categoryFilter" onchange="updateDashboard()">
<option value="All">All Categories</option>
</select>

<select id="regionFilter" onchange="updateDashboard()">
<option value="All">All Regions</option>
</select>

</div>

<p id="filterText">
Showing all data
</p>

</div>


<!-- SALES BY CATEGORY -->

<div class="section">

<h2>Sales by Category</h2>

<div id="categoryChart" class="chart"></div>

</div>


<!-- PROFIT BY CATEGORY -->

<div class="section">

<h2>Profit by Category</h2>

<div id="profitCategoryChart" class="chart"></div>

</div>


<!-- SALES BY REGION -->

<div class="section">

<h2>Sales by Region</h2>

<div id="regionChart" class="chart"></div>

</div>


<!-- TOP CITIES -->

<div class="section">

<h2>Top Cities by Sales</h2>

<div id="cityChart" class="chart"></div>

</div>


<!-- INSIGHTS -->

<div class="section">

<h2>Major Insights</h2>

<div id="insights"></div>

</div>


<script>


const allData = {data_json};


// ---------------------------------
// CREATE FILTER OPTIONS
// ---------------------------------

const categories = [
    ...new Set(allData.map(row => row.category))
];

const regions = [
    ...new Set(allData.map(row => row.region))
];


categories.forEach(category => {{

    const option = document.createElement("option");

    option.value = category;
    option.textContent = category;

    document.getElementById("categoryFilter")
        .appendChild(option);

}});


regions.forEach(region => {{

    const option = document.createElement("option");

    option.value = region;
    option.textContent = region;

    document.getElementById("regionFilter")
        .appendChild(option);

}});


// ---------------------------------
// FORMAT NUMBER
// ---------------------------------

function money(value) {{

    return "₹" + value.toLocaleString(
        "en-IN",
        {{
            maximumFractionDigits: 2
        }}
    );

}}


// ---------------------------------
// DRAW BAR CHART
// ---------------------------------

function drawChart(data, elementId) {{

    const container =
        document.getElementById(elementId);

    container.innerHTML = "";

    const entries =
        Object.entries(data);

    if (entries.length === 0) {{

        container.innerHTML =
            "<p>No data available.</p>";

        return;

    }}

    const maxValue = Math.max(
        ...entries.map(item => Math.abs(item[1])),
        1
    );


    entries.forEach(([name, value]) => {{

        const width =
            Math.abs(value) / maxValue * 100;


        container.innerHTML += `

        <div class="bar">

            <div class="label">

                ${{name}} —
                ${{money(value)}}

            </div>

            <div class="bar-bg">

                <div
                    class="bar-fill"
                    style="width:${{width}}%">
                </div>

            </div>

        </div>

        `;

    }});

}}


// ---------------------------------
// UPDATE DASHBOARD
// ---------------------------------

function updateDashboard() {{

    const selectedCategory =
        document.getElementById(
            "categoryFilter"
        ).value;


    const selectedRegion =
        document.getElementById(
            "regionFilter"
        ).value;


    // FILTER DATA

    const filteredData =
        allData.filter(row =>

            (selectedCategory === "All" ||
             row.category === selectedCategory)

            &&

            (selectedRegion === "All" ||
             row.region === selectedRegion)

        );


    // -----------------------------
    // KPI CALCULATIONS
    // -----------------------------

    let totalSales = 0;
    let totalProfit = 0;

    const orders = new Set();


    filteredData.forEach(row => {{

        totalSales += row.sales;

        totalProfit += row.profit;

        if (row.order) {{
            orders.add(row.order);
        }}

    }});


    const totalOrders =
        orders.size || filteredData.length;


    const averageSales =
        filteredData.length > 0
        ? totalSales / filteredData.length
        : 0;


    document.getElementById("sales")
        .textContent = money(totalSales);


    document.getElementById("profit")
        .textContent = money(totalProfit);


    document.getElementById("orders")
        .textContent =
        totalOrders.toLocaleString();


    document.getElementById("average")
        .textContent = money(averageSales);


    // -----------------------------
    // CATEGORY SALES
    // -----------------------------

    const categorySales = {{}};

    filteredData.forEach(row => {{

        if (!categorySales[row.category]) {{
            categorySales[row.category] = 0;
        }}

        categorySales[row.category] += row.sales;

    }});


    drawChart(
        categorySales,
        "categoryChart"
    );


    // -----------------------------
    // CATEGORY PROFIT
    // -----------------------------

    const categoryProfit = {{}};

    filteredData.forEach(row => {{

        if (!categoryProfit[row.category]) {{
            categoryProfit[row.category] = 0;
        }}

        categoryProfit[row.category] += row.profit;

    }});


    drawChart(
        categoryProfit,
        "profitCategoryChart"
    );


    // -----------------------------
    // REGION SALES
    // -----------------------------

    const regionSales = {{}};

    filteredData.forEach(row => {{

        if (!regionSales[row.region]) {{
            regionSales[row.region] = 0;
        }}

        regionSales[row.region] += row.sales;

    }});


    drawChart(
        regionSales,
        "regionChart"
    );


    // -----------------------------
    // CITY SALES
    // -----------------------------

    const citySales = {{}};

    filteredData.forEach(row => {{

        if (!citySales[row.city]) {{
            citySales[row.city] = 0;
        }}

        citySales[row.city] += row.sales;

    }});


    const topCities =
        Object.fromEntries(

            Object.entries(citySales)
            .sort((a,b) => b[1] - a[1])
            .slice(0, 10)

        );


    drawChart(
        topCities,
        "cityChart"
    );


    // -----------------------------
    // FILTER TEXT
    // -----------------------------

    document.getElementById("filterText")
        .textContent =
        "Showing " +
        filteredData.length.toLocaleString() +
        " records";


    // -----------------------------
    // INSIGHTS
    // -----------------------------

    let highestCategory = "-";
    let highestCategorySales = 0;


    Object.entries(categorySales)
    .forEach(([name, value]) => {{

        if (value > highestCategorySales) {{

            highestCategorySales = value;
            highestCategory = name;

        }}

    }});


    let highestRegion = "-";
    let highestRegionSales = 0;


    Object.entries(regionSales)
    .forEach(([name, value]) => {{

        if (value > highestRegionSales) {{

            highestRegionSales = value;
            highestRegion = name;

        }}

    }});


    document.getElementById("insights")
        .innerHTML = `

        <div class="insight">

        <b>Sales Insight:</b>
        ${{highestCategory}}
        is the highest-sales category
        in the current selection.

        </div>


        <div class="insight">

        <b>Regional Insight:</b>
        ${{highestRegion}}
        has the highest sales contribution
        in the current selection.

        </div>


        <div class="insight">

        <b>Profit Insight:</b>
        Total profit for the current selection
        is ${{money(totalProfit)}}.

        </div>

        `;

}}


// INITIAL DASHBOARD

updateDashboard();

</script>


</body>

</html>
"""


# ---------------------------------
# SAVE HTML
# ---------------------------------

output_file = Path("dashboard.html")

output_file.write_text(
    html,
    encoding="utf-8"
)


print("Dashboard created successfully!")

print("Opening dashboard in browser...")


webbrowser.open(
    output_file.resolve().as_uri()
)