from datetime import datetime
from trader_tool.base_func import base_func
import os
import schedule
import time
import pandas as pd
import os
from tqdm import tqdm
import json
from xgtrader.unification_data_ths import unification_data_ths
from .user_def_models import user_def_models
from trader_tool.index_data import index_data
import akshare as ak
import time
import schedule
import threading
import queue
from trader_tool.dfcf_etf_data import dfcf_etf_data
class xg_user_def_factor_system:
    def __init__(self,
                df='',
                index_data='',
                stock_list=['513100','511090'],
                on_list=['证券代码'],
                connect=False,
                limit=10):
        '''
        小果自定义因子合成系统
        df需要合并的默认因子
        index_data指数数据
        stock_list股票
        on_list合并的keys
        connect是否合并
        '''
        self.path=os.path.dirname(os.path.abspath(__file__))
        self.index_data=index_data
        self.base_func=base_func()
        self.data=unification_data_ths()
        self.df=df
        self.stock_list=stock_list
        self.on_list=on_list
        self.connect=connect
        self.limit=limit
    def get_user_def_func_models(self):
        '''
        自定义函数分析模型
        '''
        with open(r'{}\因子合成.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
            
        now_date=''.join(str(datetime.now())[:10].split('-'))
        user_factor=text['自定义因子函数']
        factor_name=list(user_factor.keys())
        stock_list=self.stock_list[:self.limit]
        data=pd.DataFrame()
        for i in tqdm(range(len(stock_list))):
            stock=stock_list[i]
            #300指数
            index_df=self.index_data
            user_factor_list=[]
            result_list=[]
            try: 
                hist=self.data.get_hist_data_em(stock=stock)     
                models=user_def_models(df=hist,index_df=index_df) 
                for name in  factor_name:
                    try:
                            
                        func=user_factor[name] 
                        func='models.{}'.format(func)
                        result=eval(func)
                        result_list.append(result)
                    except Exception as e:
                        func=user_factor[name] 
                        print(e,'{} {} 函数计算错误'.format(name,func))
                        result_list.append(None)
                    
            except Exception as e:
                print(e,'{} 数据获取错误'.format(stock))
                result_list.append(None)
            user_factor_list.append(result_list)
            df1=pd.DataFrame(user_factor_list)
            try:
                df1.columns=factor_name
                df1['证券代码']=stock
                df1['交易日']=now_date
                df1['更新时间']=datetime.now()
                data=pd.concat([data,df1],ignore_index=True)
            except:
                pass
            #data.index=data['证券代码']
        if self.connect:
            df=self.df
            df=pd.merge(df,data,on=self.on_list)
            df=df.drop_duplicates(subset=self.on_list,keep='last')
            data.index=data['证券代码']
            return df
        else:
            data.index=data['证券代码']
            return data
            
        
if __name__=='__main__':
    index=index_data().get_index_hist_data()
    df=dfcf_etf_data().get_all_etf_data_1()
    df['证券代码']=df['基金代码']
    models=xg_user_def_factor_system(df=df,index_data=index,connect=True)
    df=models.get_user_def_func_models()
    print(df)
    df.to_excel(r'数据.xlsx')
           
    


