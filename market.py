import asyncio
from binance import AsyncClient
from utils import MARKETS
import numpy as np
from talib import RSI

keys = {
    "api_key": '1sg1p8KodinRCO6uM6yesCfuYhsDbCqiX7lPdzNNEhxmUFu9y2Sv6tksLNiwNCFD',
    "secret_key": 'NCVK5aPAlsQH57oLOonyznFUwX09RD0CZ9KPDetwtWLSoE8rj0xmhFSLgzy66oGT'
}


async def some_function():
    client = await AsyncClient.create('API_KEY', 'SECRET_KEY')
    listRSI_change = []
    candlesticks = []

    async def get_rsi(markets: list, interval: any, period=14) -> list:

        for market in markets:
            candlestick = await client.futures_historical_klines(
                market,
                interval,
                start_str="1 day ago UTC"
            )

            candlesticks.append((await candlestick, market))

    async def main() -> list:

        task1 = asyncio.create_task(
            get_rsi(MARKETS, client.KLINE_INTERVAL_15MINUTE,))
        value = await task1
        market_out(value, MARKETS)
        await client.close_connection()

    def market_out(candlesticks_list: list, markets: list) -> list:
        market_out = {}
        close = []

        for candlesticks, symbol in candlesticks_list:
            for candlestick in candlesticks:
                candlesticks_close = candlestick[4]
                close.append(float(candlesticks_close))
            np_close = np.array(close)

            rsi = RSI(np_close, timeperiod=14)
            rsi_length = len(rsi)
            rsi_value = rsi[rsi_length - 1]
            market_out[symbol] = rsi_value
        for pair in markets:
            listRSI_change.append(market_out[pair])

        return listRSI_change

    await main()

asyncio.run(some_function()
            )
