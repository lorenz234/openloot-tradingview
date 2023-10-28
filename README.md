# Openloot tradingview
Easily make candlestick charts from historic OpenLoot transactions.

![Slide1](https://github.com/lorenz234/openloot-tradingview/assets/90760534/c2fe7697-bdc9-4f70-bc5f-96e1cff79726)

## How it works
Data is scraped using the Selenium Python WebDriver. This data is then stored in CSV files. From these files, the data is transformed into daily candlestick dataframes. These dataframes are plotted using Plotly and further consolidated into a single dashboard displayed with HTML.
