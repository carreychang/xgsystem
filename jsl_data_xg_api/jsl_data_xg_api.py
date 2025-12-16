from .jsl_data_xg import jsl_data_xg
from datetime import datetime
import os
import pandas as pd
from tqdm import tqdm
import json
from .user_def_models import user_def_models
import warnings
import akshare as ak
warnings.filterwarnings(action='ignore')
from trader_tool.unification_data import unification_data
class jsl_data_xg_api:
    def __init__(self,trader_tool='qmt',data_api='qmt',user='', password='',limit=10,) -> None:
        '''
        集思录数据
        '''
        self.limit=limit
        self.data_api=data_api
        self.trader_tool=trader_tool
        self.path=os.path.dirname(os.path.abspath(__file__))
        self.user=user
        self.password=password
        self.models=jsl_data_xg(user=self.user,password=self.password)
        self.unification_data=unification_data(data_api=self.data_api,trader_tool=self.trader_tool)
        self.data=self.unification_data.get_unification_data()
        self.models.login()
    def get_spot_data(self):
        '''
        获取实时数据
        '''
        try:
            df=self.models.get_conv_data_jsl()
            now_date=''.join(str(datetime.now())[:10].split('-'))
            df['交易日']=now_date
            df['更新时间']=datetime.now()
        except Exception as e:
            print(e,'获取实时数据有问题')
            df=pd.DataFrame()
        return df
    def get_all_connect_data(self):
        '''
        获取全部的默认因子
        '''
        try:
            df=self.models.get_all_connect_data(self.limit)
            all_factor_columns=df.columns.tolist()
            spot_df=self.get_spot_data()
            if spot_df.shape[0]>0:
                spot_columns=spot_df.columns.tolist()
            else:
                spot_columns=[]
            for columns in spot_columns:
                if columns not in all_factor_columns:
                    data_dict=dict(zip(spot_df['转债代码'].tolist(),spot_df[columns].tolist()))
                    df[columns]=df['可转债代码'].apply(lambda x: data_dict.get(x,None))
                else:
                    pass
        except Exception as e:
            print(e,'获取全部的默认因子有问题')
            df=pd.DataFrame()
        return df
    def get_user_def_func_models(self):
        '''
        自定义函数分析模型
        '''
        with open(r'{}\可转债因子合成.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        if True:
            print(datetime.now())
            now_date=''.join(str(datetime.now())[:10].split('-'))
            user_factor=text['自定义因子函数']
            factor_name=list(user_factor.keys())
            df=self.get_all_connect_data()
            if df.shape[0]>0:
                df['证券代码']=df['可转债代码']
                #可转债等权指数
                index_df=ak.bond_cb_index_jsl()
                user_factor_list=[]
                stock_list=df['可转债代码'].tolist()
                for i in tqdm(range(len(stock_list))):
                    stock=stock_list[i]  
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
                df1.columns=factor_name
                df1['证券代码']=stock_list
                df['交易日']=now_date
                df['更新时间']=datetime.now()
                df=pd.merge(df,df1,on=['证券代码'])
                df=df.drop_duplicates(subset=['证券代码'],keep='last')
            else:
                df=pd.DataFrame()
            return df
if __name__=='__main__':
    models=jsl_data_xg_api()
    df=models.get_spot_data()
    print(df)
    
    