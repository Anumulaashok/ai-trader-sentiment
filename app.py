import os
from flask import Flask, jsonify
from sentiment.sentiment_analysis import analyze_sentiment

app = Flask(__name__)

@app.route("/sentiment/<symbol>", methods=["GET"])
def sentiment(symbol):
    """
    API endpoint to get the sentiment analysis for a given stock symbol.
    """
    # Convert symbol to uppercase for consistency, although news API might handle case
    symbol_upper = symbol.upper() 
    sentiment_score = analyze_sentiment(symbol_upper)
    
    # Basic validation/error handling based on analyze_sentiment output
    if sentiment_score in ["No news found", "Sentiment analysis unavailable", "Error during analysis"]:
        # Return an appropriate error response
        # Using 404 for 'No news found', 503 for unavailable, 500 for analysis error
        status_code = 404 if sentiment_score == "No news found" else (503 if sentiment_score == "Sentiment analysis unavailable" else 500)
        return jsonify({"error": sentiment_score}), status_code

    return jsonify({
        "symbol": symbol_upper,
        "sentiment_score": sentiment_score
    })

if __name__ == "__main__":
    # Get the port from the environment variable "PORT", defaulting to 5001.
    # Use host='0.0.0.0' to make it accessible externally if needed (e.g., in Docker)
    port = int(os.getenv("PORT", 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
