import numpy as np
import asyncio
import inspect
from utils import markets
from talib import RSI
from binance import AsyncClient, Client


client = AsyncClient("API_KEY", "SEC_KEY")
candlesticks_list = []
listRSI_change = []
market_out = {}


async def get_rsi(symbol, interval, period=14):
    candlesticks = await client.futures_historical_klines(symbol, interval,
                                                          start_str="1 day ago UTC")
    candlesticks_list.append((await candlesticks, symbol))


async def main(loop: any):
    tasks = []
    for market in markets:
        task = loop.create_task(get_rsi(market, "15m"))
        tasks.append(task)
    await asyncio.wait(tasks)
    await client.close_connection()


def data():
    for candlesticks, symbol in candlesticks_list:
        close = []
        for candlestick in candlesticks:
            candlestick_close = candlestick[4]
            close.append(float(candlestick_close))
        np_close = np.array(close)

        rsi = RSI(np_close, timeperiod=14)

        rsi_length = len(rsi)
        rsi_value = rsi[rsi_length - 1]
        market_out[symbol] = rsi_value
    for pair in markets:
        listRSI_change.append(market_out[pair])


def main_function():
    loop = asyncio.get_event_loop()
    check = loop.run_until_complete(main(loop))
    data()
    # print(inspect.iscoroutinefunction(get_rsi))
    # print(inspect.iscoroutinefunction(main))
    return listRSI_change


print(main_function())
