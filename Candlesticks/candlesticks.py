import pandas as pd
import yfinance as yf
import talib
from cdl_patterns import CDL_PATTERNS

import plotly.graph_objs as go
import ipywidgets as widgets
from ipywidgets import interactive
from IPython.display import display

def get_ticker_info(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date).reset_index()
        ticker_info = {
            "symbol": ticker,
            "start_date": start_date,
            "end_date": end_date,
            "num_rows": len(data)
        }
        return ticker_info
    except Exception as e:
        return {"error": str(e)}

def get_candlestick_patterns(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date).reset_index()
        candlestick_data = {}

        for key, pattern_func in CDL_PATTERNS.items():
            calculated_value = pattern_func(data['Open'], data['High'], data['Low'], data['Close'])
            if any(calculated_value):
                candlestick_data[key] = calculated_value

        return candlestick_data
    except Exception as e:
        return {"error": str(e)}


def create_data_stock(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date).reset_index()

    #candlestick_data = {}  # Initialize an empty dictionary to store candlestick data

    for key, pattern_func in CDL_PATTERNS.items():
        calculated_value = pattern_func(data['Open'], data['High'], data['Low'], data['Close'])
        if any(calculated_value):  # Check if any pattern results are present
            data[key] = calculated_value  # Add the pattern to the dictionary

    return data  # Return the candlestick data as a dictionarys

def create_candlestick_chart(data_apple_cdl, patterns):
    # Filter out patterns that are not present in the data
    present_patterns = {}
    for pattern_name, pattern_code in patterns.items():
        pattern_results = pattern_code(data_apple_cdl['Open'], data_apple_cdl['High'], data_apple_cdl['Low'], data_apple_cdl['Close'])
        if any(pattern_results):
            present_patterns[pattern_name] = pattern_code

    # Create Candlestick Chart
    fig = go.FigureWidget(data=[
        go.Candlestick(
            x=data_apple_cdl['Date'],
            open=data_apple_cdl['Open'],
            high=data_apple_cdl['High'],
            low=data_apple_cdl['Low'],
            close=data_apple_cdl['Close']
        )
    ])

    checkboxes = {}

    # Create checkbox widgets for each present pattern
    for pattern_name, pattern_code in present_patterns.items():
        checkbox = widgets.Checkbox(
            description=pattern_name,
            value=False,
            inline=True
        )
        checkboxes[pattern_name] = checkbox

    def update_fig(change):
        annotations = []

        for pattern_name, chkbox in checkboxes.items():
            if chkbox.value:
                pattern_code = present_patterns[pattern_name]
                pattern_results = pattern_code(data_apple_cdl['Open'], data_apple_cdl['High'], data_apple_cdl['Low'], data_apple_cdl['Close'])
                for index, row in data_apple_cdl.iterrows():
                    if pattern_results[index] != 0:
                        annotation = {
                            'x': row['Date'],
                            'y': row['High'],
                            'text': pattern_name,
                            'showarrow': True,
                            'arrowhead': 2,
                            'ax': 0,
                            'ay': -40
                        }
                        annotations.append(annotation)

        with fig.batch_update():
            fig.layout.annotations = annotations
            fig.update_layout(xaxis_rangeslider_visible=False)

    fig.update_layout(
        title='Candlestick Chart with candle pattern Annotations',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark'
    )

    for chkbox in checkboxes.values():
        chkbox.observe(update_fig, names='value')

    return display(widgets.VBox([chkbox for chkbox in checkboxes.values()] + [fig]))

def create_candle_chart (data, pattern):
    # Assuming you have already created the figure using your stock data
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'])])


    for index, row in data.iterrows():
        if row[pattern]:
            annotation = {
                'x': data['Date'],
                'y': row['High'],
                'text': pattern,
                'showarrow': True,
                'arrowhead': 2,
                'ax': 0,
                'ay': -40
            }
            fig.add_annotation(annotation)

    fig.update_layout(title=f'Candlestick Chart with {pattern} Annotations',
                    xaxis_title='Date',
                    yaxis_title='Price',
                    template='plotly_dark')

    return fig
