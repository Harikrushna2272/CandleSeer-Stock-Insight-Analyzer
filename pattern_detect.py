import talib
import yfinance as yf

# Download historical data for the Nifty 50 index
data = yf.download("^NSEI", start="2020-01-01", end="2020-08-01")  # ^NSEI is the Yahoo Finance symbol for Nifty 50

# Detect candlestick patterns
data['Morning Star'] = talib.CDLMORNINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])
data['Evening Star'] = talib.CDLEVENINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])
data['Doji'] = talib.CDLDOJI(data['Open'], data['High'], data['Low'], data['Close'])
data['Hammer'] = talib.CDLHAMMER(data['Open'], data['High'], data['Low'], data['Close'])
data['Shooting Star'] = talib.CDLSHOOTINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])
data['Engulfing'] = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])
data['Harami'] = talib.CDLHARAMI(data['Open'], data['High'], data['Low'], data['Close'])
data['Three Black Crows'] = talib.CDL3BLACKCROWS(data['Open'], data['High'], data['Low'], data['Close'])
data['Piercing Pattern'] = talib.CDLPIERCING(data['Open'], data['High'], data['Low'], data['Close'])

# Filter the data to show only days with any candlestick patterns detected
candlestick_patterns = ['Morning Star', 'Evening Star', 'Doji', 'Hammer', 'Shooting Star', 
                        'Engulfing', 'Harami', 'Three Black Crows', 'Piercing Pattern']
detected_patterns = data[(data[candlestick_patterns] != 0).any(axis=1)]

# Print the rows with detected patterns
print(detected_patterns)
