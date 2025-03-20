import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import json
import requests

# Page Layout
st.set_page_config(layout="wide")

##FFD7BE
# Custom CSS for Font Styling and Background Color
st.markdown("""
    <style>
        /* Background Color */
        .stApp {
            background-color: #E8FCCF !important;
        }

        /* Sidebar (Navigation Bar) Background */
        [data-testid="stSidebar"] {
            background-color: #FFD7BE !important; /* Light Grey */
        }
        
        /* Sidebar (Navigation Bar) Font Styling */
        [data-testid="stSidebar"] h1 {
            font-size: 40px !important;
            font-family: 'Times New Roman', serif !important;
            font-weight: bold !important;
            text-decoration: none !important; /* ❌ Removes underline */
        }

        /* Font Styling */
        h1 {
            font-size: 48px !important; 
            font-family: 'Times New Roman', serif !important;
            font-weight: bold; 
            text-decoration: underline;
        }
        h2 {
            font-size: 45px !important; 
            font-family: 'Times New Roman', serif !important; 
            font-weight: bold; 
            font-style: italic;
        }
        h3 {
            font-size: 42px !important; 
            font-family: 'Times New Roman', serif !important; 
            font-weight: bold;
        }
        p {
            font-size: 22px !important; 
            font-family: 'Times New Roman', serif !important;
        }
    </style>
""", unsafe_allow_html=True)



# Load dataset
def load_data():
    df = pd.read_csv("dairy_dataset.csv")  # Ensure the uploaded file name matches
    return df

df = load_data()

# Sidebar Navigation
#st.sidebar.title(" ☰")

with st.sidebar:
    selected_page = option_menu(
        menu_title="☰ Navigation Bar",  # Hide default title
        options=["Overview", "Sales", "Inventory", "Customer Demand"],
        icons=["lightbulb", "cash", "box", "graph-up-arrow"],  # Optional icons
        #menu_icon="cast",  # Sidebar icon
        default_index=0,  # Default selected option
        styles={
            "container": {"padding": "0!important", "background-color": "#FFD7BE"},
            "icon": {"color": "black", "font-size": "22px"},
            "nav-link": {"font-size": "22px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "143D60"},
            "menu_title":{"font-weight":"bold"},
        }
    )

# KPI Cards
st.sidebar.title("🧾Key Metrics")
total_products = df["Product Name"].nunique()
total_revenue = df["Approx. Total Revenue(INR)"].sum()
avg_price = df["Price per Unit"].mean()
total_quantity_sold = df["Quantity Sold (liters/kg)"].sum()

total_products_card = f"Total Products: {total_products}"
total_revenue_card = f"Total Revenue: ₹{total_revenue:,.2f}"
avg_price_card = f"Avg Price per Unit: ₹{avg_price:.2f}"
total_quantity_sold_card = f"Total Quantity Sold: {total_quantity_sold}"

st.sidebar.info(total_products_card)
st.sidebar.info(total_revenue_card)
st.sidebar.info(avg_price_card)
st.sidebar.info(total_quantity_sold_card)

# Filter menu
# Sidebar Filters
st.sidebar.title("📶 Filters")
selected_brand = st.sidebar.selectbox("Select Brand", ["All"] + df["Brand"].unique().tolist())
selected_location = st.sidebar.selectbox("Select Location", ["All"] + df["Location"].unique().tolist())
selected_product = st.sidebar.selectbox("Select Product", ["All"] + df["Product Name"].unique().tolist())

# Extract Year from Date
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month  # Extracts month number (1-12)

# Year Filter
years_available = sorted(df["Year"].dropna().unique().tolist())
selected_year = st.sidebar.selectbox("Select Year", ["All"] + [str(year) for year in years_available])

# Apply Filters
filtered_df = df.copy()
if selected_brand != "All":
    filtered_df = filtered_df[filtered_df["Brand"] == selected_brand]
if selected_location != "All":
    filtered_df = filtered_df[filtered_df["Location"] == selected_location]
if selected_year != "All":
    selected_year = int(selected_year)  # Convert string to int
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]
if selected_product != "All":
    filtered_df = filtered_df[filtered_df["Product Name"] == selected_product]


