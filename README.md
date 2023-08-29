# Bool-Market
Data Science Final Project Batch 1327

# Candlesticks Explained

## Single Candlesticks

### Doji
![Doji](images/candlesticks/doji.jpeg)

**Characterised by:** the opening and closing price being the same.

**Signifies:**indecision in the market. If it occurs in and uptrend or a downtrend, it means the trend is likely to reverse.

**Logic:**20 * ABS(O - C) <= H - L

### Dragonfly Doji
![Doji](images/candlesticks/dragonfly_doji.jpeg)
**Characterised by:** the same open, close and high price during the trading window. It is the bullish version of the Gravestone Doji.

**Signifies:**resistance of buyers and their attempts to push the market up.

**Logic:**50 * ABS(O - C) <= H - L AND STOC1 >= 70 AND H - L >= AVGH10 - AVGL10 AND L = MINL10

### Gravestone Doji
![Gravestone](images/candlesticks/gravestone_doji.png)
**Characterised by:** very similar opening, closing, and low prices during the tradin window.

**Signifies:**The long upper shadow is an indication that the market is testing a powerful supply or resistance area.

**Logic:**100 * ABS(O - C) <= H - L AND STOC1 <= 5 AND H > L AND 10 * L <= 3 * H1 + 7 * L1 AND H - L >= AVGH10-AVGL10

### Hammer
![Hammer](images/candlesticks/hammer.jpeg)
**Characterised by:** a short body, and long lower shadows.

**Signifies:**That sellers were unsuccessful in their attempt to push the price lower. When at the bottom of a downtrend, it signifies a reversal.

**Logic:**5 * ABS(C - O) <= H - L AND 10 * ABS(O - C) >= H - L AND 2 * O >= H + L AND STOC1 >= 50 AND (20 * O >= 19 * H + L OR STOC1 >= 95) AND 10 * (H - L) >= 8 * (AVGH10 - AVGL10) AND L = MINL5 AND H > L

### Spinning Top / Bottom
![Spinning](images/candlesticks/spinning.jpeg)
**Characterised by:** a short body, but with shadows that are at least twice the size of the body.

**Signifies:**That both buyers and sellers tried to push the price, but that it closed close to the opening price.

**Logic:**ABS(C - O) / (H - L) < BodyThreshold AND MAX(O, C) - L > ShadowThreshold AND H - MIN(O, C) > ShadowThreshold

### Marubozo
![Marubozu](images/candlesticks/Marabozu.jpeg)
**Characterised by:**a body with no high or low shadows.

**Signifies:**An extremely strong buying or selling pressure in the previous trading period.

**Logic:**H - L = ABS(O - C) AND H - L > 3 * AVG(ABS(O - C), 15) / 2

#### Opening Marubozu
![Opening_Marubozu](images/candlesticks/opening_marubozu.png)
**Characterised by:**the opening price occurring at the high or low of the trading window.

**Signifies:**That as soon as the bell rang, the bears or the bulls took charge and pushed the prices in the direction for the rest of the window.

**Logic:**(L = O OR O = H) AND H - L > ABS(O - C) AND ABS(O - C) > 3 * AVG(ABS(O - C), 15) / 2

#### Closing Marubozu
![Closing_Marubozu](images/candlesticks/closing_marubozu.png)
**Characterised by:**the closing price being either the high or the low for the trading window.

**Signifies:**That not only did the prices maintain the move in a single direction after initial jitters, in fact the participants maintained the sentiments until the end moment of the trading window.

**Logic:**(L = C OR C = H) AND H - L > ABS(O - C) AND ABS(O - C) > 3 * AVG(ABS(O - C), 15) / 2
