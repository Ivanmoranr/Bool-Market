import os
import pandas as pd
import numpy as np


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
        df['Date'] = pd.to_datetime(df['Date'])
    else:
    
        df['Start Date'] = start
        df['End Date'] = end
        df['Pattern'] = pattern
    
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