# Home Page
if selected_page == "Overview":
    st.title("📊 Dairy Product Analysis Dashboard")
    st.image("Dairy products.jpg",use_container_width=True)
    
    st.write("### About the Dataset")
    st.write("This dataset contains information on dairy product sales, revenue, inventory, and production. It includes details such as product names, sales channels, stock levels, and total revenue.")
    st.dataframe(filtered_df)
     
    st.write("### Insights from the Data")
    st.write("- Identify top-selling dairy products and track revenue growth.")
    st.write("- Analyze sales trends across different locations and brands.")
    st.write("- Monitor inventory levels to prevent stock shortages or overstocking.")
    st.write("- Optimize pricing and distribution strategies based on demand.")
    
    st.write("### How This Helps Businesses Expand")
    st.write("1. **Optimizing Product Portfolio** - Businesses can focus on high-performing products and phase out underperforming ones.")
    st.write("2. **Market Expansion** - Identifying high-demand locations and expanding operations accordingly.")
    st.write("3. **Better Inventory Management** - Avoid stockouts and overstocking by maintaining an optimal inventory level.")
    st.write("4. **Customer Insights** - Understanding customer preferences to tailor marketing strategies.")
    st.write("5. **Improved Sales Strategies** - Determining the best sales channels (Retail, Wholesale, Online) to boost revenue.")
    st.write("6. **Competitive Pricing** - Adjusting prices based on demand and competition.")
    st.write("7. **Supply Chain Optimization** - Ensuring an efficient flow of goods from production to sales.")
    
    #st.dataframe(filtered_df)

# Sales & Revenue Analysis Page
if selected_page == "Sales":
    st.title("💰 Sales & Revenue Analysis")

    # Apply filters to KPI calculations
    total_products = filtered_df["Product Name"].nunique()
    total_revenue = filtered_df["Approx. Total Revenue(INR)"].sum()
    avg_price = filtered_df["Price per Unit"].mean()
    total_quantity_sold = filtered_df["Quantity Sold (liters/kg)"].sum()

    # KPI Cards with Filters Applied
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(label="**Total Products**", value=total_products)
    col2.metric(label="**Total Revenue (INR)**", value=f"₹{total_revenue:,.2f}")
    col3.metric(label="**Avg Price per Unit (INR)**", value=f"₹{avg_price:.2f}")
    col4.metric(label="**Total Quantity Sold (liters/kg)**", value=total_quantity_sold)


    st.write("#### 📉 Revenue by Brands")

    # Group and sort revenue by brand in descending order
    brand_revenue = filtered_df.groupby("Brand")["Approx. Total Revenue(INR)"].sum().reset_index()
    brand_revenue = brand_revenue.sort_values(by="Approx. Total Revenue(INR)", ascending=False)  # Explicit descending order

    # Create the funnel chart
    funnel_fig = px.funnel(brand_revenue, x="Approx. Total Revenue(INR)", y="Brand", 
                       title="Revenue by Brands", color="Brand", width=1400, height=450)

    # Force descending order in the funnel chart
    funnel_fig.update_layout(
        xaxis_title="Total Revenue (INR)",
        yaxis_title="Brand",
        font=dict(size=14),
        showlegend=False,  # Hide legend for clarity
        yaxis=dict(categoryorder="total ascending")  # Forces descending order display
    )

    st.plotly_chart(funnel_fig)

    st.write("#### 🌍 Sales by State (India)")

    # Aggregate revenue by state
    state_revenue = filtered_df.groupby("Location")["Quantity Sold (liters/kg)"].sum().reset_index()

    # Load India states GeoJSON data
    geojson_url = "https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson"
    geojson_data = requests.get(geojson_url).json()

    # Check correct property key in geojson (use 'NAME_1' instead of 'st_nm' if needed)
    try:
        state_name_mapping = {feature["properties"]["NAME_1"]: feature["properties"]["NAME_1"] for feature in geojson_data["features"]}
        state_revenue["Location"] = state_revenue["Location"].map(state_name_mapping)
    except KeyError:
        st.error("State name mapping failed. Check your GeoJSON structure.")
        
    # Merge with full India states
    all_states = pd.DataFrame({"Location": state_name_mapping.keys()})
    merged_df = all_states.merge(state_revenue, on="Location", how="left").fillna(0)  # Fill missing revenue with 0
    
    # Create choropleth map
    map_fig = px.choropleth(
        merged_df,
        geojson=geojson_data,
        locations="Location",
        featureidkey="properties.NAME_1",  # Match state names correctly
        color="Quantity Sold (liters/kg)",
        title="Quantity Sold Across Indian States",
        color_continuous_scale="blues",
        range_color=[0, 70_000],  # Fix color range between 0 and 4 million
        width=3000, height=450
    )

    # Set layout
    map_fig.update_geos(
    visible=False,
    fitbounds="locations",
    projection_type="mercator"  # Keeps India shape accurate
    )

    st.plotly_chart(map_fig)

    # Top 5 Dairy Products by Revenue
    st.write("### Top 5 Dairy Products by Revenue")
    top_products = filtered_df.groupby("Product Name")["Approx. Total Revenue(INR)"].sum().nlargest(5).reset_index()
    fig = px.bar(top_products, x="Product Name", y="Approx. Total Revenue(INR)", color="Product Name", 
                 title="Top 5 Products by Revenue", width=1400, height=450,
                 text="Approx. Total Revenue(INR)")
    fig.update_traces(textposition='outside')
    fig.update_layout(legend=dict(font=dict(size=14, weight="bold")))
    st.plotly_chart(fig)

    #Sales by Channel
    st.write("### Sales by Channel")
    sales_channel_fig = px.pie(filtered_df, names="Sales Channel", values="Approx. Total Revenue(INR)", 
                               title="Sales Channel Distribution", width=1200, height=450)
    sales_channel_fig.update_traces(textinfo="percent+label", textfont=dict(size=14, family="Arial", color="black"))
    sales_channel_fig.update_layout(legend=dict(font=dict(size=14, weight="bold")))
    st.plotly_chart(sales_channel_fig)

    st.write("### 📈 Revenue Trends Over Time (Monthly)")

    # Convert Month Number to Month Name for Sorting
    month_order = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 
               7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
    filtered_df["Month Name"] = filtered_df["Month"].map(month_order)

    # Aggregate Revenue by Month
    revenue_by_month = filtered_df.groupby(["Year", "Month Name"])["Approx. Total Revenue(INR)"].sum().reset_index()

    # Sort by Month Number
    revenue_by_month["Month Number"] = revenue_by_month["Month Name"].map({v: k for k, v in month_order.items()})
    revenue_by_month = revenue_by_month.sort_values(["Year", "Month Number"])

    # Create Line Chart
    trend_fig = px.line(revenue_by_month, x="Month Name", y="Approx. Total Revenue(INR)", 
                     color="Year", markers=True, line_shape="linear",
                     title="Monthly Revenue Trends Over Time", width=1400, height=450)

    # Add Data Labels
    trend_fig.update_traces(text=revenue_by_month["Approx. Total Revenue(INR)"].apply(lambda x: f"₹{x:,.2f}"), 
                        textposition="middle right",  # Moves labels slightly away from the line
                        textfont=dict(size=12, color="black", family="Arial"),  # Increase font size
                        hoverinfo="text+name")

    # Style Legends and Labels
    trend_fig.update_layout(legend=dict(title="Year", font=dict(size=14, weight="bold")),
                        xaxis_title="Month",
                        yaxis_title="Total Revenue (INR)",
                        font=dict(size=14))

    # Show Chart
    st.plotly_chart(trend_fig)




