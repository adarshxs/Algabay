import streamlit as st
import requests
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import os
from dotenv import load_dotenv

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

    # List of famous Indian stock companies
    stocks = [
        "Reliance Industries",
        "Tata Consultancy Services",
        "HDFC Bank",
        "Infosys",
        "Hindustan Unilever",
        "ICICI Bank",
        "State Bank of India",
        "Bajaj Finance",
        "Kotak Mahindra Bank",
        "Bharti Airtel",
    ]

    # Number of columns
    num_columns = 5

    # Display buttons for stock selection in grid layout
    if "selected_stock" not in st.session_state:
        st.session_state.selected_stock = None

    # Display buttons for stock selection in grid layout
    for i in range(0, len(stocks), num_columns):
        row_stocks = stocks[i:i + num_columns]
        row_columns = st.columns(len(row_stocks))
        for j, stock in enumerate(row_stocks):
            if row_columns[j].button(stock):
                st.session_state.selected_stock = stock

    # Stock information to prepend to Claude's prompt
    stock_info = ""
    if st.session_state.selected_stock:  # Updated reference here
        stock_info = f"Information about following company: {st.session_state.selected_stock}. Strictly adhere to relevancy of the company and keep the answer short and precise."

    # Create two columns
    col1, col2 = st.columns(2)

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
