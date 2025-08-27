import logging
from . import symbol_pool;
from . import snowball_api;
import pandas as pd


def select():
    symbol_arr=symbol_pool.husheng_300
    for symbol in symbol_arr:
        #取日线，
        #再取30min
        #再取15 min
        day_json=snowball_api.klines(symbol,'day',10)

        df=pd.DataFrame(
            day_json['data']['item'],
            columns=day_json['data']['column']
        )

        df['date']=pd.to_datetime(df['timestamp'],unit='ms').dt.date

        #计算五日均线和10日均线
        df['MA5'] =df['close'].rolling(window=5).mean()
        df['MA10']=df['close'].rolling(window=10).mean()

        result=df[['date','close','MA5','MA10']]
        print(result)
        mean5=df['MA5']
        print("五日均线")
        print(mean5)
        # thirtyMin_json=snowball_api.klines(symbol,'30min',365)
        # logger.info(thirtyMin_json)
        # logger.info("/n")
        # fiftyMin_json=snowball_api.klines(symbol,'15min',365)
        # logger.info(fiftyMin_json)
    return 


def print_stock_list():
    stock_list_json=snowball_api.fetch_hs_stock_list(page=1,size=30,order='desc',order_by='percent')
    #symbol；name; percent 涨跌幅; turnover_rate 换手率; pb;pb_ttm;current_year_percent当前年涨幅；
    df=pd.DataFrame(stock_list_json['data']['list'])
    stock_name_df=df.loc[:,['symbol','name']]
    print(stock_name_df)
    return df