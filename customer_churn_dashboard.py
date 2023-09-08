# Import required libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate KPIs
def calculate_kpis(df):
    kpis = {}
    total_customers = len(df)
    churned_customers = len(df[df['Exited'] == 1])
    kpis['Churn Rate'] = round((churned_customers / total_customers) * 100, 2)
    
    df['CLV'] = (df['Balance'] * df['Age']) / df['NumOfProducts']
    kpis['Average CLV'] = round(df['CLV'].mean(), 2)
    
    df['ARPU'] = df['Balance'] / df['NumOfProducts']
    kpis['Average ARPU'] = round(df['ARPU'].mean(), 2)
    
    kpis['Average Satisfaction Score'] = round(df['Satisfaction Score'].mean(), 2)
    
    kpis['Retention Rate'] = round(100 - kpis['Churn Rate'], 2)
    
    return kpis

# Initialize Streamlit app
st.title("Custom Churn Dashboard")

# Upload data through Streamlit
uploaded_file = st.file_uploader("Upload your customer data file", type=["csv", "xlsx"])
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        customer_data = pd.read_csv(uploaded_file)
    else:
        customer_data = pd.read_excel(uploaded_file)

    # Calculate KPIs
    kpi_values = calculate_kpis(customer_data)
    
    # Convert KPIs to a DataFrame for display
    kpi_df = pd.DataFrame(list(kpi_values.items()), columns=['KPI', 'Value'])
    
    # Display KPIs in a table
    st.header("Key Performance Indicators")
    st.table(kpi_df.set_index('KPI'))
    
    # Create a bar chart for Churn Rate vs. Retention Rate
    st.header("Churn Rate vs. Retention Rate")
    churn_retention_data = pd.DataFrame({
        'Metric': ['Churn Rate', 'Retention Rate'],
        'Value': [kpi_values['Churn Rate'], kpi_values['Retention Rate']]
    })
    st.bar_chart(churn_retention_data.set_index('Metric'))

    # Create two columns for the histograms
    col1, col2 = st.columns(2)

    # Create a histogram for Customer Lifetime Value (CLV) in the first column
    with col1:
        st.header("Customer Lifetime Value (CLV) Distribution")
        fig1, ax1 = plt.subplots()
        ax1.hist(customer_data['CLV'], bins=20, edgecolor='black')
        ax1.set_xlabel('Customer Lifetime Value')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Distribution of Customer Lifetime Value')
        st.pyplot(fig1)
        plt.close(fig1)

    # Create a histogram for Average Revenue Per User (ARPU) in the second column
    with col2:
        st.header("Average Revenue Per User (ARPU) Distribution")
        fig2, ax2 = plt.subplots()
        ax2.hist(customer_data['ARPU'], bins=20, edgecolor='black')
        ax2.set_xlabel('Average Revenue Per User')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Distribution of Average Revenue Per User')
        st.pyplot(fig2)
        plt.close(fig2)

    # Create a pie chart for Customer Satisfaction Scores
    st.header("Distribution of Customer Satisfaction Scores")
    score_counts = customer_data['Satisfaction Score'].value_counts().sort_index()
    fig3, ax3 = plt.subplots()
    ax3.pie(score_counts, labels=score_counts.index, autopct='%1.1f%%', startangle=90)
    ax3.axis('equal')
    plt.title('Distribution of Customer Satisfaction Scores')
    st.pyplot(fig3)
    plt.close(fig3)
