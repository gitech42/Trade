#!/usr/bin/python3
# -*- coding: iso-8859-1 -*
""" Python starter bot for the Crypto Trader games, from ex-Riddles.io """
__version__ = "1.0"

import sys

from click import prompt

class Bot:
    def __init__(self):
        self.botState = BotState()
        self.btc = float(0)
        self.list_price = []
        #self.moyennehigh = float(0)

    def run(self):
        while True:
            reading = input()
            if len(reading) == 0:
                continue
            self.parse(reading)

    def parse(self, info: str):
        tmp = info.split(" ")
        moyennehigh = float(0)
        moyennelow = float(0)
        if tmp[0] == "settings":
            self.botState.update_settings(tmp[1], tmp[2])
        if tmp[0] == "update":
            if tmp[1] == "game":
                self.botState.update_game(tmp[2], tmp[3])
        if tmp[0] == "action":
            # This won't work every time, but it works sometimes!
            dollars = self.botState.stacks["USDT"]
            bitcoint_wallet = self.botState.stacks["BTC"]
            if (len(self.list_price) >= 1):
                affordable = dollars / self.list_price[-1]
                buy_price = 0.1 *affordable
            #print(f'My stacks are {dollars}. The current closing price is {self.list_price[-1]}. So I can afford {affordable}', file=sys.stderr)
            self.list_price.append(self.botState.charts["USDT_BTC"].closes[-1])
            #print("OPENS PRICE = "+ str(self.botState.charts["USDT_BTC"].opens[-1]), file=sys.stderr)
            print("close PRICE list = "+ str(self.list_price), file=sys.stderr)
            #print("high PRICE = "+ str(self.botState.charts["USDT_BTC"].highs[-1]), file=sys.stderr)
            #print("DATE PRICE = "+ str(self.botState.charts["USDT_BTC"].dates[-1]), file=sys.stderr)
            #print("lows PRICE = "+ str(self.botState.charts["USDT_BTC"].lows[-1]), file=sys.stderr)
            print("volume PRICE = "+ str(self.botState.charts["USDT_BTC"].volumes[-1]), file=sys.stderr)
            #print("cloes list PRICE = "+ str(len(self.botState.charts["USDT_BTC"].closes)), file=sys.stderr)
            i = len(self.list_price) - 12
            if (len(self.list_price) >= 12):
                #while(i != len(self.list_price)):
                    if dollars < 50 and self.botState.charts["USDT_BTC"].closes[-1] > self.botState.charts["USDT_BTC"].closes[-4]:
                        print("no_moves", flush=True)
                    if (self.list_price[-1] <= self.list_price[0]):
                        if (buy_price <= 0.00005):
                            print("no_moves", flush=True)
                        else :
                            print(f'buy USDT_BTC {0.5*affordable}', flush=True)
                    elif (self.list_price[-1] >= self.list_price[-2] and bitcoint_wallet > 0.00002465):
                        print(f'sell USDT_BTC {bitcoint_wallet}', flush=True)
                    else:
                        print("no_moves", flush=True)
            else :
                print("no_moves", flush=True)
                    #i+=1x²
            #elif (moyennelow > moyennehigh):
            #   if (buy_price <= 0.00005):
            #       print("no_moves", flush=True)
            #   else :
            #        print(f'buy USDT_BTC {buy_price}', flush=True)
            #        self.btc += 0.1 * affordable
            #elif (moyennehigh > moyennelow and bitcoint_wallet > 0.00002465):
            #    if (bitcoint_wallet > (self.botState.initialStack / 2)):
            #        print(f'sell USDT_BTC {bitcoint_wallet / 2}', flush=True)
            #    else:
            #        print(f'sell USDT_BTC {bitcoint_wallet / 4}', flush=True)
            #else:
            #    print("no_moves", flush=True)
            self.list_price.sort()

#### faire autre algo basé sur les prix d'une periode N (stocker tt les prix, sort la list dans lordre croissant et comparer a la hause ou a la baisse)

class Candle:
    def __init__(self, format, intel):
        tmp = intel.split(",")
        for (i, key) in enumerate(format):
            value = tmp[i]
            if key == "pair":
                self.pair = value
            if key == "date":
                self.date = int(value)
            if key == "high":
                self.high = float(value)
            if key == "low":
                self.low = float(value)
            if key == "open":
                self.open = float(value)
            if key == "close":
                self.close = float(value)
            if key == "volume":
                self.volume = float(value)

    def __repr__(self):
        return str(self.pair) + str(self.date) + str(self.close) + str(self.volume)


class Chart:
    def __init__(self):
        self.dates = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        self.indicators = {}

    def add_candle(self, candle: Candle):
        self.dates.append(candle.date)
        self.opens.append(candle.open)
        self.highs.append(candle.high)
        self.lows.append(candle.low)
        self.closes.append(candle.close)
        self.volumes.append(candle.volume)


class BotState:
    def __init__(self):
        self.timeBank = 0
        self.maxTimeBank = 0
        self.timePerMove = 1
        self.candleInterval = 1
        self.candleFormat = []
        self.candlesTotal = 0
        self.candlesGiven = 0
        self.initialStack = 0
        self.transactionFee = 0.1
        self.date = 0
        self.stacks = dict()
        self.charts = dict()

    def update_chart(self, pair: str, new_candle_str: str):
        if not (pair in self.charts):
            self.charts[pair] = Chart()
        new_candle_obj = Candle(self.candleFormat, new_candle_str)
        self.charts[pair].add_candle(new_candle_obj)

    def update_stack(self, key: str, value: float):
        self.stacks[key] = value

    def update_settings(self, key: str, value: str):
        if key == "timebank":
            self.maxTimeBank = int(value)
            self.timeBank = int(value)
        if key == "time_per_move":
            self.timePerMove = int(value)
        if key == "candle_interval":
            self.candleInterval = int(value)
        if key == "candle_format":
            self.candleFormat = value.split(",")
        if key == "candles_total":
            self.candlesTotal = int(value)
        if key == "candles_given":
            self.candlesGiven = int(value)
        if key == "initial_stack":
            self.initialStack = int(value)
        if key == "transaction_fee_percent":
            self.transactionFee = float(value)

    def update_game(self, key: str, value: str):
        if key == "next_candles":
            new_candles = value.split(";")
            self.date = int(new_candles[0].split(",")[1])
            for candle_str in new_candles:
                candle_infos = candle_str.strip().split(",")
                self.update_chart(candle_infos[0], candle_str)
        if key == "stacks":
            new_stacks = value.split(",")
            for stack_str in new_stacks:
                stack_infos = stack_str.strip().split(":")
                self.update_stack(stack_infos[0], float(stack_infos[1]))


if __name__ == "__main__":
    mybot = Bot()
    mybot.run()