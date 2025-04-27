import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import plotly.express as px


# Reading the data
df = pd.read_csv("cleaning dataset final.csv")
#st.header("Mapping Trends in Digital Engagement")
st.markdown(
    """
    <div style='text-align: center;'>
        <h3 style='color: #1E90FF; font-size: 42px; font-weight: bold; font-family: Arial, sans-serif;'>
            <em>The Social Clock: Mapping Global Trends in Digital Engagement 📱</em> 
        </h3>
        <p style='color: #555; font-size: 18px; font-style: italic; font-family: "Georgia", serif;'>
            Understanding user behavior is vital in today’s digital age. This project analyzes global social media engagement across demographics, platforms, and devices. With advanced visualizations and interactive filters, it empowers data-driven decisions and uncovers key digital trends. Welcome to the future of social insights!.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)



# Load the logo image
logo = Image.open("Project Logo.jpg")  # Replace with the path to your logo file

# Display the logo at the top of the sidebar
st.sidebar.image(logo, use_container_width=True)  # Updated parameter

# Sidebar Filters
# Sidebar Filters
st.sidebar.header("Filter Options")

# Gender Filter
if st.sidebar.checkbox("Select All Genders", value=True):
    gender_filter = df["Gender"].unique()
else:
    gender_filter = st.sidebar.multiselect(
        "Select Gender",
        options=df["Gender"].unique(),
        default=[]  # Start with no selection when "Select All" is unchecked
    )

# Profession Filter
if st.sidebar.checkbox("Select All Professions", value=True):
    professions_filter = df['Profession'].unique()
else:
    professions_filter = st.sidebar.multiselect(
        "Select Profession:", 
        options=df['Profession'].unique(),
        default=[]  # Start with no selection when "Select All" is unchecked
    )

# Age Range Filter
age_filter = st.sidebar.slider(
    "Select Age Range",
    min_value=int(df["Age"].min()),
    max_value=int(df["Age"].max()),
    value=(int(df["Age"].min()), int(df["Age"].max()))
)

# Location Filter
if st.sidebar.checkbox("Select All Locations", value=True):
    location_filter = df["Location"].unique()
else:
    location_filter = st.sidebar.multiselect(
        "Select Location",
        options=df["Location"].unique(),
        default=[]  # Start with no selection when "Select All" is unchecked
    )

# Platform Filter
if st.sidebar.checkbox("Select All Platforms", value=True):
    platform_filter = df["Platform"].unique()
else:
    platform_filter = st.sidebar.multiselect(
        "Select Platform",
        options=df["Platform"].unique(),
        default=[]  # Start with no selection when "Select All" is unchecked
    )

# Device Type Filter
if st.sidebar.checkbox("Select All Devices", value=True):
    device_filter = df["DeviceType"].unique()
else:
    device_filter = st.sidebar.multiselect(
        "Select Device Type",
        options=df["DeviceType"].unique(),
        default=[]  # Start with no selection when "Select All" is unchecked
    )



# Apply Filters
filtered_df = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Age"].between(*age_filter)) &
    (df["Location"].isin(location_filter)) &
    (df["Platform"].isin(platform_filter))&
    (df['Profession'].isin(professions_filter))&
    (df['DeviceType'].isin(device_filter))
]


# KPIs Calculation on Filtered Data
st.subheader("Overall Insights Engine Analysis")
avg_engagement = filtered_df['Engagement'].mean()
total_time_spent = filtered_df['Total Time Spent'].sum()
avg_time_video = filtered_df['Time Spent On Video'].mean()

# Create a single row for KPIs
col1, col2, col3 = st.columns(3)

# Function to display styled KPI with modern design
def styled_metric(label, value, font_size_label=16, font_size_value=24, bg_color="#f9f9f9", text_color="#333"):
    st.markdown(
        f"""
        <div style="background: {bg_color}; border-radius: 10px; padding: 15px; text-align: center; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
            <p style="margin: 0; font-size: {font_size_label}px; color: {text_color}; font-weight: bold;">{label}</p>
            <p style="margin: 0; font-size: {font_size_value}px; color: {text_color}; font-weight: bold;">{value}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display KPIs in columns with light colors
with col1:
    styled_metric("Average Engagement", f"{avg_engagement:.2f}", bg_color="#eaf4fc", text_color="#1e81b0")

with col2:
    styled_metric("Total Time Spent", f"{total_time_spent / 3600:.2f} hours", bg_color="#fff4e6", text_color="#f39c12")

with col3:
    styled_metric("Time Spent per Video", f"{avg_time_video:.2f} seconds", bg_color="#eafce9", text_color="#27ae60")



####1
# Sidebar Filters

# Group the filtered data
if not filtered_df.empty:
    connection_counts = filtered_df.groupby(['Profession', 'ConnectionType'], observed=True).size().unstack(fill_value=0)

    # Subheader for the chart
    st.subheader("Connection Type Usage by Profession")

    # Create a Matplotlib figure with a modern style
    #plt.style.use('seaborn-poster')
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.set_palette("viridis", len(connection_counts.columns))

    # Create the bar plot
    connection_counts.plot(kind='bar', stacked=False, ax=ax)
    ax.set_xlabel('Profession', color='#333', fontsize=16, weight='bold')
    ax.set_ylabel('Count', color='#333', fontsize=16, weight='bold')
    ax.set_title('Connection Type Usage by Profession', fontsize=20, color='#2C3E50', weight='bold', pad=20)

    # Adjust legend placement and style
    ax.legend(title='Connection Type', title_fontsize=14, loc='upper right', fontsize=12)

    # Add a grid for better readability
    ax.grid(axis='y', linestyle='--', linewidth=0.6, alpha=0.7)

    # Remove the default Streamlit "box" by using the full width of the layout
    st.pyplot(fig, use_container_width=True)
else:
    st.warning("No data available for the selected filters.")





#######2
2####
# Sidebar Filters for Dynamic Visualization
# Sidebar Filters for Dynamic Visualization
# Calculate average addiction level for selected age groups
if not filtered_df.empty:
    grouped_data = filtered_df.groupby('Age')['Addiction Level'].mean()

    # Plot the line chart
    st.subheader("Average Addiction Level by Age Group")
    fig, ax = plt.subplots(figsize=(10, 6))  # Set figure size for better readability
    # Line chart with customization
    ax.step(grouped_data.index, grouped_data.values, marker='o', linestyle='--', color="olive", linewidth=2)

    # Annotate each data point with its value
    for i, (x, y) in enumerate(zip(grouped_data.index, grouped_data.values)):
        ax.text(x, y, f'{y:.2f}', fontsize=10, color='#FF1493', ha='center', va='bottom')  # Adjust fontsize and position

    # Add axis labels and title
    ax.set_xlabel('Age Group', fontsize=14, color='#FF1493')
    ax.set_ylabel('Average Addiction Level', fontsize=14, color='#FF1493')
    ax.set_title('Average Addiction Level by Age Group', fontsize=20, color='#C71585')

    # Add gridlines for better readability
    ax.grid(True, linestyle='--', linewidth=0.5,color='#FF1493')

    # Render the plot dynamically in Streamlit
    st.pyplot(fig)
else:
    st.warning("No data available for the selected filters.")







3##### Sidebar Filters

# Group the filtered data
if not filtered_df.empty:
    grouped_data = filtered_df.groupby(['Gender', 'Platform'], observed=True)['Self Control'].count().unstack(fill_value=0)

    # Plotting the bar chart
    st.subheader("📊 Self-Control Across Genders and Platforms 🌐")
    fig, ax = plt.subplots(figsize=(12, 8))

    # Create the bar plot
    grouped_data.plot(
        kind='bar', 
        stacked=True, 
        colormap='viridis', 
        figsize=(12, 6), 
        edgecolor='black',  # Adding borders for better clarity
        ax=ax
    )

    # Customizing the chart
    ax.set_title('Self Control Across Genders on Different Platforms', fontsize=20, pad=20, color='#006400')
    ax.set_xlabel('Gender', fontsize=16, labelpad=10)
    ax.set_ylabel('Self Control', fontsize=16, labelpad=10)
    ax.legend(title='Platform', fontsize=12, loc='upper right')  # Adjust legend position
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=14)

    # Adding gridlines for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Render the plot dynamically in Streamlit
    st.pyplot(fig)
