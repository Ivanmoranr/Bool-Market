import pandas as pd
import yfinance as yf
import talib
from cdl_patterns import CDL_PATTERNS

import plotly.graph_objs as go
import ipywidgets as widgets
from ipywidgets import interactive
from IPython.display import display

def create_data_stock(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date).reset_index()
    except Exception as e:
        return f"Error: {str(e)}"

    for key, pattern_func in CDL_PATTERNS.items():
        calculated_value = pattern_func(data['Open'], data['High'], data['Low'], data['Close'])
        if calculated_value is not None:
            data[key] = calculated_value

    return data


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

    display(widgets.VBox([chkbox for chkbox in checkboxes.values()] + [fig]))
