# AI Trader Sentiment API

## Description

This project provides a simple Flask-based API that performs sentiment analysis on recent news headlines for a given stock symbol. It fetches news using the NewsAPI and analyzes sentiment using the FinBERT model fine-tuned for financial text.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url> # Replace <repository_url> with the actual URL
    cd ai-trader-sentiment
    ```

2.  **Create and activate a Python virtual environment:**
    *   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The first time you run the application, the FinBERT model (~400MB) will be downloaded.*

## Configuration

1.  **Get a NewsAPI Key:**
    You need an API key from NewsAPI to fetch news headlines. Register for a free key at [https://newsapi.org/](https://newsapi.org/).

2.  **Update the API Key:**
    Open the file `utils/news_fetcher.py` and replace the placeholder string `'YOUR_NEWSAPI_KEY'` with your actual NewsAPI key:
    ```python
    # Replace with your actual NewsAPI key
    NEWS_API_KEY = 'YOUR_NEWSAPI_KEY' 
    ```

## Running the Application

1.  **Start the Flask server:**
    ```bash
    python app.py
    ```
    Alternatively, you can use the Flask CLI (if Flask is installed globally or the venv is active):
    ```bash
    flask run --port=5001 # Specify port if needed
    ```

2.  **Accessing the API:**
    The server will start, typically on `http://localhost:5001` or `http://0.0.0.0:5001`. The default port is 5001. You can specify a different port by setting the `PORT` environment variable before running the app:
    ```bash
    export PORT=8080 # macOS/Linux
    set PORT=8080   # Windows
    python app.py
    ```

## API Endpoint

### Get Sentiment by Symbol

*   **Endpoint:** `GET /sentiment/<symbol>`
*   **Description:** Retrieves the overall sentiment (positive, negative, or neutral) based on recent news headlines for the specified stock symbol.
*   **`<symbol>`:** The stock ticker symbol (e.g., AAPL, GOOGL, TSLA).

*   **Example Request:**
    ```bash
    curl http://localhost:5001/sentiment/AAPL
    ```

*   **Example Success Response (200 OK):**
    ```json
    {
      "symbol": "AAPL",
      "sentiment_score": "neutral" 
    }
    ```
    *(Note: The actual sentiment score will vary based on current news.)*

*   **Example Error Response (404 Not Found - No News):**
    ```json
    {
      "error": "No news found"
    }
    ```
*   **Example Error Response (503 Service Unavailable - Model Issue):**
    ```json
    {
      "error": "Sentiment analysis unavailable"
    }
    ```