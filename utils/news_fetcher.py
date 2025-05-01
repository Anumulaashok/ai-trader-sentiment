import requests

# Replace with your actual NewsAPI key
NEWS_API_KEY = 'YOUR_NEWSAPI_KEY' 
BASE_URL = 'https://newsapi.org/v2/everything'

def fetch_news(symbol):
    """
    Fetches news headlines for a given stock symbol from NewsAPI.

    Args:
        symbol (str): The stock symbol (e.g., 'AAPL').

    Returns:
        list[str]: A list of news headlines, or an empty list if an error occurs.
    """
    params = {
        'q': symbol,
        'apiKey': NEWS_API_KEY,
        'sortBy': 'publishedAt', # Fetch most recent news
        'pageSize': 10 # Limit the number of articles
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        
        # Extract headlines
        headlines = [article['title'] for article in data.get('articles', []) if article.get('title')]
        return headlines
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news for {symbol}: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

if __name__ == '__main__':
    # Example usage (replace 'AAPL' with a symbol you want to test)
    sample_symbol = 'AAPL' 
    headlines = fetch_news(sample_symbol)
    if headlines:
        print(f"Headlines for {sample_symbol}:")
        for i, headline in enumerate(headlines):
            print(f"{i+1}. {headline}")
    else:
        print(f"Could not fetch headlines for {sample_symbol}.")
