import streamlit as st
import datetime
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import capm_functions
import numpy as np
import plotly.express as px

st.title("Calculate Beta and Return for individual stock")

# User inputs
col1, col2 = st.columns([2, 1])
with col1:
    selected_stock = st.selectbox(
        "Choose a stock",
        ['TSLA', 'AAPL', 'NFLX', 'MSFT', 'MGM', 'AMZN', 'NVDA', 'GOOGL']
    )
with col2:
    num_years = st.number_input("Number of Years", 1, 10, value=1)

try:
    # Date range
    end = datetime.date.today()
    start = datetime.date(end.year - num_years, end.month, end.day)

    # Download data
    sp500 = web.DataReader(['sp500'], 'fred', start, end).reset_index()
    stock_data = yf.download(selected_stock, start=start, end=end)['Close'].reset_index()
    
    # Rename columns
    sp500.columns = ['Date', 'sp500']
    stock_data.columns = ['Date', selected_stock]

    # Merge datasets
    df = pd.merge(stock_data, sp500, on='Date', how='inner')

    # Calculate daily returns
    daily_returns = capm_functions.daily_return(df)

    # Calculate beta and return
    beta, alpha = capm_functions.calculate_beta(daily_returns, selected_stock)
    rf = 0
    rm = daily_returns['sp500'].mean() * 252
    expected_return = rf + beta * (rm - rf)

    st.markdown(f"### Beta : {beta}")
    st.markdown(f"### Return : {round(expected_return, 2)}")

    # Plot regression chart
    fig = px.scatter(
        daily_returns,
        x='sp500',
        y=selected_stock,
        trendline="ols",
        title=selected_stock
    )
    fig.update_layout(width=900, height=500)
    st.plotly_chart(fig)

except:
    str.write('We were unable to generate the Beta plot for this stock due to insufficient or missing historical market data during the selected period. Try adjusting the time range or selecting a different stock')
