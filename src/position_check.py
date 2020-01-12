# ライブラリのインポート
import json
import oandapyV20 as oandapy
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.orders as orders
import configparser
import sys
import numpy as np
from datetime import datetime

# OANDA API接続情報取得
config = configparser.ConfigParser()
config.read('./cfg/config.ini') # パスの指定が必要です
account_id = config.get('oanda','account_id')
access_token = config.get('oanda','access_token')
# OANDA API接続
oanda = oandapy.API(environment="practice", access_token=access_token)

# ポジションの取得
def positioncheck():
    res = positions.OpenPositions(accountID=account_id)
    response=oanda.request(res)
    return response
    
#取引可能な通貨情報の取得
def get_instrument_info():
    params = { "instruments": "USD_JPY" }
    r = accounts.AccountInstruments(accountID=account_id ,params=params)
    info=oanda.request(r)
    return info
    
#口座情報の取得    
def get_account_info():
    r = accounts.AccountSummary(account_id)
    account_info=oanda.request(r)
    return account_info

def main():
    #get_info=get_instrument_info()
    positions_array =positioncheck()
    print(positions_array)
    #print(positions_array['positions'])
    

if __name__ == '__main__':
    main()