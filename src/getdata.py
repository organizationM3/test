'''
This exports OHLC csv file.
note:  Users need to install oandapV20 and pandas using pip command
'''
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import pandas as pd
import datetime

accountID = "101-009-13073790-002"
access_token = "2c1bb076a6c23d3f3f46f83ae9d7b163-0ec3e1e074994704c1c3b3ea35f352c6"
access_env = "practice" #practice or live
inst = "USD_JPY"
request_data = { #ref -> https://developer.oanda.com/docs/jp/v1/rates/#section-14
    "count": 5000,  # upper limit
    "granularity": "H1"
}
ohlc = []

def main():
    api = API(access_token=access_token, environment=access_env)
    req = instruments.InstrumentsCandles(instrument=inst, params=request_data)
    for rec in api.request(req)['candles']:
        ohlc.append([rec['time'], rec['mid']['o'], rec['mid']['h'], rec['mid']['l'], rec['mid']['c']])
    df = pd.DataFrame(ohlc)
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close']
    df = df.set_index('Time')
    df.index = pd.to_datetime(df.index, format='%Y-%m-%dT%H:%M:%S.000000000Z')
    df.index = df.index + datetime.timedelta(hours=9)
    df.to_csv('usdjpy.csv')

if __name__ == '__main__':
    main()
