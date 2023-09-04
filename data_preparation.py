import os
import pandas as pd
import numpy as np
from pathlib import Path
from tensorflow.keras.preprocessing.sequence import pad_sequences
from synthetic_data import *


def extract_info(filename):
    """Takes a filename and extracts the start date, end date and pattern"""
    index_num = int(filename.split('_')[0])
    
    pattern_df = pd.read_csv('data/patterns.csv')
    row = pattern_df.iloc[index_num] 
    
    if not row.empty:
        start_date = row['Start Date']
        end_date = row['End Date']
        pattern = row['Pattern']
        
        return start_date, end_date, pattern
    
    
def start_date(df):
    """Checks the start date is present, and finds the closest start date available"""
    start_date = df['Start Date'].iloc[0]
   
    while df[df.Date ==str(start_date).replace(" 00:00:00","")].shape[0] == 0:
        start_date -= pd.Timedelta(days=1)
        
   
    start = df[df.Date == str(start_date).replace(" 00:00:00","")].index[0]
        
    return start


def end_date(df):
    """Checks the end date is present, and finds the closest end date available"""
    end_date = df['End Date'].iloc[0]
   
    while df[df.Date ==str(end_date).replace(" 00:00:00","")].shape[0] == 0:
        end_date += pd.Timedelta(days=1)
        
   
    end = df[df.Date == str(end_date).replace(" 00:00:00","")].index[0]
        
    return end


def preprocess_csv(filename):
    """
    Takes a filename and:
    * drops adjusted Close and Volume columns
    * Adds Start Date. End Date and Pattern columns
    * Converts verbose patterns to numerical
    * Finds closest Start and End dates
    * Saves csv to existing path
    """
    patterns_dict = {
        "rising_wedge": 1,
        "falling_wedge": 2,
        "double_top": 3,
        "double_bottom": 4
    }
    
    start, end, pattern = extract_info(filename)     
    
    path_to_file = f'data/patterns/{pattern}/{filename}'
    df = pd.read_csv(path_to_file)
    

    if 'Volume' in df.columns and 'Adjusted_close' in df.columns:
        cols_to_drop = ['Adjusted_close', 'Volume']
        df.drop(columns=cols_to_drop, inplace=True)
    
    if pattern not in patterns_dict:
        df['Start Date'] = -1
        df['End Date'] = -1
        df['Pattern'] = 0
        df['Pattern Present'] = 0
        df['Date'] = pd.to_datetime(df['Date'])
    else:
    
        df['Start Date'] = start
        df['End Date'] = end
        df['Pattern'] = pattern
        df['Pattern Present'] = 1
    
        df['Date'] = pd.to_datetime(df['Date'])
        df['Start Date'] = pd.to_datetime(df['Start Date'])
        df['End Date'] = pd.to_datetime(df['End Date'])
    
    
        df['Pattern'] = df['Pattern'].map(patterns_dict)
    
        start = start_date(df)
        df['Start Date'] = start
        end = end_date(df)
        df['End Date'] = end

    
    df.to_csv(path_to_file, index=False)
    print(f'{path_to_file} saved')
    return df


def convert_csv(pattern_list):
    """Takes a list of patterns and processes all csv's"""
    for pattern in pattern_list:
        directory_path = f'data/patterns/{pattern}'
        for root, dirs, files in os.walk(directory_path):
            for filename in files:
                preprocess_csv(filename)
                

def extract_file_list():
    """Returns a list of all pattern names in data/patterns folder"""
    pattern_list = []
    directory_path = f'data/patterns'
    for root, dirs, files in os.walk(directory_path):
        for folder in dirs:
            pattern_list.append(folder)
    return pattern_list[:-2]


def real_data_pattern(pattern, model_type):
    """
    Takes a pattern name and returns X and y
    model_type: categorise(pattern present or not) or full(pattern location detection)
    """
    DATA_PATH_ = Path(f"data/patterns/{pattern}")
    DATA_PATH_.exists()

    data = {filepath.stem: pd.read_csv(filepath) for filepath in DATA_PATH_.glob("*.csv")}

    X_real = []
    y_real = []
    
    if model_type == "full":
        for key, df in data.items():
            X_real.append(df[['Open', 'High', 'Low', 'Close']].values)
            y_real.append(df.loc[0, ['Start Date', 'End Date', 'Pattern']].values)
            
    elif model_type == 'categorise':
        for key, df in data.items():
            X_real.append(df[['Open', 'High', 'Low', 'Close']].values)
            y_real.append(df.loc[0, ['Pattern Present']].values)

    return X_real, y_real


def synthetic_data(X_real, pattern, model_type):
    """Takes the real X data and pattern and returns the required amount of synthetic data"""
    amount_40 = int(len(X_real) * 0.4)

    X_synthetic, y_synthetic = gen_x_y(l=amount_40, pattern=pattern, noise=True, general=False, model_type=model_type)

    return X_synthetic, y_synthetic


def real_data_no_pattern(X_real, pattern, model_type):
    """Takes the real X data and pattern being tested and returns 25% of the real data with no pattern"""

    patterns_dict = {
        "rising_wedge": 'downtrend',
        "falling_wedge": 'uptrend',
        "double_top": 'support',
        "double_bottom": 'support'
    }

    amount_25 = int(len(X_real) * 0.25)

    pattern_type = patterns_dict.get(pattern, pattern)

    DATA_PATH = Path(f"data/patterns/{pattern_type}")
    
    if DATA_PATH.exists():
        data = {filepath.stem: pd.read_csv(filepath) for filepath in DATA_PATH.glob("*.csv")}
        
        data = {key: df[:amount_25] for key, df in data.items()}

        X_no_pattern = []
        y_no_pattern = []

        if model_type == 'full':
            for key, df in data.items():
                X_no_pattern.append(df[['Open', 'High', 'Low', 'Close']].values)
                y_no_pattern.append(df.loc[0, ['Start Date', 'End Date', 'Pattern']].values)
            
        elif model_type == 'categorise':
            for key, df in data.items():
                X_no_pattern.append(df[['Open', 'High', 'Low', 'Close']].values)
                y_no_pattern.append(df.loc[0, ['Pattern Present']].values)
    
    return X_no_pattern, y_no_pattern


def join_data(real_pattern, synthetic, real_no_pattern):
    """Takes all data and returns a combined list of arrays"""
    return real_pattern + synthetic + real_no_pattern


def pad_arrays(X, dtype='float32', padding='post', value=-100):
    """Takes a list of arrays and pads to the minimum required length"""
    return pad_sequences(X, dtype=dtype, padding=padding, value=value)