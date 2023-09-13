## Insatllation:
* create a virtual environment named `bool`
```bash
pyenv virtualenv bool
```

* install dependencies (inside project dir):
```bash
pip install -r requirements.txt
```
* For the TA-lib
(You need to first install requieremnts or the TA-lib installation is going to fail)

```bash
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
```

```bash
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
```
Then, inside project dir (with environment activated):
```bash
pip install -r requirements-extra.txt
```
## Files explained

* one_candle.py

In this file you have the final function, if you want to get a plot use:

plotting(ticker, start_date, end_date,  with_pattern=False, with_candle = False, cdle_patterns=pd.Series(CDL_PATTERNS.keys()).sample(2))

For example:

plotting(ticker, start_date, end_date,  with_pattern=False, with_candle = False, cdle_patterns=pd.Series(CDL_PATTERNS.keys()).sample(2))

That outputs you the following plot:

imagea------------------------------------

* preprocessing.py

Where the preprocessing was done

* graph_generator.py

Where all the synthetic data generation is done

* get_real_data.py

Where we get the data from the csvs stored in data/pattern
