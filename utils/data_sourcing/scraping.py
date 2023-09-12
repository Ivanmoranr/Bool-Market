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
        time.sleep(5)

    def login(self, email, password):
        """Logs in using email and password"""
        wait = WebDriverWait(self.driver, 10)
        login_btn = wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Log in')]")))
        login_btn.click()

        time.sleep(5)

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

        time.sleep(5)

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
        time.sleep(3)

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
        data_dir = 'data'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        file_path = os.path.join(data_dir, 'patterns.csv')
        df.to_csv(file_path, index=False)

        return df, 'Dataframe successfully saved.'



#-RUN-#
def scrape_data(url, email, password):
    """Scrapes all data from Atmatix page and compiles into a DF"""
    selenium_instance = Selenium()
    selenium_instance.start_maximize(url)
    selenium_instance.login(email, password)

    for page in range(381):
        selenium_instance.page_info()
        print(f"Got page info: {page}")
        selenium_instance.next_page()

    df, message = selenium_instance.convert_data_to_saved_df()
    return df, message