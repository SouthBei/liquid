import requests
from typing import List, Dict, Any, Optional
from urllib.parse import urlencode
import os
import json
import time
from . import api_ref



# 批量获取多个股票的实时行情
def quotec(symbols):
    url= api_ref.realtime_quote+symbols
    return fetch_without_token(url)

# 获取单个股票的详细实时行情
def quote_detail(symbol):
    url = api_ref.realtime_quote_detail+symbol
    return fetch(url)
# 获取股票的盘口数据
def pankou(symbol):
    url = api_ref.realtime_pankou+symbol
    return fetch(url)

# 获取股票的k线数据，支持不同周期
def klines(symbol,period='day',count=284):
    return fetch(api_ref.kline.format(symbol,int(time.times()*1000),period,count))


def klines_strong(symbol:str, period: str='day',count: int=284, **extra_params:Any) ->Dict[str,Any]:
    """
    获取股票K线数据(高度可扩展)
    
    参数:
        symbol: 股票代码
        period: K线周期(day/week/month/min/5min/15min/30min/60min)
        count: 获取的K线数量
       ** extra_params: 额外参数（如开始时间、结束时间等）
    """

    valid_periods= ['day','week','month','min','5min','30min']

    if period not in valid_periods:
        raise ValueError(f'无效的周期:{period},可选周期:{valid_periods}')
    
    # 基础参数
    base_params={'symbol':symbol}

    # 额外查询参数 (包括默认参数和动态参数)
    extra_params ={
        "timestamp":int(time.time()*1000),
        "period":period,
        "count": count,
        **extra_params # 动态参数可覆盖默认值 (加自定义timestamp)
    }

    return fetch_market_data(
        endpoint=api_ref.kline,
        base_params=base_params,
        extra_params=extra_params
    )

def fetch_market_data(endpoint:str,base_params: Dict[str,Any],extra_params:Optional[Dict[str,Any]]=None, use_token: bool=True) -> Dict[str,Any]:
     """
    通用市场数据获取函数（高扩展性版）
    
    参数:
        endpoint: 接口URL模板（支持格式化占位符）
        base_params: 用于URL模板格式化的参数（如symbol、type等）
        extra_params: 额外的查询参数（如count、period等）
        use_token: 是否需要Token验证
    
    返回:
        市场数据（JSON格式）
    """
     extra_params =extra_params or {}
     url = _build_url(endpoint,base_params,extra_params)
     return fetch(url) if use_token else fetch_without_token(url)

def _build_url(endpoint: str,base_params: Dict[str,Any],extra_params:Optional[Dict[str,Any]]=None):
    """
    构建完整URL,合并基础参数和额外参数
    
    参数:
        endpoint: 基础URL模板
        base_params: 基础参数(用于URL格式化)
        extra_params: 额外参数(用于URL查询字符串)
    
    返回:
        完整的请求URL
    """
     # 格式化基础URL（替换占位符）
    formatted_url = endpoint.format(**base_params)
    
    # 合并并过滤空值参数
    all_params= {k:v for k,v in extra_params.items() if v is not None}

    # 拼接查询字符串
    if all_params:
        return f"{formatted_url}?{urlencode(all_params)}"
    return formatted_url




def fetch_finance_data(data_type,symbol,is_annals=0,count=10):
    '''
    通用数据获取函数
    参数:
    data_type: 数据类型 'cash_flow','indicator','balance','income','business'
    symbol: 股票代码
    is_annals:是否年报(1 表示年报， 0 表示季报)
    count: 获取的数据条数
    '''
    url_mapping={
        'cash_flow': api_ref.finance_cash_flow_url,
        'indicator': api_ref.finance_indicator_url,
        'balance': api_ref.finance_balance_url,
        'income': api_ref.finance_income_url,
        'business': api_ref.finance_balance_url
    }

    if data_type not in url_mapping:
        raise ValueError(f"无效的数据类型:{data_type},可选值为:{list(url_mapping.keys())}")

    #构建URL
    url=f"{url_mapping[data_type]}{symbol}"

    if is_annals==1:
        url +="&type=Q4"
    
    #添加数据条数
    url += f'$count={str(count)}'
    return fetch(url)









def fetch(url,host="stock.xueqiu.com"):
    HEADERS={'Host': host,
               'Accept': 'application/json',
               'Cookie': get_token(),
               'User-Agent': 'Xueqiu iPhone 14.15.1',
               'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
               'Accept-Encoding': 'br, gzip, deflate',
               'Connection': 'keep-alive'}
    
    response=requests.get(url,headers=HEADERS)
    print(url)

    if(response.status_code!=200):
        raise Exception(response.content)

    return json.loads(response.content)


def fetch_without_token(url,host="stock.xueqiu.com"):
    HEADERS = {'Host': host,
               'Accept': 'application/json',
               'User-Agent': 'Xueqiu iPhone 11.8',
               'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
               'Accept-Encoding': 'br, gzip, deflate',
               'Connection': 'keep-alive'}
    
    response=requests.get(url,headers=HEADERS)
    print(url)

    if(response.status_code!=200):
        raise Exception(response.content)

    return json.loads(response.content)    



def get_token():
    if os.environ.get('XUEQIUTOKEN') is None:
        raise Exception('未设置Token')
    else:
        return os.environ['XUEQIUTOKEN']
    
def set_token(token):
    os.environ['XUEQIUTOKEN'] = token
    return os.environ['XUEQIUTOKEN']