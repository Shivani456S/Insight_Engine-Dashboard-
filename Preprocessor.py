import pandas as pd
import streamlit as st
from Preprocessor import preprocessor_data
from datetime import datetime

def preprocessor_data("cleaning dataset final.csv"):
    # Read the dataset
    df = pd.read_csv("cleaning dataset final.csv")
    
    # Clean the dataset (handle missing values, incorrect data types, etc.)
    df = clean_data(df)
    
    # Create new columns based on existing ones if needed (e.g., date parsing, time calculations)
    df = create_additional_columns(df)
    
    # Return the processed dataframe
    return df

def clean_data(df):
    # Handle missing values (you can also drop rows or columns, or fill with a value)
    df = df.dropna(subset=['Gender', 'Profession', 'Age', 'Location', 'Platform', 'Total Time Spent', 'Engagement'])  # Example, modify as needed
    
    # Convert data types to appropriate types
    df['Age'] = df['Age'].astype(int)  # Ensure 'Age' is an integer
    df['Total Time Spent'] = df['Total Time Spent'].astype(float)  # Ensure 'Total Time Spent' is a float
    df['Engagement'] = df['Engagement'].astype(float)  # Ensure 'Engagement' is a float
    
    # Handle duplicates if necessary
    df = df.drop_duplicates()
    
    return df

def create_additional_columns(df):
    # Convert 'Date' to datetime format if the dataset contains a 'Date' column
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Coerce errors to NaT if invalid
    
    # Example: Create a 'Hour' column from 'Total Time Spent' (assuming 'Total Time Spent' is in minutes)
    df['Hour'] = df['Total Time Spent'] // 60  # Convert minutes to hours
    
    # Example: Create a 'Month' column for grouping by month (if 'Date' is available)
    if 'Date' in df.columns:
        df['Month'] = df['Date'].dt.to_period('M')  # Add month column
    
    return df

def add_custom_bins(df):
    # Create custom age groups if necessary
    bins = [0, 18, 30, 40, 50, 60, 100]
    labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '60+']
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    
    return df

def aggregate_monthly_data(df):
    # Aggregate data by month for trends over time (for example: total time spent by month)
    if 'Date' in df.columns:
        df['Month'] = df['Date'].dt.to_period('M')  # Ensure 'Month' column exists
        monthly_data = df.groupby('Month')['Total Time Spent'].sum().reset_index()
        monthly_data['Month'] = monthly_data['Month'].dt.to_timestamp()  # Convert 'Month' back to datetime format
        return monthly_data
    else:
        return None
