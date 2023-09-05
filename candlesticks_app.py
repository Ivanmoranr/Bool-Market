import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from candlesticks import create_candlestick_chart, create_data_stock, create_candle_chart
from cdl_patterns import CDL_PATTERNS
import talib
import ipywidgets as widgets
from ipywidgets import interactive
from IPython.display import display

# Streamlit app title and description
st.title("Candlestick Pattern Analyzer")
st.write("Select a stock symbol and date range to analyze candlestick patterns.")

# Input form for stock symbol, start date, and end date
ticker = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL):")
start_date = st.text_input("Enter Start Date (YYYY-MM-DD):")
end_date = st.text_input("Enter End Date (YYYY-MM-DD):")

# Create a button to fetch data
if st.button("Fetch Data and Analyze"):
    try:
        # Fetch historical stock data
        data = yf.download(ticker, start=start_date, end=end_date)
        data.reset_index(inplace=True)

        # Create a list to hold the selected patterns
        selected_patterns = []

        # Create a checkbox for each pattern
        st.write("Select Candlestick Patterns to Analyze:")
        for pattern_name in CDL_PATTERNS.keys():
            checkbox = st.checkbox(pattern_name)
            if checkbox:
                selected_patterns.append(pattern_name)

        # Filter the patterns
        filtered_data = data.copy()
        for pattern_name in selected_patterns:
            pattern_code = CDL_PATTERNS[pattern_name]
            pattern_results = pattern_code(data['Open'], data['High'], data['Low'], data['Close'])
            filtered_data[pattern_name] = pattern_results

        # Create a list to hold the selected patterns as traces
        selected_traces = []

        # Add selected patterns to the traces list
        for pattern_name in selected_patterns:
            selected_traces.append(
                go.Scatter(
                    x=filtered_data['Date'],
                    y=filtered_data[pattern_name],
                    mode='markers',
                    name=pattern_name
                )
            )

        # Create Candlestick Chart
        fig = go.Figure(data=[go.Candlestick(
            x=filtered_data['Date'],
            open=filtered_data['Open'],
            high=filtered_data['High'],
            low=filtered_data['Low'],
            close=filtered_data['Close'],
            name='Candlesticks'
        )])

        # Add selected pattern traces to the chart
        for trace in selected_traces:
            fig.add_trace(trace)

        # Customize the layout
        fig.update_layout(
            title=f'Candlestick Chart with Selected Patterns ({", ".join(selected_patterns)})',
            xaxis_title='Date',
            yaxis_title='Price',
            template='plotly_dark'
        )

        # Display the chart
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error: {str(e)}")
