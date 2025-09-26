import yfinance as yf
from flask import Flask, request, jsonify
app=Flask(__name__)

@app.route("/company", methods=["POST"])
def stock():
    data = request.get_json(force=True)
    ticker = data.get("ticker")

    if not ticker:
        return jsonify({"error": "Ticker name is required"}), 400

    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")  # use 1mo or longer to match screenshot

    if hist.empty:
        return jsonify({"error": f"No data found for ticker '{ticker}'"}), 404

    # Force-convert fast_info into a dictionary with only JSON-safe values
    fi = {k: (float(v) if isinstance(v, (int, float)) else str(v)) 
          for k, v in stock.fast_info.items()}

    # Convert full history (like screenshot)
    history_data = []
    for index, row in hist.iterrows():
        history_data.append({
            "Date": str(index),
            "Open": float(row["Open"]),
            "High": float(row["High"]),
            "Low": float(row["Low"]),
            "Close": float(row["Close"]),
            "Volume": int(row["Volume"]),
            "Dividends": float(row.get("Dividends", 0)),
            "Stock Splits": float(row.get("Stock Splits", 0))
        })

    return jsonify({
        "fast_info": fi,
        "history": history_data
    })


# from controller import *