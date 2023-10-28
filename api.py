from selenium import webdriver
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import pandas as pd
import json
import time

# change the list to the items you want to scrape
items_to_scrape = ['BT0_Time_Warden_Exotic',
                   'BT0_Armory_Transcendent',
                   'BT0_MysteryBox_Exclusive']

def get_history(archetypeid, page):
    # set up the webdriver
    driver = webdriver.Chrome()
    driver.get(f"https://api.openloot.com/v2/market/items/transaction/history?archetypeId={archetypeid}&page={page}&pageSize=1000")

    time.sleep(2)

    # get the html data
    html_data = driver.page_source

    # close the webdriver
    driver.quit()

    # parse the html data using BeautifulSoup
    soup = BeautifulSoup(html_data, 'html.parser')
    pre_tag = soup.find('pre', {'style': 'word-wrap: break-word; white-space: pre-wrap;'})
    content = pre_tag.string.strip()

    # convert the content to a python dictionary
    data = json.loads(content)
    
    return data

def get_candles_day(df):
    df_sales = df[df['eventName'] == 'sale']
    df_sales['date'] = pd.to_datetime(df_sales['date'])
    df_candles = df_sales.groupby(pd.Grouper(key='date', freq='D')).agg({'price': ['first', 'last', 'min', 'max', 'sum']})
    df_candles.columns = ['Open', 'Close', 'Low', 'High', 'Volume']
    return df_candles

def plot_candles(csv_file):
    df = pd.read_csv(csv_file)
    df_candles = get_candles_day(df)

    # Create a candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=df_candles.index,
                    open=df_candles['Open'],
                    high=df_candles['High'],
                    low=df_candles['Low'],
                    close=df_candles['Close'])])

    # Customize layout
    fig.update_layout(
        title=csv_file,
        yaxis_title='Price',
        xaxis_title='Date',
        xaxis_rangeslider_visible=False  # Hide range slider at the bottom
    )

    # Add volume bars
    fig.add_trace(go.Bar(x=df_candles.index, y=df_candles['Volume'], marker_color='rgba(150, 200, 250, 0.3)', yaxis="y2", name='Volume'))

    # Include a second y-axis for volume bars
    fig.update_layout(
        yaxis2=dict(
            title='Volume',
            titlefont=dict(
                color='rgba(150, 200, 250, 0.8)'
            ),
            tickfont=dict(
                color='rgba(150, 200, 250, 0.8)'
            ),
            overlaying='y',
            side='right',
            position=0.9
        )
    )

    # save the figure
    fig.write_html(csv_file[:-4] + '.html')

### do the scraping and plotting
for item in items_to_scrape:

    # get the data
    page = 1
    while True:
        data = get_history(item, page)
        df = pd.DataFrame(data['items'])
        with open(item + '.csv', 'a') as f:
            df.to_csv(f, header=f.tell()==0, index=False)
        if len(data['items']) < 1000:
            break
        page += 1
        time.sleep(2)

    # plot the data
    plot_candles(item + '.csv')