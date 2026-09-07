import streamlit as st
import sqlite3
import pandas as pd

st.title('Manufacturing Production Analytics Dashboard')

st.caption(
    'Interactive dashboard for monitoring production performance,'
    'downtime, and downtime factors.'
)

connection = sqlite3.connect('manufacturing.db')

query = """
SELECT * FROM production_analysis; """

data = pd.read_sql_query(query, connection)

st.subheader('Filters')
col1, col2, col3 = st.columns(3)
with col1:
    selected_product = st.selectbox(
        'Product',
        ['All'] + sorted(data['product_name'].unique().tolist())
    )

with col2:
    selected_shift = st.selectbox(
        'Shift',
        ['All'] + sorted(data['shift'].unique().tolist())
    )

with col3:
    selected_operator = st.selectbox(
        'Operator',
        ['All'] + sorted(data['operator'].unique().tolist())
    )

filtered_data = data.copy()

if selected_product != 'All':
    filtered_data = filtered_data[
        filtered_data['product_name'] == selected_product
    ]

if selected_shift != 'All':
    filtered_data = filtered_data[
        filtered_data['shift'] == selected_shift
    ]

if selected_operator != 'All':
    filtered_data = filtered_data[
        filtered_data['operator'] == selected_operator
    ]

st.divider()

st.subheader('Production Overview')
col1, col2, col3, col4 = st.columns(4)
col1.metric(
    'Total Batches', len(filtered_data)
)

col2.metric(
    'Total Quantity',
    f"{filtered_data['quantity_produced'].sum():,.0f}"
)

col3.metric(
    'Average Time Variance',
    f"{filtered_data['time_variance_min'].mean():.2f} min"
)

col4.metric(
    'Average Downtime',
    f"{filtered_data['downtime_minutes'].mean():.2f} min"
)

st.divider()

st.subheader('Average Time Variance by Product')
product_performance = (
    filtered_data.groupby('product_name')['time_variance_min']
    .mean().reset_index()
)

product_performance['time_variance_min'] = (
    product_performance['time_variance_min'].round(2)
)

st.bar_chart(
    product_performance.set_index('product_name')
)

st.subheader('Average Downtime by Shift')
shift_performance = (
    filtered_data.groupby('shift')['downtime_minutes']
    .mean().reset_index()
)

shift_performance['downtime_minutes'] = (
    shift_performance['downtime_minutes'].round(2)
)

st.bar_chart(
    shift_performance.set_index('shift')
)

st.subheader('Total Quantity Produced by Product')
product_quantity = (
    filtered_data.groupby('product_name')['quantity_produced']
    .sum().reset_index()
)

st.bar_chart(
    product_quantity.set_index('product_name')
)

st.divider()

st.subheader('Total Downtime by Factor')
selected_batches = filtered_data['batch_id'].tolist()
if selected_batches:
    placeholders = ','.join(["?"] * len(selected_batches))

    factor_query = f"""
    SELECT
        df.factor_name,
        SUM(d.downtime_minutes) AS total_downtime
    FROM downtime d
    JOIN downtime_factors df
        ON d.factor_id = df.factor_id
    WHERE d.batch_id IN ({placeholders})
    GROUP BY df.factor_name
    ORDER BY total_downtime DESC;
    """

    factor_data = pd.read_sql_query(
        factor_query,
        connection,
        params=selected_batches
    )

    st.bar_chart(
        factor_data.set_index('factor_name'),
        horizontal=True
    )

st.subheader('Production Data')
st.dataframe(filtered_data)
connection.close()