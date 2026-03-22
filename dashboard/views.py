from django.shortcuts import render
from django.http import FileResponse
import main
import yfinance as yf
import os
import pickle
from main import prepare_data, generate_excel, generate_pdf

PICKLE_DIR = "pickle_data"

def fetch_financials(ticker_symbol):
    path = os.path.join(PICKLE_DIR, f"{ticker_symbol}.pkl")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.financials
    os.makedirs(PICKLE_DIR, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(data, f)
    return data

def home(request):
    ticker_symbol = request.GET.get("ticker", "AAPL")
    fin = fetch_financials(ticker_symbol)

    latest = fin.columns[0]
    prev = fin.columns[1]

    def get(row):
        for r in fin.index:
            if r.strip() == row.strip():
                return fin.loc[r]
        return None

    def fmt(val):
        if val is None:
            return "N/A"
        return f"${val / 1_000_000_000:.1f}B"

    def chg(row):
        s = get(row)
        if s is None:
            return None, None
        v_new = s[latest]
        v_old = s[prev]
        if v_old and v_old != 0:
            pct = (v_new - v_old) / abs(v_old) * 100
            return round(pct, 1), pct >= 0
        return None, None

    metrics = {}
    for row in ["Total Revenue", "Gross Profit", "Operating Income", "Net Income"]:
        s = get(row)
        pct, is_up = chg(row)
        metrics[row] = {
            "value": fmt(s[latest]) if s is not None else "N/A",
            "pct": f"{'+' if is_up else ''}{pct}%" if pct is not None else "",
            "is_up": is_up,
        }

    context = {
            "ticker": ticker_symbol,
            "metrics": metrics,
            "tickers": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META"],
        }
    return render(request, 'index.html', context)



def export_excel(request):
    ticker_symbol = request.GET.get("ticker", "AAPL")
    fin = fetch_financials(ticker_symbol)
    df = prepare_data(fin)

    out_path = os.path.join("reports", f"{ticker_symbol}_income_statement.xlsx")

    if not os.path.exists(out_path):
        generate_excel(ticker_symbol, df)

    return FileResponse(open(out_path, "rb"), as_attachment=True, filename=f"{ticker_symbol}_income_statement.xlsx")


def export_pdf(request):
    ticker_symbol = request.GET.get("ticker", "AAPL")
    fin = fetch_financials(ticker_symbol)
    df = prepare_data(fin)

    out_path = os.path.join("reports", f"{ticker_symbol}_income_statement.pdf")

    if not os.path.exists(out_path):
        generate_pdf(ticker_symbol, df)

    return FileResponse(open(out_path, "rb"), as_attachment=True, filename=f"{ticker_symbol}_income_statement.pdf")



def documentation(request):
    return render(request, 'documentation.html')