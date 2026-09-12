import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"C:\Users\vibha\Downloads\Supermart Grocery Sales - Retail Analytics Dataset.csv")
print(df.head())
print(df.info())
print(df.isnull().sum())
print(df.duplicated().sum())
print(df.columns)
print(df.describe())
print(df.groupby("Category")["Sales"].sum())
print(df.groupby("Category")["Profit"].sum())
print(df.groupby("Region")["Sales"].sum())
df["Order Date"] = pd.to_datetime(df["Order Date"], format="mixed")
monthly_sales = df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum()
print(monthly_sales)
category_sales = df.groupby("Category")["Sales"].sum()

category_sales.plot(kind="bar")
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.show()
category_profit = df.groupby("Category")["Profit"].sum()

category_profit.plot(kind="bar")
plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Total Profit")
plt.tight_layout()
plt.show()
# Region-wise Sales
region_sales = df.groupby("Region")["Sales"].sum()

print(region_sales)

plt.figure(figsize=(8,5))
region_sales.plot(kind="bar")
plt.title("Region-wise Sales")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
# Region-wise Profit
region_profit = df.groupby("Region")["Profit"].sum()

print(region_profit)

plt.figure(figsize=(8,5))
region_profit.plot(kind="bar")
plt.title("Region-wise Profit")
plt.xlabel("Region")
plt.ylabel("Total Profit")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
# Discount Analysis
discount_profit = df.groupby("Discount")["Profit"].mean()

print(discount_profit)

plt.figure(figsize=(8,5))
discount_profit.plot(kind="bar")
plt.title("Average Profit by Discount")
plt.xlabel("Discount")
plt.ylabel("Average Profit")
plt.tight_layout()
plt.show()
# Sales vs Profit
plt.figure(figsize=(8,5))
plt.scatter(df["Sales"], df["Profit"])
plt.title("Sales vs Profit")
plt.xlabel("Sales")
plt.ylabel("Profit")
plt.tight_layout()
plt.show()
# Top 10 Cities by Sales
city_sales = df.groupby("City")["Sales"].sum().sort_values(ascending=False).head(10)

print(city_sales)

plt.figure(figsize=(10,5))
city_sales.plot(kind="bar")
plt.title("Top 10 Cities by Sales")
plt.xlabel("City")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# Key Insights
print("\n--- Key Insights ---")

print("Highest Sales Category:",
      df.groupby("Category")["Sales"].sum().idxmax())

print("Highest Profit Category:",
      df.groupby("Category")["Profit"].sum().idxmax())

print("Highest Sales Region:",
      df.groupby("Region")["Sales"].sum().idxmax())

print("Highest Sales City:",
      df.groupby("City")["Sales"].sum().idxmax())

print("Average Sales:", df["Sales"].mean())
print("Average Profit:", df["Profit"].mean())