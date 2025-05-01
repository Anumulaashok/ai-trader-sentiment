from transformers import BertTokenizer, BertForSequenceClassification, pipeline
from utils.news_fetcher import fetch_news
import torch # Import torch to potentially manage device placement if needed

# Load FinBERT tokenizer and model
model_name = "yiyanghkust/finbert-tone"
try:
    tokenizer = BertTokenizer.from_pretrained(model_name)
    # Explicitly load the model for sequence classification
    model = BertForSequenceClassification.from_pretrained(model_name) 
    # Create sentiment analysis pipeline
    # Specify task="text-classification" for clarity, though it's often inferred
    # device=0 for GPU if available, -1 for CPU
    sentiment_pipeline = pipeline("text-classification", model=model, tokenizer=tokenizer, device=-1) 
except Exception as e:
    print(f"Error loading model or tokenizer: {e}")
    # Provide a fallback or raise an error if the model is essential
    sentiment_pipeline = None 

def analyze_sentiment(symbol):
    """
    Analyzes the sentiment of news headlines for a given stock symbol.

    Args:
        symbol (str): The stock symbol (e.g., 'AAPL').

    Returns:
        str: The overall sentiment score ('positive', 'negative', 'neutral'), 
             or 'No news found' if no headlines are available.
             Returns 'Sentiment analysis unavailable' if the pipeline failed to load.
    """
    if sentiment_pipeline is None:
        return "Sentiment analysis unavailable"
        
    headlines = fetch_news(symbol)

    if not headlines:
        return "No news found"

    sentiments = []
    try:
        # Process headlines in batches if necessary, but for 10 it's likely fine
        results = sentiment_pipeline(headlines) 
        # Extract just the labels
        sentiments = [result['label'] for result in results] 
    except Exception as e:
        print(f"Error during sentiment analysis for {symbol}: {e}")
        return "Error during analysis" # Or handle more gracefully

    # Determine overall sentiment score
    positive_count = sentiments.count('POSITIVE')
    negative_count = sentiments.count('NEGATIVE')
    # neutral_count = sentiments.count('NEUTRAL') # Not strictly needed for this logic

    total_headlines = len(headlines)
    sentiment_score = "neutral" # Default sentiment

    if positive_count > total_headlines / 2:
        sentiment_score = "positive"
    elif negative_count > total_headlines / 2:
        sentiment_score = "negative"

    return sentiment_score

if __name__ == '__main__':
    # Example usage (replace 'AAPL' with a symbol you want to test)
    sample_symbol = 'TSLA' 
    overall_sentiment = analyze_sentiment(sample_symbol)
    print(f"Overall sentiment for {sample_symbol}: {overall_sentiment}")

    sample_symbol_no_news = 'NONEXISTENTSTOCKXYZ'
    overall_sentiment_no_news = analyze_sentiment(sample_symbol_no_news)
    print(f"Overall sentiment for {sample_symbol_no_news}: {overall_sentiment_no_news}")
