import ccxt
import pandas as pd
from langchain_core.tools import tool


# вспомогательная функция для загрузки данных
def _fetch_market_data(symbol="BTC/USDT", timeframe='1h', limit=100):
    exchange = ccxt.binance()

    # делаем запрос к бирже: Open, High, Low, Close, Volume
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high',
                                       'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    return df, exchange

@tool
def get_technical_analysis(symbol: str,
                           timeframe: str = '1h'):
    """
    Функция для расчета индикаторов SMA_50 и RSI_14
    """
    try:
        # загрузка данных
        df, exchange = _fetch_market_data(symbol, timeframe, limit=100)

        # считаем индикаторы
        # SMA 50
        df['SMA_50'] = df['close'].rolling(window=50).mean()

        # RSI 14
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        df['RSI'] = 100 - (100 / (1 + rs))

        last_data = df.iloc[-1].to_dict()


        return {
            "exchange": exchange.name,
            "symbol": symbol,
            "price": last_data['close'],
            "SMA_50": round(last_data['SMA_50'], 2) if not pd.isna(last_data['SMA_50']) else "N/A",
            "RSI": round(last_data['RSI'], 2) if not pd.isna(last_data['RSI']) else "N/A"
        }
    except Exception as e:
        return f"Ошибка при анализе: {e}"


if __name__ == "__main__":
    df, exchange = _fetch_market_data()
    print(df.head())