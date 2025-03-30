import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on March 17th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")

# My additions

# 1. Add drop down for Category
selected_category = st.selectbox("Select a Category", df["Category"].unique())

# 2. Add a multi-select for Sub_Category within the selected_category
subcategories = df[df["Category"] == selected_category]["Sub_Category"].unique()
selected_subcategories = st.multiselect("Select Sub_Category", subcategories)

# Filter data based on selections
if selected_subcategories:
    df_selected = df[(df["Category"] == selected_category) & (df["Sub_Category"].isin(selected_subcategories))]
else:
    df_selected = df[df["Category"] == selected_category]

# 3. Show a line chart of sales for the selected items
# Reset index in case Order_Date is set as the index for grouping
df_selected_reset = df_selected_reset_index()
sales_over_time = df_selected_reset.groupby("Order_Date")["Sales"].sum().reset_index()
st.line_chart(sales_over_time, x="Order_Date", y="Sales")

# 4. Show three metrics dor the selected items: total sales, total profit, overall profit margin (%)
total_sales = df_selected["Sales"].sum()
total_profit = df_selected["Profit"].sum()
profit_margin = total_profit / total_sales if total_sales != 0 else 0

# 5. Use the delta option, comparing the selected profit margin and overall avg profit margin
overall_sales = df["Sales"].sum()
overall_profit = df["Profit"].sum()
overall_profit_margin = overall_profit / overall_sales if overall_sales != 0 else 0
delta_margin = profit_margin - overall_profit_margin

# Display metrics in three columns
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:, .2f}")
col2.metric("Total Profit", f"${total_profit:, .2f}")
col3.metric("Profit Margin", f"{profit_margin:.2%}", delta=f"{delta_margin:.2%}")
