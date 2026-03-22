import shutil
import openpyxl
from datetime import datetime
import requests
import json


def fetch_detailed_data():
    # Используем эндпоинт для статистики за 24 часа
    url = "https://api.binance.com/api/v3/ticker/24hr"
    target_symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT']
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            all_stats = response.json()
            # Оставляем только нужные монеты и важные поля
            filtered = []
            for item in all_stats:
                if item['symbol'] in target_symbols:
                    filtered.append({
                        "symbol": item['symbol'],
                        "price": item['lastPrice'],
                        "change_percent": item['priceChangePercent'], # Изменение в %
                        "high": item['highPrice'],                  # Макс за сутки
                        "low": item['lowPrice'],                   # Мин за сутки
                        "volume": item['quoteVolume']              # Объем в USDT
                    })
            return filtered
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    data = fetch_detailed_data()
    if data:
        print(json.dumps(data, indent=4))
        
        print("\n--- Аналитика за 24ч: ---")
        for c in data:
            status = "📈" if float(c['change_percent']) > 0 else "📉"
            print(f"{status} {c['symbol']}: {c['price']}$ ({c['change_percent']}%)")
            print(f"    Диапазон: {c['low']} - {c['high']} | Объем: {float(c['volume']):,.0f} USDT")