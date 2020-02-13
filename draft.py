import json
import boto3
import datetime
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import configparser
import os
import pandas as pd
import statsmodels.api as sm

def lambda_handler(event, context):
    config_ini = configparser.ConfigParser()
    config_ini.read('config.ini', encoding='utf-8')

    access_token = config_ini['OANDA INFO']['ACCESS_TOKEN']
    access_env = config_ini['OANDA INFO']['ACCESS_ENV']
    inst = config_ini['OANDA INFO']['INST']
    request_data = { 
        "count": config_ini['OANDA INFO']['COUNT'],  
        "granularity": config_ini['OANDA INFO']['GRANULARITY']
    }

    api = API(access_token=access_token, environment=access_env)
    response = instruments.InstrumentsCandles(instrument=inst, params=request_data)
    
    df = pd.DataFrame(oandaJsonToPythonList(api.request(response)))
    df.columns = ['Datetime', 'Volume', 'Open', 'High', 'Low', 'Close']

    print(df)
    targetData = df['Close'].values
    print(type(targetData))
    print(sarima_predict(targetData))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def oandaJsonToPythonList(JSONRes):
    data = []
    for res in JSONRes['candles']:
        data.append( [
            datetime.datetime.fromisoformat(res['time'][:19]),
            res['volume'],
            res['mid']['o'],
            res['mid']['h'],
            res['mid']['l'],
            res['mid']['c'],
            ])
    return data

def sarima_predict(data):
    aic_min = 1000000000
    best_result = None
    for d in range(3):
        for p in range(3):
            for q in range(3):
                result =  sm.tsa.statespace.SARIMAX(endog=data, order=(p,d,q), use_exact_diffuse=True).fit()
                print("p=",p,",q=",q,",d=",d,",aic=",result.aic)
                if(result.aic<aic_min):
                    best_result = result
                    aic_min = result.aic
    return best_result.forecast(1)[0]


if __name__=='__main__':
    '''
    事前準備
    '''
    os.chdir('C:/Users/yuki.iwasaki/Desktop/git_practice/systemTrade/getData/hello_world')
    event = ""
    context = ""
    lambda_handler(event, context)