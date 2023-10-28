# Openloot tradingview
Easily make candlestick charts from historic OpenLoot transactions.

## How it works
Data is scraped using the Selenium Python WebDriver. This data is then stored in CSV files. From these files, the data is transformed into daily candlestick dataframes. These dataframes are plotted using Plotly and further consolidated into a single dashboard displayed with HTML.