# Inventory & Stock Management
elif selected_page == "Inventory":
    
    st.title("📦 Inventory & Stock Management")
    
    st.write("### 🚨Low Stock Alerts")
    low_stock = filtered_df[filtered_df["Quantity in Stock (liters/kg)"] < filtered_df["Minimum Stock Threshold (liters/kg)"]]
    # Select only the necessary columns
    low_stock_columns = ["Location", "Product ID", "Product Name", "Brand", "Quantity in Stock (liters/kg)", "Minimum Stock Threshold (liters/kg)"]
    low_stock_filtered = low_stock[low_stock_columns]

    # Display the table in Streamlit
    st.dataframe(low_stock_filtered)
    
    st.write("### 📊 Product Shelf Life Distribution")

    # Create a scatter plot to show shelf life for each product
    shelf_life_fig = px.strip(
    filtered_df,
    x="Shelf Life (days)",
    y="Product Name",
    color="Product Name",
    title="Product Shelf Life Distribution",
    labels={"Shelf Life (days)": "Shelf Life (Days)", "Product Name": "Product"},
    height=450
    )

    # Customize layout for better readability
    shelf_life_fig.update_layout(
    xaxis_title="Shelf Life (Days)",
    yaxis_title="Product",
    showlegend=False
    )

    st.plotly_chart(shelf_life_fig)

    st.write("### 🌞 Storage Condition Across Products")

    sunburst_fig = px.sunburst(
    filtered_df,
    path=["Storage Condition", "Product Name"],
    values="Quantity in Stock (liters/kg)",  # Helps represent quantity visually
    color="Storage Condition",
    title="Product Storage Condition Distribution",
    )

    # Customize layout for better readability
    sunburst_fig.update_traces(textinfo="label+percent entry")

    st.plotly_chart(sunburst_fig)

    
    st.write("### 📊 Reorder Quantity by Product")

    # Create a lollipop chart for reorder quantity
    reorder_fig = px.scatter(
    filtered_df,
    x="Reorder Quantity (liters/kg)",
    y="Product Name",
    color="Product Name",
    title="Reorder Quantity by Product",
    labels={"Reorder Quantity (liters/kg)": "Reorder Quantity", "Product Name": "Product"},
    height=450
    )

    # Add a line to connect points (to make it a lollipop chart)
    for product in filtered_df["Product Name"].unique():
        product_df = filtered_df[filtered_df["Product Name"] == product]
        reorder_fig.add_trace(px.line(
            product_df,
            x="Reorder Quantity (liters/kg)",
            y="Product Name"
        ).data[0])

    # Customize layout for better readability
    reorder_fig.update_layout(
    xaxis_title="Reorder Quantity (liters/kg)",
    yaxis_title="Product",
    showlegend=False
    )

    st.plotly_chart(reorder_fig)
    
