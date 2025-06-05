import plotly.express as px 
import numpy as np

# function rto plot interative potly charts
def interactive_plot(df):
    fig = px.line()
    for i in df.columns[1:]:
        fig.add_scatter(x = df['Date'], y = df[i], name = i)
        
    fig.update_layout(width = 450, margin = dict(l=20,t=50,b=20),legend = dict(orientation = 'h', yanchor = 'bottom', y = 1.02, xanchor = 'right', x = 1, ))
    
    return fig 

# function to normalise the prices based on the initial price
# we'll get to know how much the price has increased/decreased compared to initial price
def normalize(df_2):
    df = df_2.copy()
    for i in df.columns[1:]:
        df[i] = df[i]/df[i][0]
    return df


# function to calculate daily returns
def daily_return(df):
    df_daily_return = df.copy()
    for col in df.columns[1:]:
        df_daily_return[col] = df[col].pct_change().fillna(0) * 100
    return df_daily_return


# function to calculate beta 
def calculate_beta(stocks_daily_return, stock):
    rm = stocks_daily_return['sp500'].mean()*252
    b, a = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return[stock], 1)
    return b,a
    