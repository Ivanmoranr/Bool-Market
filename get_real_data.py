import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from synthetic_data import *
from preprocessing import *
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

def data_augmentation(Xs: list[np.ndarray], ys: list[tuple[int, int, int]], noise = False):
    """Creates more patterns based on the list of given ones, optionally with pattern."""
    assert len(Xs) == len(ys)
    new_Xs, new_ys = [], []

    for X, y in zip(Xs, ys):
        size = X.shape[0]
        start, end, pattern = y

        start_margin, end_margin = round(start * (2/3)), round((size - end )*(2/3))
        if start_margin > 4 and end_margin > 4:

            for _ in range(10):
                margin_left = np.random.randint(4, start_margin)
                margin_right = np.random.randint(4, end_margin)
                new_Xs.append(X[start - margin_left : end + margin_right])
                new_ys.append((margin_left, margin_left + end - start, pattern)) # margin_left, margin_right + end - start, pattern

        if noise: # then add also the ones without pattern from start and end
            if start > 9: # then the size is enough to have a time-series before
                new_Xs.append(X[:start])
                new_ys.append((-1,-1,0))

            if size - end > 9:
                new_Xs.append(X[end:])
                new_ys.append((-1,-1,0))

    return new_Xs, new_ys

def upside_down(Xs, ys):
    assert len(Xs) == len(ys)
    new_Xs, new_ys = [], []

    # pat={
    #     "rising_wedge":1,
    #     "falling_wedge":2,
    #     "double_top":3,
    #     "double_bottom":4
    # }
    inverse_patterns = {
        1: 2,
        2: 1,
        3: 4,
        4: 3,
    }
    for X, y in zip(Xs, ys):
        start, end, pattern = y
        if pattern != 0:
            new_pattern = inverse_patterns[pattern]
            l = X - np.max(X[start:end])
            o = -l
            new_Xs.append(o)
            new_ys.append((start, end, new_pattern))

    return new_Xs, new_ys

def augmentation(X1, y1, X2, y2, X3, y3, X4, y4, noise=True):
    x_1, y_1 = data_augmentation(X1, y1, noise=noise)
    x_2, y_2 = data_augmentation(X2, y2, noise=noise)
    x_3, y_3 = data_augmentation(X3, y3, noise=noise)
    x_4, y_4 = data_augmentation(X4, y4, noise=noise)

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


def augmentate(X1, y1, noise=True):
    x_1, y_1 = data_augmentation(X1, y1, noise=noise)
    X_2, Y_2 = upside_down(x_1, y_1)
    X = x_1 + X_2
    y = y_1 + Y_2

    return X, y

def get_data():
    X_ris_wedg, y_ris_wedg, X_fal_wedg, y_fal_wedg, X_d_top, y_d_top, X_d_bottom, y_d_bottom = get_X_y(noise=False, general=False)
    X1, y1, X2, y2, X3, y3, X4, y4 = get_real_X_y(noise=False)
    X = X1 + X2 + X3 + X4 + X_ris_wedg + X_fal_wedg + X_d_top + X_d_bottom
    y = y1 + y2 + y3 + y4 + y_ris_wedg + y_fal_wedg + y_d_top + y_d_bottom
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    X_train, y_train = augmentate(X_train, y_train, noise=True)
    X_test, y_test = augmentate(X_test, y_test, noise=True)
    X_train_preprocessed, y_train_p, y_train_dates = preprocess(X_train, y_train)
    X_test_preprocessed, y_test_p, y_test_dates = preprocess(X_test, y_test)
    return X_train_preprocessed, y_train_p, y_train_dates, X_test_preprocessed, y_test_p, y_test_dates
