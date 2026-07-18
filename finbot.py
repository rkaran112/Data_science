import json
import openai
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf

openai.api_key = open('API_KEY','r').read()

def get_stock_price(ticker):
    return str(yf.Ticker(ticker).history(period='1y').iloc[-1].Close)

def calculate_SMA(ticker,window):
    data = yf.Ticker(ticker).history(period = '1y').Close
    return str(data.rolling(window=window).mean().iloc[-1])

def calculate_EMA(ticker,window):
    data = yf.Ticker(ticker).history(period = '1y').Close
    return str(data.ewm(span=window,adjust=False).mean().iloc[-1])

def calculate_RSI(ticker):
    data = yf.Ticker(ticker).history(period = '1y').Close
    delta = data.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper = 0)
    emma_up = up.ewm(com = 14-1,adjust = False).mean()
    emma_down = down.ewm(com = 14-1,adjust = False).mean()
    rs = emma_up/emma_down
    rsi = 100 - (100 / (1 + rs))
    return str(rsi.iloc[-1])

def calculate_MACD(ticker):
    data = yf.Ticker(ticker).history(period = '1y').Close
    short_EMA = data.ewm(span=12,adjust=False).mean()
    long_EMA = data.ewm(span=26,adjust=False).mean()

    MACD = short_EMA - long_EMA
    signal = MACD.ewm(span=9,adjust = False).mean()
    MACD_histogram = MACD - signal
    return f'{MACD.iloc[-1]},{signal.iloc[-1]},{MACD_histogram.iloc[-1]}'

def plot_stock_price(ticker):
    data = yf.Ticker(ticker).history(period = '1y').Close
    plt.figure(figsize=(10,5))
    plt.plot(data.index,data)
    plt.title(f'{ticker} Stock Price Over Last Year')
    plt.xlabel('Date')
    plt.ylabel('Stock Price {$}')
    plt.grid(True)
    plt.savefig('graph.png')
    plt.close()

def stock_holder_info(ticker):
    share_holders=  yf.Ticker(ticker).get_institutional_holders()
    return share_holders

def news(ticker):
    news = yf.Ticker(ticker).news
    return news

def personal_finance(ticker):
    return f'Personal finance analysis for {ticker} is not yet implemented.'

functions = [
    {
        "name": "get_stock_price",
        "description": "Gets the latest stock price given the ticker symbol of the company.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company. Note FB is renamed to Meta"
                }
            },
            "required": ["ticker"]
        }
    },
    {
        "name": "calculate_SMA",
        "description": "Calculates the simple moving average of the given the ticker symbol of the company",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company. Note FB is renamed to Meta"
                },
                "window": {
                    "type": "integer",
                    "description": "This is the time frame to calculate the SMA value"
                }
            },
            "required": ["ticker", "window"]
        }
    },
    {
        "name": "calculate_EMA",
        "description": "Calculates the Exponential Moving Average (EMA) of a stock over the past year.",
        "parameters": [
            {
                "name": "ticker",
                "type": "string",
                "description": "The stock ticker symbol for a company."
            },
            {
                "name": "window",
                "type": "integer",
                "description": "The time frame (in days) to calculate the EMA value."
            }
        ],
        "returns": "The last calculated EMA value as a string."
    },
    {
        "name": "calculate_RSI",
        "description": "Calculates the Relative Strength Index (RSI) of a stock over the past year.",
        "parameters": [
            {
                "name": "ticker",
                "type": "string",
                "description": "The stock ticker symbol for a company."
            }
        ],
        "returns": "The last RSI value as a string."
    },
    {
        "name": "calculate_MACD",
        "description": "Calculates the Moving Average Convergence Divergence (MACD) for a stock, including the signal and MACD histogram values over the past year.",
        "parameters": [
            {
                "name": "ticker",
                "type": "string",
                "description": "The stock ticker symbol for a company."
            }
        ],
        "returns": "A string representing the last values of MACD, signal, and MACD histogram."
    },
    {
        "name": "plot_stock_price",
        "description": "Plots and saves a graph of the stock price over the last year.",
        "parameters": [
            {
                "name": "ticker",
                "type": "string",
                "description": "The stock ticker symbol for a company."
            }
        ],
        "returns": "Saves the plot as 'graph.png' and does not return a value."
    },
    {
        "name": "stock_holder_info",
        "description": "Retrieves information about the institutional holders of the specified stock.",
        "parameters": [
            {
                "name": "ticker",
                "type": "string",
                "description": "The stock ticker symbol for a company."
            }
        ],
        "returns": "A DataFrame containing details about the stock's institutional holders."
    },
    {
        "name": "news",
        "description": "Fetches the latest news related to the specified stock.",
        "parameters": [
            {
                "name": "ticker",
                "type": "string",
                "description": "The stock ticker symbol for a company."
            }
        ],
        "returns": "A list of news items related to the stock."
    },
    {
        "name": "personal_finance",
        "description": "A placeholder function related to personal finance features for a specified stock.",
        "parameters": [
            {
                "name": "ticker",
                "type": "string",
                "description": "The stock ticker symbol for a company."
            }
        ],
        "returns": "Currently does not return any output."
    }
]

avail_fun = {
    "get_stock_price":get_stock_price,
    "calculate_SMA": calculate_SMA,
    "calculate_EMA": calculate_EMA,
    "calculate_RSI":calculate_RSI,
    "calculate_MACD": calculate_MACD,
    "plot_stock_price": plot_stock_price,
    "stock_holder_info": stock_holder_info,
    "news": news,
    "personal_finance": personal_finance
}

if 'messages' not in st.session_state:
    st.session_state['messages'] = []
    
st.title('Stock Analysis Chatbot Assitant')
user_input = st.text_input('Your input:')

if user_input:
    try:
        st.session_state['messages'].append({'role': 'user', 'content': f'{user_input}'})

        response = openai.completions.create(
            model='gpt-3.5-turbo-0613',  # Corrected model name
            prompt=user_input,
            max_tokens=150,  # Adjust as needed
            # messages=st.session_state['messages'],
            # functions=functions,
            # function_call='auto',
            stream=False
        )
        response_message = response.choices[0].text.strip()

        if response_message.get('function_call'):
            function_name = response_message['function_call']['name']
            function_args = json.loads(response_message['function_call']['arguments'])
            if function_name in ['get_stock_price', 'calculate_RSI', 'calculate_MACD', 'stock_holder_info', 'news',
                                 'personal_finance']:
                args_dict = {'ticker': function_args.get('ticker')}
            elif function_name in ['calculate_SMA', 'calculate_EMA']:
                args_dict = {'ticker': function_args.get('ticker'), "window": function_args.get('window')}

            function_to_call = avail_fun[function_name]
            function_response = function_to_call(**args_dict)

            if function_name == "plot_stock_price":
                st.image('graph.png')
            else:
                st.session_state['messages'].append({'role': 'function', 'name': function_name, 'content': function_response})

                second_response = openai.completions.create(
                    model='gpt-3.5-turbo-0613',
                    prompt=st.session_state['messages'],
                    stream = False
                )
                st.text(second_response.choices[0].text.strip())
                st.session_state['messages'].append({'role': 'assistant', 'content': second_response.choices[0].text.strip()})
        else:
            st.text(response_message)

    except Exception as e:
        st.text(f"Error: {e}")
