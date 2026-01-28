import ccxt
import pandas as pd


def fetch_market_data(symbol="BTC/USDT", timeframe='1h', limit=100):
    """
    Loads data from MEXC exchange
    
    :param symbol: exchange pair
    :param timeframe: what timeframe candles are indicating
    :param limit: limit of last candles
    """
    exchange = ccxt.mexc()

    try:
        print(f"Загружаю данные для {symbol} {timeframe}")

        # делаем запрос к бирже: Open, High, Low, Close, Volume
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        return ohlcv

    except Exception as e:
        print(f"Error: {e}")
        return None
    


def count_sma(df: pd.DataFrame, candles_cnt=50) -> float:
    """
    average price for last [candles_cnt] candles
    
    """

    return df['close'].rolling(window=candles_cnt).mean()

    
        

if __name__ == "__main__":
    data = fetch_market_data(timeframe='1m')
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high',
                                      'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    print(df)