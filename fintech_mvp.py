import streamlit as st
import requests
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import os
from dotenv import load_dotenv
import streamlit.components.v1 as components

# Load the environment variables from the .env file
load_dotenv()

# Retrieve the keys
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Initialize Claude API with the loaded key
anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)


def get_stock_news(stock_name):
    response = requests.get(f"https://newsapi.org/v2/everything?q={stock_name}&apiKey={NEWS_API_KEY}")
    return response.json()["articles"][:10]

def ask_claude(stock_info, query):
    prompt = f"{HUMAN_PROMPT} {stock_info} {query}{AI_PROMPT}"
    completion = anthropic.completions.create(
        model="claude-2",
        max_tokens_to_sample=300,
        prompt=prompt,
    )
    return completion.completion

def fintech_app():
    st.title("Algabay AI")

    # Dictionary of famous Indian stock companies with their symbols
    stocks_with_symbols = {
        "Reliance Industries": "RELIANCE",
        "Tata Consultancy Services": "TCS",
        "HDFC Bank": "HDFCBANK",
        "Infosys": "INFY",
        "Hindustan Unilever": "HUL",
        "ICICI Bank": "ICICIBANK",
        "State Bank of India": "SBIN",
        "Bajaj Finance": "BAJFINANCE",
        "Kotak Mahindra Bank": "KOTAKBANK",
        "Bharti Airtel": "BHARTIARTL",
    }

    # Dropdown for stock selection
    selected_stock = st.selectbox(
        'Select a stock:',
        options=list(stocks_with_symbols.keys())
    )

    if selected_stock:
        st.session_state.selected_stock = selected_stock
        stock_symbol = stocks_with_symbols[selected_stock]  # Retrieve the symbol for the selected stock
    else:
        stock_symbol = "NZDCAD" 
    tradingview_widget_code = f"""
        <div class="tradingview-widget-container">
            <div id="tradingview_{stock_symbol}"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script type="text/javascript">
            new TradingView.widget(
                {{
                    "container_id": "tradingview_{stock_symbol}",
                    "symbol": "{stock_symbol}",
                    "interval": "D",
                    "width": "100%",
                    "height": "400",
                    // Additional widget options
                }}
            );
            </script>
        </div>
        """
    components.html(tradingview_widget_code, height=450)


    col1, col2 = st.columns(2)
    # Stock information to prepend to Claude's prompt
    stock_info = ""
    if st.session_state.selected_stock:  # Updated reference here
        stock_info = f"Information about following company: {st.session_state.selected_stock}. Strictly adhere to relevancy of the company and keep the answer short and precise."


    # Display stock news in the left column
    with col1:
        st.subheader("Latest News")
        if st.session_state.selected_stock:  # Updated reference here
            news_articles = get_stock_news(st.session_state.selected_stock)  # Updated reference here
        else:
            # Display generic news if no stock selected
            news_articles = get_stock_news("Nifty 50") + get_stock_news("Sensex")
        for article in news_articles:
            st.write(f"**{article['title']}**")
            st.write(article["description"])
            st.write(f"[Read more]({article['url']})")
            st.write("---")

    # AI Assistant Interaction in the right column
    with col2:
        st.subheader("Ask Algabay AI")
        user_query = st.text_input("Type your question about the stock:")
        if user_query:
            response = ask_claude(stock_info, user_query)
            st.write(response)
    
        

if __name__ == "__main__":
    fintech_app()
