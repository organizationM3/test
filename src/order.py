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
import pandas as pd
import position_check

# OANDA API接続情報取得
config = configparser.ConfigParser()
config.read('./cfg/config.ini') 
account_id = config.get('oanda','account_id')
access_token = config.get('oanda','access_token')
# OANDA API接続
oanda = oandapy.API(environment="practice", access_token=access_token)


def get_csv():
    past_data=pd.read_csv('./usdjpy.csv')
    predict_data=pd.read_csv('./predict.csv')
    return past_data,predict_data

def logic_to_buy():
    flag=0
    past_data,predict_data=get_csv()
    previos_close=past_data.loc[4999,'Close']
    predict_price_open=predict_data.loc[0,'Open']
    predict_price_high=predict_data.loc[0,'High']
    predict_price_low=predict_data.loc[0,'Low']
    predict_price_close=predict_data.loc[0,'Close']
    price_increase=predict_price_open-previos_close
    if price_increase>0:
        flag=1
    
    return flag
    

def order():
    data =  {
    "order": {
    "instrument": "USD_JPY",
    "units": "+10000",
    "type": "MARKET",
    "positionFill": "DEFAULT"
             }    
            }
    r = orders.OrderCreate(account_id, data=data)
    result=oanda.request(r)
    return result
    
def main():
    flag=logic_to_buy()
    if flag==1:
        result=order()
        print(result)
    positions_array=position_check.positioncheck()
    print(positions_array)
    

if __name__ == '__main__':
    main()