import pandas as pd
import json
import requests
import os
class xg_data_api:
    '''
    小果数据api，支持qmt,服务器api
    '''
    def __init__(self,url='http://124.220.32.224',port=8888,password='123456'):
        '''
        小果数据api，支持qmt
        url服务器网页
        port端口
        password授权码
        '''
        self.url=url
        self.port=port
        self.password=password
        self.path=os.path.dirname(os.path.abspath(__file__))
    def get_user_info(self):
        '''
        获取用户信息
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={
            "output":"finace_data_table_1.data@e60ed22f488acd1653d4a92a187c4775d06cc39e4afa58da3bee9c8261dcc6a0",
            "outputs":{"id":"finace_data_table_1","property":"data@e60ed22f488acd1653d4a92a187c4775d06cc39e4afa58da3bee9c8261dcc6a0"},
            "inputs":[{"id":"finace_data_password","property":"value","value":self.password},
            {"id":"finace_data_data_type","property":"value","value":"代码"},
            {"id":"finace_data_text","property":"value","value":"from trader_tool.stock_data import stock_data\nstock_data=stock_data()\ndf=stock_data.get_stock_hist_data_em(stock='600031',start_date='20210101',end_date='20600101',data_type='D',count=8000)\ndf.to_csv(r'{}\\数据\\{}数据.csv')\n                \n                "},
            {"id":"finace_data_run","property":"value","value":"运行"},
            {"id":"finace_data_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["finace_data_run.value"],"parsedChangedPropsIds":["finace_data_run.value"]}
            
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['finace_data_table_1']['data'])
        return df
    def get_user_def_data(self,func=''):
        '''
        自定义数据获取
        调用数据库
        '''
        text=self.params_func(text=func)
        func=text
        info=self.get_user_info()
        print(info)
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={
            "output":"finace_data_table.data@e60ed22f488acd1653d4a92a187c4775d06cc39e4afa58da3bee9c8261dcc6a0",
            "outputs":{"id":"finace_data_table","property":"data@e60ed22f488acd1653d4a92a187c4775d06cc39e4afa58da3bee9c8261dcc6a0"},
            "inputs":[{"id":"finace_data_password","property":"value","value":self.password},
            {"id":"finace_data_data_type","property":"value","value":"代码"},
            {"id":"finace_data_text","property":"value","value":func},
            {"id":"finace_data_run","property":"value","value":"运行"},
            {"id":"finace_data_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["finace_data_run.value"],"parsedChangedPropsIds":["finace_data_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['finace_data_table']['data'])
        return info, df
    def params_func(self,text=''):
        '''
        解析函数
        '''
        data_list=[]
        f=text.split('\n')
        for i in f:
            text=i.strip().lstrip()
            data_list.append(text)
        func='\n'.join(data_list)
        return func
    def get_wencai_data(self,question='趋势向上,集合竞价大单进入,人气排行高',loop=True):
        '''
        获取数据数据
        '''
        func='''
        import pywencai
        df=pywencai.get(question='{}',loop=True)
        print(df)
        '''.format(question)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def qmt_get_tick_data(self,code_list='600111.SH',period='tick',start_time='20240714',end_time='20240731'):
        '''
        qmt获取连续tick数据
        '''
        func='''
        from xtquant import xtdata
        code_list='{}'
        period='{}'
        start_time='{}'
        end_time='{}'
        xtdata.subscribe_quote(stock_code=code_list,period=period,start_time=start_time,end_time=end_time,count=-1)
        df=xtdata.get_market_data_ex(stock_list=[code_list],period=period,start_time=start_time,end_time=end_time,count=-1)
        print(df)
        df=df[code_list]
        df['date']=df.index
        '''.format(code_list,period,start_time,end_time)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_tick_data(self,stock='600031.SH'):
        '''
        获取tick数据
        '''
        func='''
        from xtquant import xtdata
        import pandas as pd
        stock='{}'
        tick=xtdata.get_full_tick(code_list=[stock])
        tick=tick[stock]
        df=pd.DataFrame(tick.items())
        print(df)
        '''.format(stock)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_instrument_detail(self,stock='600031.SH'):
        '''
        获取合约基础信息
        '''
        func='''
        from xtquant import xtdata
        import pandas as pd
        df=xtdata.get_instrument_detail(stock_code='{}')
        df=pd.DataFrame(df.items())
        print(df)
        '''.format(stock)
        info,df=self.get_user_def_data(func=func)
        return info,df
    

if __name__=='__main__':
    '''
    数据api
    '''
    trader=xg_data_api()
    info,df=trader.get_instrument_detail()
    print(df)


