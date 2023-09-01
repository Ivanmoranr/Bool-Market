import os
import numpy as np
import pandas as pd
def get_real_X_y():
    pattern_list = ["rising_wedge", "falling_wedge", "double_top", "double_bottom"]
    X1=[]
    y1=[]
    X2=[]
    y2=[]
    X3=[]
    y3=[]
    X4=[]
    y4=[]
    for pattern in pattern_list:
        directory_path = f'data/patterns/{pattern}'
        if pattern == "rising_wedge":
            for root, dirs, files in os.walk(directory_path):
                for filename in files:
                    df = pd.read_csv(f"data/patterns/rising_wedge/{filename}")
                    X1.append(np.array(df[["Open", "High", "Low", "Close"]]))
                    y1.append(tuple(df.iloc[0][["Start Date", "End Date", "Pattern"]]))
        if pattern == "falling_wedge":
            for root, dirs, files in os.walk(directory_path):
                for filename in files:
                    df = pd.read_csv(f"data/patterns/falling_wedge/{filename}")
                    X2.append(np.array(df[["Open", "High", "Low", "Close"]]))
                    y2.append(tuple(df.iloc[0][["Start Date", "End Date", "Pattern"]]))
        if pattern == "double_top":
            for root, dirs, files in os.walk(directory_path):
                for filename in files:
                    df = pd.read_csv(f"data/patterns/double_top/{filename}")
                    X3.append(np.array(df[["Open", "High", "Low", "Close"]]))
                    y3.append(tuple(df.iloc[0][["Start Date", "End Date", "Pattern"]]))
        if pattern == "double_bottom":
            for root, dirs, files in os.walk(directory_path):
                for filename in files:
                    df = pd.read_csv(f"data/patterns/double_bottom/{filename}")
                    X4.append(np.array(df[["Open", "High", "Low", "Close"]]))
                    y4.append(tuple(df.iloc[0][["Start Date", "End Date", "Pattern"]]))

    return X1, y1, X2, y2, X3, y3, X4, y4

def get_up_down(patterns=["uptrend","downtrend"]):
    X1=[]
    y1=[]
    X2=[]
    y2=[]
    for pattern in patterns:
        directory_path = f'data/patterns/{pattern}'
        if pattern == "uptrend":
            for root, dirs, files in os.walk(directory_path):
                for filename in files:
                    df = pd.read_csv(f"data/patterns/uptrend/{filename}")
                    X1.append(np.array(df[["Open", "High", "Low", "Close"]]))
                    y1.append(tuple(df.iloc[0][["Start Date", "End Date", "Pattern"]]))
        if pattern == "downtrend":
            for root, dirs, files in os.walk(directory_path):
                for filename in files:
                    df = pd.read_csv(f"data/patterns/downtrend/{filename}")
                    X2.append(np.array(df[["Open", "High", "Low", "Close"]]))
                    y2.append(tuple(df.iloc[0][["Start Date", "End Date", "Pattern"]]))

    return X1, y1, X2, y2
