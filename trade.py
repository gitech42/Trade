#!/usr/bin/python3
# -*- coding: iso-8859-1 -*
""" Python starter bot for the Crypto Trader games, from ex-Riddles.io """
__version__ = "1.0"

import string
import sys

from click import prompt

class Bot:
    def __init__(self):
        self.botState = BotState()
        self.btc = float(0)

    def run(self):
        while True:
            reading = input()
            if len(reading) == 0:
                continue
            self.parse(reading)

    def parse(self, info: str):
        buy_crypto = 0
        fee_porcent = 0
        tmp = info.split(" ")
        moyennehigh = float(0)
        moyennelow = float(0)
        if tmp[0] == "settings":
            self.botState.update_settings(tmp[1], tmp[2])
        if tmp[0] == "update":
            if tmp[1] == "game":
                self.botState.update_game(tmp[2], tmp[3])
        if tmp[0] == "action":
            print("La devisE DE CE TEST EST = " + self.botState.devise_crypto, file=sys.stderr)
            dollars = self.botState.stacks[self.botState.devise]
            monney_to_crypto = self.botState.monney_to_crypto
            bitcoint_wallet = self.botState.stacks[self.botState.devise_crypto]
            current_closing_price = self.botState.charts[monney_to_crypto].closes[-1]
            #print("OPENS PRICE = "+ str(self.botState.charts[monney_to_crypto].opens[-1]), file=sys.stderr)
            print("close PRICE = "+ str(self.botState.charts[monney_to_crypto].closes[-1]), file=sys.stderr)
            #print("high PRICE = "+ str(self.botState.charts[monney_to_crypto].highs[-1]), file=sys.stderr)
            #print("DATE PRICE = "+ str(self.botState.charts[monney_to_crypto].dates[-1]), file=sys.stderr)
            #print("lows PRICE = "+ str(self.botState.charts[monney_to_crypto].lows[-1]), file=sys.stderr)
            print("volume PRICE = "+ str(self.botState.transactionFee), file=sys.stderr)
            #print("cloes list PRICE = "+ str(len(self.botState.charts[monney_to_crypto].closes)), file=sys.stderr)
            i = len(self.botState.charts[monney_to_crypto].closes) - 200
            if (len(self.botState.charts[monney_to_crypto].closes) >= 200):
                while(i != len(self.botState.charts[monney_to_crypto].closes)):
                    moyennelow += self.botState.charts[monney_to_crypto].closes[i]
                    i+=1
                moyennelow /= 200
            i = len(self.botState.charts[monney_to_crypto].closes) - 400
            if (len(self.botState.charts[monney_to_crypto].closes) >= 400):
                while(i != len(self.botState.charts[monney_to_crypto].closes)):
                    moyennehigh += self.botState.charts[monney_to_crypto].closes[i]
                    i+=1
                moyennehigh /= 400
            #print("Moyenne haute = " + str(self.moyennehigh) + "moyenne basse = " + str(self.moyennelow), file=sys.stderr)
            affordable = dollars / current_closing_price
            buy_price = 0.1 *affordable
            print(f'My stacks are {dollars}. The current closing price is {current_closing_price}. So I can afford {affordable}', file=sys.stderr)
            #print("Moyenne haute = " + str(self.moyennehigh) + "moyenne basse = " + str(self.moyennelow), file=sys.stderr)
            if dollars < 50 and self.botState.charts[monney_to_crypto].closes[-1] > self.botState.charts[monney_to_crypto].closes[-4]:
                print("no_moves", flush=True)
            elif (moyennelow > moyennehigh):
                if (buy_price <= 0.00005):
                    print("no_moves", flush=True)
                else :
                    fee_porcent = self.botState.transactionFee * buy_crypto
                    print(f'buy {monney_to_crypto} {buy_price - fee_porcent}', flush=True)
                    self.btc += 0.1 * affordable
            elif (moyennehigh > moyennelow and bitcoint_wallet > 0.00002465):
                if (bitcoint_wallet > (self.botState.initialStack / 2)):
                    buy_crypto = bitcoint_wallet / 2
                    fee_porcent = self.botState.transactionFee * buy_crypto
                    print(f'sell {monney_to_crypto} {buy_crypto - fee_porcent}', flush=True)
                else:
                    buy_crypto = bitcoint_wallet / 4
                    fee_porcent = self.botState.transactionFee * buy_crypto
                    print(f'sell {monney_to_crypto} {buy_crypto - fee_porcent}', flush=True)
            else:
                print("no_moves", flush=True)

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
        self.devise = ""
        self.devise_crypto = ""
        self.monney_to_crypto = ""

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
        i = 0
        if key == "next_candles":
            new_candles = value.split(";")
            self.date = int(new_candles[0].split(",")[1])
            for candle_str in new_candles:
                candle_infos = candle_str.strip().split(",")
                self.update_chart(candle_infos[0], candle_str)
                self.monney_to_crypto = candle_infos[0]
        if key == "stacks":
            new_stacks = value.split(",")
            for stack_str in new_stacks:
                if (i == 2):
                    break
                stack_infos = stack_str.strip().split(":")
                self.update_stack(stack_infos[0], float(stack_infos[1]))
                if (i == 0):
                    self.devise_crypto = stack_infos[0]
                elif (i == 1):
                    self.devise = stack_infos[0]
                i+=1




if __name__ == "__main__":
    mybot = Bot()
    mybot.run()
