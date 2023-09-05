from src.data_sourcing.data_sourcing import Selenium, DataCollector
from time import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

def main():
    wd = Selenium()
    wd.start_maximize("https://www.atmatix.pl/en/stats")
    wd.login("olmos.edward@gmail.com", "M@dr!d!23")

    total_pages = wd.find_total_pages()
    for num in range(total_pages):
        wd.page_info()
        wd.next_page()
        time.sleep(5)

    wd.convert_data_to_saved_df()
    df, msg = wd.data_preparation()

    eod_api = '64ef583e9a7137.71172021'
    eod_base = 'https://eodhistoricaldata.com/api/eod/'

    dc = DataCollector(eod_api=eod_api, eod_base=eod_base)
    dc.collect_data(df=df)
    data = 'data/patterns.csv'
    dc.update_have_data_column(path_to_df=data)
    dc.rename_similar_patterns()

if __name__ == "__main__":
    main()