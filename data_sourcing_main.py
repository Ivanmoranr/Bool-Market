from utils.data_sourcing.scraping import *
from utils.data_sourcing.api_collection import *

url = 'https://www.atmatix.pl/en/patterns/all'
email = 'olmos.edward@gmail.com'
password = 'M@dr!d!23'

eod_api = '64ef583e9a7137.71172021'
eod_base = 'https://eodhistoricaldata.com/api/eod/'
data = 'data/patterns.csv'

df, message = scrape_data(url, email, password)
api_data_collection(eod_api, eod_base, df)

df = pd.read_csv('data/patterns.csv')
data_preparation(df)