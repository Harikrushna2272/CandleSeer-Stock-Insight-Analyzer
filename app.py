import os
import csv
import talib
import yfinance as yf
import pandas as pd
from flask import Flask, request, render_template
from patterns import candlestick_patterns

app = Flask(__name__)

@app.route('/snapshot')
def snapshot():
    os.makedirs('datasets/daily', exist_ok=True)  # Ensure the directory exists

    with open('datasets/symbols.csv') as f:
        for line in f:
            if "," not in line:
                continue
            symbol = line.split(",")[0]
            if "." not in symbol:
                symbol += ".NS"  # Add `.NS` for Indian stocks

            try:
                data = yf.download(symbol, start="2023-01-01", end="2023-08-01")
                if not data.empty:
                    data.to_csv(f'datasets/daily/{symbol}.csv')
                else:
                    print(f"No data found for {symbol}")
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")

    return {"code": "success"}


# Main route to display the scanner and scan for candlestick patterns
@app.route('/')
def index():
    pattern = request.args.get('pattern', False)
    stocks = {}

    # Load symbols and company names
    with open('datasets/symbols.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}

    # If a pattern is selected, analyze stock data
    if pattern:
        for filename in os.listdir('datasets/daily'):
            if filename.endswith('.csv'):
                try:
                    df = pd.read_csv(f'datasets/daily/{filename}')
                    symbol = filename.split('.')[0]

                    # Get the corresponding candlestick pattern function
                    pattern_function = getattr(talib, pattern, None)
                    if not pattern_function:
                        print(f"Invalid pattern function: {pattern}")
                        continue

                    # Apply the pattern function on stock data
                    results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                    last = results.tail(1).values[0]

                    if last > 0:
                        stocks[symbol][pattern] = 'bullish'
                    elif last < 0:
                        stocks[symbol][pattern] = 'bearish'
                    else:
                        stocks[symbol][pattern] = None
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")

    return render_template('index.html', candlestick_patterns=candlestick_patterns, stocks=stocks, pattern=pattern)

if __name__ == "__main__":
    app.run(debug=True)