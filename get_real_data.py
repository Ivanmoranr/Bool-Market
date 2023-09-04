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

def data_augmentation(X1, y1, noise = False):
    x_1=[]
    y_1=[]
    if noise:
        for i in range(len(X1)):
            if y1[i][0]>9:
                x_1.append(X1[i][:y1[i][0]])
                y_1.append((-1,-1,0))
        for i in range(len(X1)):
            if (len(X1)-y1[i][1])>9:
                x_1.append(X1[i][y1[i][1]:])
                y_1.append((-1,-1,0))
    for i in range(len(X1)):
        for i in range(10):
            if round(y1[i][0]/3)>3:
                num = np.random.randint(0,round(y1[i][0]/3))
                num_2 = np.random.randint(0,round(y1[i][0]/3))
                x_1.append(X1[i][(y1[i][0]-num):(y1[i][1]+num_2)])
                y_1.append((num, num_2+y1[i][1], y1[i][2]))
    return x_1, y_1

def upside_down(x_1, y_1):
    X_1=[]
    Y_1=[]
    pat={"rising_wedge":1,
            "falling_wedge":2,
            "double_top":3,
            "double_bottom":4
        }

    for i in range(len(x_1)):
        if y_1[i][2] != 0:
            if y_1[i][2] == 1:
                num=2
            elif y_1[i][2] == 2:
                num=1
            elif y_1[i][2] == 3:
                num=4
            elif y_1[i][2] == 4:
                num=3
            l = x_1[i] - np.max(x_1[i][y_1[i][0]:y_1[i][1]])
            o = -l
            X_1.append(o)
            Y_1.append((y_1[i][0], y_1[i][1], num))

    return X_1, Y_1

def augmentation(X1, y1, X2, y2, X3, y3, X4, y4):
    x_1, y_1 = data_augmentation(X1, y1)
    x_2, y_2 = data_augmentation(X2, y2)
    x_3, y_3 = data_augmentation(X3, y3)
    x_4, y_4 = data_augmentation(X4, y4)

    X_2, Y_2 = upside_down(x_1, y_1)
    X_1, Y_1 = upside_down(x_2, y_2)
    X_4, Y_4 = upside_down(x_3, y_3)
    X_3, Y_3 = upside_down(x_4, y_4)

    X1 = x_1+X_1
    X2 = x_2+X_2
    X3 = x_3+X_3
    X4 = x_4+X_4

    y1 = y_1 + Y_1
    y2 = y_2 + Y_2
    y3 = y_3 + Y_3
    y4 = y_4 + Y_4

    return X1, y1, X2, y2, X3, y3, X4, y4
