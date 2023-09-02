import os
import numpy as np
import pandas as pd
def get_real_X_y(noise=False):
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

    if noise:
        for i in range(len(X1)):
            pat = {"0":X2, "1":X3,"2":X4}
            p = np.random.randint(0,3)
            p = str(p)
            num = np.random.randint(0,len(pat[p]))
            X1.append(pat[p][num])
            y1.append([-1,-1,0])

        for i in range(len(X2)):
            pat = {"0":X1, "1":X3,"2":X4}
            p = np.random.randint(0,3)
            p = str(p)
            num = np.random.randint(0,len(pat[p]))
            X2.append(pat[p][num])
            y2.append([-1,-1,0])

        for i in range(len(X3)):
            pat = {"0":X1, "1":X2,"2":X4}
            p = np.random.randint(0,3)
            p = str(p)
            num = np.random.randint(0,len(pat[p]))
            X3.append(pat[p][num])
            y3.append([-1,-1,0])

        for i in range(len(X4)):
            pat = {"0":X1, "1":X2,"2":X3}
            p = np.random.randint(0,3)
            p = str(p)
            num = np.random.randint(0,len(pat[p]))
            X4.append(pat[p][num])
            y4.append([-1,-1,0])


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