else:
    st.warning("No data available for the selected filters.")



###4

st.subheader("Time Spent by Age Group")
if not filtered_df.empty:
    bins = [0, 18, 30, 40, 50, 60, 100]
    labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '60+']
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    average_time_spent = df.groupby('Age Group')['Total Time Spent'].mean().reset_index()
    fig = px.bar(
        average_time_spent, 
        x='Age Group', 
        y='Total Time Spent', 
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(
        title="Average Time Spent by Age Group",
        xaxis_title="Age Group",
        yaxis_title="Total Time Spent (minutes)",
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig)
else:
    st.warning("No data available for Time Spent.")



#####5
# Assuming your DataFrame 'df' is already loaded
# If not, replace this with the actual loading mechanism
df = pd.read_csv("cleaning dataset final.csv")

# Create a synthetic date column
start_date = '2023-01-01'  # Change this to your desired start date
df['Date'] = pd.date_range(start=start_date, periods=len(df), freq='D')

# Ensure the 'Date' column is in datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Aggregate the data by month
df['Month'] = df['Date'].dt.to_period('M')  # Create a new column for month

# Calculate total time spent per month
monthly_trends = df.groupby('Month')['Total Time Spent'].sum().reset_index()

# Convert 'Month' back to a datetime format for plotting
monthly_trends['Month'] = monthly_trends['Month'].dt.to_timestamp()

# Visualization in Streamlit
st.subheader("📊 Monthly Trends in Social Media Engagement")

# Create the Matplotlib plot
fig, ax = plt.subplots(figsize=(12, 6))

# Set a custom background color
ax.set_facecolor('#f0f8ff')  # Light blue background

# Draw the line plot with sharp transitions
ax.plot(
    monthly_trends['Month'],
    monthly_trends['Total Time Spent'],
    marker='o',
    linestyle='-',
    color='blue',
    linewidth=2.5,
    markersize=8,
    label='Total Time Spent'
)

# Add a title and subtitle
ax.set_title('Monthly Trends in Social Media Engagement', fontsize=20, fontweight='bold', color='darkblue')
ax.set_xlabel('Month', fontsize=16, fontweight='bold', color='purple', labelpad=15)
ax.set_ylabel('Total Time Spent (minutes)', fontsize=16, fontweight='bold', color='teal', labelpad=15)

# Customize ticks
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

# Add prominent grid lines
ax.grid(color='gray', linestyle='-', linewidth=0.7, alpha=0.7)

# Annotate each point with its value
for i, row in monthly_trends.iterrows():
    ax.text(
        row['Month'],
        row['Total Time Spent'] + 50,  # Position text slightly above
        f"{row['Total Time Spent']}",
        ha='center',
        va='bottom',
        fontsize=9,
        color='black',
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.3')
    )

# Add a legend
ax.legend(loc='upper right', fontsize=12)

# Spread the plot slightly equally from both sides
plt.xlim([monthly_trends['Month'].min() - pd.DateOffset(days=10), monthly_trends['Month'].max() + pd.DateOffset(days=10)])

# Render the plot in Streamlit
st.pyplot(fig)





####6
# Create a new 'Hour' column based on 'Total Time Spent'
df['Hour'] = df['Total Time Spent'] // 60

# Check if 'Hour' column is present
if 'Hour' not in df.columns:
    print("Error: 'Hour' column not found!")
else:
    # Check data types of columns
    print(df.dtypes)
    df['Hour'] = df['Hour'].astype(int)  # Ensure Hour is integer

    # Set the style of seaborn with a soft background color
    sns.set(style="whitegrid", rc={"axes.facecolor": "#e6f2ff"})  # Light blue background for the plot area

    # Create a box plot
    plt.figure(figsize=(18, 12))  # Increased figure size for more space
    box_plot = sns.boxplot(
        x='Hour', 
        y='Total Time Spent', 
        data=df, 
        hue='Hour',  # Set hue to 'Hour' for proper color mapping
        palette="coolwarm",  # Attractive color palette
        linewidth=2,  # Thicker lines for better visibility
        width=0.8,  # Wider boxes to give a more spaced-out look
        fliersize=6,  # Larger outliers for better visibility
        legend=False  # Hide legend since hue is only for color mapping
    )

    # Modify the title with matching colors and design
    plt.title('Distribution of Time Spent on Social Media by Hour of the Day', 
              fontsize=30, fontweight='bold', 
              color='darkblue', backgroundcolor='lightyellow', 
              pad=25, style='italic', loc='center')

    # Customize the axis labels with vibrant colors and light yellow background
    xlabel = plt.xlabel('Hour of the Day', fontsize=20, fontweight='bold', color='darkgreen', labelpad=20, style='italic')
    ylabel = plt.ylabel('Total Time Spent (minutes)', fontsize=20, fontweight='bold', color='darkgreen', labelpad=20, style='italic')

    # Set the background color for the x and y axis labels
    xlabel.set_bbox(dict(facecolor='lightyellow', edgecolor='none', alpha=0.7))
    ylabel.set_bbox(dict(facecolor='lightyellow', edgecolor='none', alpha=0.7))

    # Add text labels for each box (median values with "Median" label)
    for i in range(24):
        median = df[df['Hour'] == i]['Total Time Spent'].median()
        if pd.notna(median):  
            # Adding "Median: " before the value
            box_plot.text(i, median + 5, f'Median: {median:.1f}', 
                          horizontalalignment='center', size=12, color='black', weight='semibold', 
                          bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3'))

    # Set x-axis ticks from 0 to 10
    plt.xticks(range(11), fontsize=14, color='slategray', fontweight='bold')

    # Increase y-axis limits to show a larger range of 'Total Time Spent'
    plt.ylim(0, df['Total Time Spent'].max() + 100)  # Increase y-axis range to show more spread

    # Style the ticks and grid
    plt.yticks(fontsize=14, color='slategray', fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # Remove top and right spines for a cleaner look
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(plt)







###7


# Assuming 'df' is your DataFrame
# Replace 'df' with your actual DataFrame if it's named differently

# Example: Make sure platform_filter is a DataFrame and contains the 'Platform' column
# You might have a DataFrame like df containing platform data


# Assuming 'df' is your main DataFrame, replace with your actual DataFrame if it's named differently
# Ensure that the DataFrame contains the 'Platform' and 'Total Time Spent' columns

# Check if 'Platform' column exists in the main DataFrame (df)
if 'Platform' in df.columns and 'Total Time Spent' in df.columns:
    # Group the data by 'Platform' and calculate the total time spent
    platform_data = df.groupby('Platform').agg({
        'Total Time Spent': 'sum'  # Sum total time spent
    }).reset_index()
    st.header("Top 4 Social Media Plateform")
    # Add a multiselect for platform selection
    selected_platforms = st.multiselect("Select Platforms", options=platform_data['Platform'].unique())

    if selected_platforms:
        # Filter the data based on the selected platforms
        filtered_platform_data = platform_data[platform_data['Platform'].isin(selected_platforms)]

        # Display KPI for each selected platform
        for platform in selected_platforms:
            total_time_spent_selected = filtered_platform_data[filtered_platform_data['Platform'] == platform]['Total Time Spent'].sum()
            st.metric(label=f"Total Time Spent on {platform}", value=f"{total_time_spent_selected:,} hours")

        # Create a pie chart with Plotly Express for the selected platforms
        fig = px.pie(filtered_platform_data, values='Total Time Spent', names='Platform', 
                     title='Time Spent Distribution Across Selected Platforms',  # Dynamic title
                     color_discrete_sequence=px.colors.qualitative.Set3,  # Color palette
                     hover_name='Platform', hover_data=['Total Time Spent'])

        # Update the layout of the pie chart
        fig.update_layout(
            width=800, height=600, font_size=14, 
            title=dict(
                text='<b><span style="color:##FC8D62;"></span></b><br>'
                     '<span style="font-style:italic;font-size:18px; color:#888888;">(Based on Total Time Spent)</span>',
                font=dict(family='Arial Black', size=26),
                x=0.5, y=0.97, xanchor='center', yanchor='top'
            )
        )
        fig.update_traces(marker=dict(line=dict(width=3, color='white')),
                          textinfo='label+percent', textposition='inside', textfont_size=16)

        # Render the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    else:
        # Show a warning message if no platform is selected
        st.warning("Please select at least one platform to see the data.")

else:
    # Error message if 'Platform' or 'Total Time Spent' columns are missing
    st.error("Columns 'Platform' or 'Total Time Spent' not found in the dataset.")




###8
# Group and calculate mean time spent
demographic_time = df.groupby(["Gender", "Location"])["Total Time Spent"].mean().unstack()

# Streamlit app structure
st.subheader("Time Spent on Social Media by Gender and Location")

# Heatmap Visualization
if not filtered_df.empty:
    demographic_time = filtered_df.groupby(["Gender", "Location"])["Total Time Spent"].mean().unstack()

    if demographic_time.empty:
        st.warning("No data available to generate the heatmap. Please adjust the filters.")
    else:
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(
            demographic_time,
            ax=ax,
            annot=True,
            fmt=".1f",
            cmap="viridis",
            cbar_kws={'label': 'Avg Time Spent (mins)'}
        )
        ax.set_title("Time Spent on Social Media by Gender and Location", fontsize=16)
        ax.set_ylabel("Gender", fontsize=12)
        ax.set_xlabel("Location", fontsize=12)
        st.pyplot(fig)
else:
    st.warning("No data available for the selected filters. Please adjust the filters.")


#Custom footer in raw html/css paired with markdown feature of streamlit
footer = """
<style>
.footer {
    position: relative; /* Make footer relative to the content */
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
    margin-top: 20px; /* Adds spacing before the footer */
    padding: 10px 0;  /* Adds padding inside the footer */
    border-top: 1px solid #ddd; /* Optional: Add a subtle top border */
}
</style>
<div class="footer">
    <p>☀️Developed by Shivani Singh☀️ </p>
    
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
