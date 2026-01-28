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
    


def count_sma(df: pd.DataFrame, candles_cnt=50) -> pd.Series:
    """
    average price for last [candles_cnt] candles
    
    """

    return df['close'].rolling(window=candles_cnt).mean()

def count_rsi(df: pd.DataFrame, candles_cnt=14) -> float:
    """
    counts RSI indicator for last [candles_cnt] candles
    """
    
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    
    return 100 - (100 / (1 + rs))
        

if __name__ == "__main__":
    data = fetch_market_data(timeframe='1m')
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high',
                                      'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')


    df['SMA_20'] = count_sma(df)
    print(df)