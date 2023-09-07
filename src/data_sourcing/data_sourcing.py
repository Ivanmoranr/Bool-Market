from datetime import datetime
import pandas as pd
from io import StringIO
import time
import os
import requests


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class Selenium:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.info = []

    def start_maximize(self, url):
        """Starts Selenium driver and maximizes the window"""
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(10)

    def login(self, email, password):
        """Logs in using email and password"""
        wait = WebDriverWait(self.driver, 10)
        login_btn = wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Log in')]")))
        login_btn.click()

        time.sleep(10)

        email_entry = wait.until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "/html/body/div[2]/div/div[1]/div/div/div[2]/form/fieldset/div[1]/div/input")))
        email_entry.send_keys(email)

        pass_entry = wait.until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "/html/body/div[2]/div/div[1]/div/div/div[2]/form/fieldset/div[2]/div/input")))
        pass_entry.send_keys(password)

        log_btn = wait.until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "/html/body/div[2]/div/div[1]/div/div/div[2]/form/fieldset/div[4]/button")))
        log_btn.click()

        time.sleep(10)

    def find_total_pages(self):
        wait = WebDriverWait(self.driver, 10)
        anchor = wait.until(expected_conditions.visibility_of_element_located(
            (By.XPATH, "/html/body/div[1]/div/div[6]/div[2]/div[1]/div[3]/div[2]/div/ul/li[8]/a")))
        return anchor.text

    def page_info(self):
        """Extracts all information from the tabular page and appends it to the 'info' list"""
        page_table_rows = self.driver.find_elements(By.XPATH, "//table//tr")
        for row in page_table_rows:
            td_elements = row.find_elements(By.TAG_NAME, "td")
            if len(td_elements) >= 10:
                children_to_extract = [2, 3, 4, 6, 9]
                extracted_children = [td_elements[i].text for i in children_to_extract]
                self.info.append(extracted_children)
        return self.info

    def next_page(self):
        """Navigates to the next page"""
        wait = WebDriverWait(self.driver, 10)
        next_page_btn = wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Next')]")))
        self.driver.execute_script("arguments[0].scrollIntoView();", next_page_btn)
        next_page_btn.click()

    def convert_data_to_saved_df(self):
        """Converts the collected 'info' data to a DataFrame"""
        columns = ['Company', 'Pattern', 'Width', 'End Date', 'Breakout Date']

        data_to_add = []

        for row in self.info:
            company = row[0]
            pattern = row[1]
            width = row[2]
            end_date = row[3]
            breakout_date = row[4]

            data_to_add.append({
                'Company': company,
                'Pattern': pattern,
                'Width': width,
                'End Date': end_date,
                'Breakout Date': breakout_date
            })

        df = pd.DataFrame(data_to_add, columns=columns)
        df.to_csv('data/patterns.csv', index=False)
        return df, 'Dataframe successfully saved.'

    def data_preparation(self):
        """Performs data preparation on the collected 'info' data"""
        if not self.info:
            raise ValueError("No data to prepare. Call 'page_info' to collect data first.")

        df = pd.DataFrame(self.info, columns=['Company', 'Pattern', 'Width', 'End Date', 'Breakout Date'])

        # Data preparation steps
        ticker_with_parentheses = df['Company'].str.extract(r'(?<=\()(\w+)(?=\))')
        ticker_without_parentheses = df['Company'].str.extract(r'^(\w+)$')
        df['Ticker'] = ticker_with_parentheses.fillna(ticker_without_parentheses)

        df['End Date'] = pd.to_datetime(df['End Date'])
        df['Width'] = pd.to_numeric(df['Width'])
        df['API Start Date'] = df.apply(lambda row: row['End Date'] - pd.DateOffset(days=row['Width'] * 4), axis=1)
        df['API End Date'] = df.apply(lambda row: row['End Date'] + pd.DateOffset(days=row['Width'] * 3), axis=1)

        df['Start Date'] = df.apply(lambda row: row['End Date'] - pd.DateOffset(days=row['Width']), axis=1)

        df['Start Date'] = pd.to_datetime(df['Start Date'])
        df['API Start Date'] = pd.to_datetime(df['API Start Date'])
        df['API End Date'] = pd.to_datetime(df['API End Date'])

        df['Pattern'] = df['Pattern'].apply(lambda x: '_'.join(x.lower().split()))

        df.loc[df['Pattern'] == '3_rising_valleys', 'Pattern'] = 'rising_wedge'
        df.loc[df['Pattern'] == 'asc._broad._triangle', 'Pattern'] = 'ascending_triangle'
        df.loc[df['Pattern'] == 'desc._broad._triangle', 'Pattern'] = 'descending_triangle'
        df.loc[df['Pattern'] == 'asc._broad.wedge', 'Pattern'] = 'rising_wedge'
        df.loc[df['Pattern'] == 'desc._broad._wedge', 'Pattern'] = 'falling_wedge'

        df['Have Data'] = False

        df = df[['Ticker', 'Company', 'Pattern', 'Start Date', 'End Date', 'Width', 'API Start Date', 'API End Date',
                 'Breakout Date', 'Have Data']]

        df.to_csv('data/patterns.csv', index=False)

        return df, 'Dataframe successfully processed and saved.'