elif selected_page == "Customer Demand":
    
    st.title("📈 Customer Demand & Trends")

    # Best-Selling Products
    st.write("### 🏆 Best-Selling Dairy Products")
    top_selling = filtered_df.groupby("Product Name")["Quantity Sold (liters/kg)"].sum().nlargest(10).reset_index()
    best_selling_fig = px.bar(
        top_selling,
        x="Product Name",
        y="Quantity Sold (liters/kg)",
        color="Product Name",
        title="Top 10 Best-Selling Dairy Products"
    )
    best_selling_fig.update_traces(texttemplate='%{y}', textposition='outside')  # Add data labels
    st.plotly_chart(best_selling_fig)

    # Seasonal Trends
    st.write("### 📅 Seasonal Sales Trends")
    # Extract Month and Year for Analysis
    filtered_df["Month"] = pd.to_datetime(filtered_df["Date"]).dt.month
    filtered_df["Year"] = pd.to_datetime(filtered_df["Date"]).dt.year

    # Define Month Order for Proper Sorting
    month_order = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }

    # Convert Month Number to Month Name
    filtered_df["Month Name"] = filtered_df["Month"].map(month_order)

    # Aggregate Sales Data by Month
    seasonal_sales = filtered_df.groupby(["Year", "Month Name"])["Quantity Sold (liters/kg)"].sum().reset_index()

    # Sort Data by Year & Month Order
    seasonal_sales["Month Number"] = seasonal_sales["Month Name"].map({v: k for k, v in month_order.items()})
    seasonal_sales = seasonal_sales.sort_values(["Year", "Month Number"])

    # Create Line Chart for Seasonal Trends
    seasonal_trend_fig = px.line(seasonal_sales, 
                              x="Month Name", 
                              y="Quantity Sold (liters/kg)", 
                              color="Year",
                              markers=True)

    # Enhance Chart Formatting
    seasonal_trend_fig.update_traces(textposition="top center", marker=dict(size=8))
    seasonal_trend_fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Quantity Sold",
    xaxis={'categoryorder':'array', 'categoryarray': list(month_order.values())},  # Ensure Months are in Order
    legend_title="Year",
    font=dict(size=14)
    )

    # Display Chart
    st.plotly_chart(seasonal_trend_fig, use_container_width=True)


    # Brand Popularity
    st.write("### 🏷️ Brand Market Share")
    # Aggregate Revenue by Brand and Product
    brand_product_revenue = filtered_df.groupby(["Brand", "Product Name"])["Quantity Sold (liters/kg)"].sum().reset_index()

    # Create Sunburst Chart
    sunburst_fig = px.sunburst(
    brand_product_revenue,
    path=["Brand", "Product Name"],  # Hierarchical Levels (Parent → Child)
    values="Quantity Sold (liters/kg)",  # Determines Size of Each Section
    title="Brand Market Share by Revenue",
    color="Quantity Sold (liters/kg)", 
    color_continuous_scale="blues"  # Adjust color scheme if needed
    )

    # Improve Formatting
    sunburst_fig.update_traces(textinfo="label+percent parent")  # Show Label + Parent %
    sunburst_fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    # Display Chart
    st.plotly_chart(sunburst_fig, use_container_width=True)



    # Price Sensitivity Analysis
    st.write("### 💰 Price Sensitivity Analysis")
    price_sensitivity_fig = px.scatter(
        filtered_df,
        x="Price per Unit",
        y="Quantity Sold (liters/kg)",
        color="Product Name",
        size="Quantity Sold (liters/kg)",
        title="Impact of Price on Sales",
        hover_data=["Product Name"]
    )
    price_sensitivity_fig.update_traces(marker=dict(opacity=0.7))  # Improve visibility
    
    st.plotly_chart(price_sensitivity_fig)
