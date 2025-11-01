# Tesla & GameStop Stock and Revenue Dashboard Analysis
# This Python script can be run directly in Jupyter (not a notebook).

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go

# ---------------------- Question 1: Tesla Stock Data ----------------------
tesla = yf.Ticker('TSLA')
tesla_data = tesla.history(period='max')
tesla_data.reset_index(inplace=True)
print('Tesla Stock Data:')
print(tesla_data.head())

# ---------------------- Question 2: Tesla Revenue Data ----------------------
tesla_url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'}
response = requests.get(tesla_url, headers=headers)
html_data = response.text
soup = BeautifulSoup(html_data, 'html.parser')
tables = soup.find_all('table')

# Extract Tesla revenue table
tesla_revenue_table = None
for table in tables:
    if 'Tesla Quarterly Revenue' in table.text:
        tesla_revenue_table = table
        break

if tesla_revenue_table is None:
    raise Exception('Tesla revenue table not found')

# Build Tesla revenue DataFrame
tesla_revenue = pd.DataFrame(columns=['Date', 'Revenue'])
for row in tesla_revenue_table.find_all('tr')[1:]:
    cols = row.find_all('td')
    if len(cols) == 2:
        date = cols[0].text.strip()
        revenue = cols[1].text.strip()
        tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame({'Date':[date], 'Revenue':[revenue]})], ignore_index=True)

tesla_revenue['Revenue'] = tesla_revenue['Revenue'].replace(r'[\$,]', '', regex=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != '']
print('Tesla Revenue Data:')
print(tesla_revenue.head())

# ---------------------- Question 3: GameStop Stock Data ----------------------
gme = yf.Ticker('GME')
gme_data = gme.history(period='max')
gme_data.reset_index(inplace=True)
print('GameStop Stock Data:')
print(gme_data.head())

# ---------------------- Question 4: GameStop Revenue Data ----------------------
gme_url = 'https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue'
response = requests.get(gme_url, headers=headers)
html_data = response.text
soup = BeautifulSoup(html_data, 'html.parser')
tables = soup.find_all('table')

gme_revenue_table = None
for table in tables:
    if 'GameStop Quarterly Revenue' in table.text:
        gme_revenue_table = table
        break

if gme_revenue_table is None:
    raise Exception('GameStop revenue table not found')

# Build GameStop revenue DataFrame
gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])
for row in gme_revenue_table.find_all('tr')[1:]:
    cols = row.find_all('td')
    if len(cols) == 2:
        date = cols[0].text.strip()
        revenue = cols[1].text.strip()
        gme_revenue = pd.concat([gme_revenue, pd.DataFrame({'Date':[date], 'Revenue':[revenue]})], ignore_index=True)

gme_revenue['Revenue'] = gme_revenue['Revenue'].replace(r'[\$,]', '', regex=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != '']
print('GameStop Revenue Data:')
print(gme_revenue.head())

# ---------------------- Question 5: Tesla Dashboard ----------------------
tesla_data['Date'] = pd.to_datetime(tesla_data['Date'])
tesla_revenue['Date'] = pd.to_datetime(tesla_revenue['Date'])

fig = go.Figure()
fig.add_trace(go.Scatter(x=tesla_data['Date'], y=tesla_data['Close'], name='Tesla Stock Price'))
fig.add_trace(go.Bar(x=tesla_revenue['Date'], y=tesla_revenue['Revenue'], name='Tesla Revenue', yaxis='y2'))
fig.update_layout(title='Tesla Stock Price and Revenue', xaxis_title='Date', yaxis=dict(title='Stock Price'), yaxis2=dict(title='Revenue', overlaying='y', side='right'), legend=dict(x=0.1, y=0.9))
fig.show()

# ---------------------- Question 6: GameStop Dashboard ----------------------
gme_data['Date'] = pd.to_datetime(gme_data['Date'])
gme_revenue['Date'] = pd.to_datetime(gme_revenue['Date'])

fig = go.Figure()
fig.add_trace(go.Scatter(x=gme_data['Date'], y=gme_data['Close'], name='GME Stock Price'))
fig.add_trace(go.Bar(x=gme_revenue['Date'], y=gme_revenue['Revenue'], name='GME Revenue', yaxis='y2'))
fig.update_layout(title='GameStop Stock Price and Revenue', xaxis_title='Date', yaxis=dict(title='Stock Price'), yaxis2=dict(title='Revenue', overlaying='y', side='right'), legend=dict(x=0.1, y=0.9))
fig.show()