class DataCollector:
    def __init__(self, eod_api, eod_base):
        self.eod_api = eod_api
        self.eod_base = eod_base

    def time_to_string(self, date):
        return date.strftime('%Y-%m-%d')

    def collect_data(self, df):
        indices = ['SWIG80', 'WIG20', 'WIG30', 'WIG', 'WIG140', 'MWIG140', 'WIG20EUR', 'WIG20USD', 'WIG_BANKI', 'WIG_CHEMIA', 'WIGTECH', 'WIG_POLAND', 'WIG_MEDIA', 'WIG_ODZIEZ']
        for index, row in df.iterrows():
            if row['Ticker'] in indices:
                symbol = row['Ticker']
                exchange = 'INDX'
            else:
                if pd.isna(row['Ticker']):
                    symbol = row['Company']
                    exchange = 'INDX'
                else:
                    symbol = row['Ticker']
                    exchange = 'WAR'

            from_date = self.time_to_string(row['API Start Date'])
            to_date = self.time_to_string(row['API End Date'])

            url = f'{self.eod_base}{symbol}.{exchange}?'

            params = {
                'api_token': self.eod_api,
                'period': 'd',
                'from': from_date,
                'to': to_date
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                csv_content = response.text
                sub_df = pd.read_csv(StringIO(csv_content))

                pattern = row['Pattern']
                dataframe_name = f"{index}_{symbol}_{pattern}.csv"
                root_path = os.getcwd()
                data_directory = os.path.join(root_path, 'data', 'patterns', f'{pattern}')

                os.makedirs(data_directory, exist_ok=True)

                sub_df.to_csv(os.path.join(data_directory, dataframe_name), index=False)

                df.at[index, 'Have Data'] = True
                print(f"Saved DataFrame '{dataframe_name}'")
            else:
                print(f"API request for index {index} with Ticker: {row.Ticker} was not successful.")


    def update_have_data_column(self, path_to_df):
        df = pd.read_csv(path_to_df)
        for index, row in df.iterrows():
            if pd.isna(row['Ticker']):
                ticker = row.Company
                id_num = index
                pattern = row.Pattern
            else:
                ticker = row.Ticker
                id_num = index
                pattern = row.Pattern

            folder_name = f'data/patterns/{pattern}'
            f_name = f'{index}_{ticker}_{pattern}.csv'
            f_path = os.path.join(folder_name, f_name)

            if os.path.exists(f_path):
                df.at[index, 'Have Data'] = True
            else:
                df.at[index, 'Have Data'] = False

    def rename_similar_patterns(self):
        old_names = ['asc._broad._wedge', 'desc._broad._wedge']
        new_names = ['rising_wedge', 'falling_wedge']

        for index, pattern in enumerate(old_names):
            old_directory_path = f'data/patterns/{pattern}'
            new_directory_path = f'data/patterns/{new_names[index]}'

            for root, dirs, files in os.walk(old_directory_path):
                for filename in files:
                    if filename.endswith(f'{pattern}.csv'):
                        old_file_path = os.path.join(root, filename)
                        new_file_path = os.path.join(new_directory_path,
                                                     filename.replace(f'{pattern}.csv', f'{new_names[index]}.csv'))

                        os.rename(old_file_path, new_file_path)
                        print(f'Renamed and moved: {old_file_path} -> {new_file_path}')

            # Check if the old directory is empty and delete it
            if not os.listdir(old_directory_path):
                os.rmdir(old_directory_path)
                print(f'Deleted empty folder: {old_directory_path}')






