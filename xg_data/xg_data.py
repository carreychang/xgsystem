import pandas as pd
import json
import requests
import os
class xg_data:
    '''
    小果数据api，支持qmt,本地
    '''
    def __init__(self,url='http://124.220.32.224',port=8888,password='123456'):
        '''
        小果数据api，支持qmt,本地
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
        获取问财经数据
        '''
        func='''
            from xg_data.xg_data_api import xg_data_api
            api=xg_data_api(url='{}',port='{}',password='{}')
            info,df=api.get_wencai_data(question='{}')
            print(df)
        '''.format(self.url,self.port,self.password,question)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def qmt_get_tick_data(self,code_list='600111.SH',period='tick',start_time='20240714',end_time='20240731'):
        '''
        qmt连续tick数据
        '''
        func='''
            from xg_data.xg_data_api import xg_data_api
            api=xg_data_api(url='{}',port='{}',password='{}')
            info,df=api.qmt_get_tick_data(code_list='{}',period='{}',start_time='{}',end_time='{}')
            print(df)
        '''.format(self.url,self.port,self.password,code_list,period,start_time,end_time)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_full_tick(self,stock='600031.SH'):
        '''
        获取tick数据
        '''
        func='''
            from xg_data.xg_data_api import xg_data_api
            api=xg_data_api(url='{}',port='{}',password='{}')
            info,df=api.get_tick_data(stock='{}')
            print(df)
        '''.format(self.url,self.port,self.password,stock)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_instrument_detail(self,stock='600031.SH'):
        '''
        获取合约基础信息
        '''
        func='''
            from xg_data.xg_data_api import xg_data_api
            api=xg_data_api(url='{}',port='{}',password='{}')
            info,df=api.get_instrument_detail(stock='{}')
            print(df)
        '''.format(self.url,self.port,self.password,stock)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_hot_stock_rank(self,data_type='大家都在看',date='hour'):
        '''
        股票人气排行
        '''
        func='''
        from trader_tool.ths_rq import ths_rq
        rq=ths_rq()
        df=rq.get_hot_stock_rank(data_type='{}',date='{}')
        print(df)
        '''.format(data_type,date)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_stock_concept_rot_rank(self):
        '''
        获取股票概念热度排行
        '''
        func='''
        from trader_tool.ths_rq import ths_rq
        rq=ths_rq()
        df=rq.get_stock_concept_rot_rank()
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_stock_industry_rot_rank(self):
        '''
        获取股票行业热度排行
        '''
        func='''
        from trader_tool.ths_rq import ths_rq
        rq=ths_rq()
        df=rq.get_stock_concept_rot_rank()
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_etf_hot_rank(self):
        '''
        同花顺etf热度排行
        '''
        func='''
        from trader_tool.ths_rq import ths_rq
        rq=ths_rq()
        df=rq.get_etf_hot_rank()
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_cov_bond_rot_rank(self):
        '''
        同花顺可转债热度排行
        '''
        func='''
        from trader_tool.ths_rq import ths_rq
        rq=ths_rq()
        df=rq.get_cov_bond_rot_rank()
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_HK_stock_rot_rank(self):
        '''
        港股热度排行
        '''
        func='''
        from trader_tool.ths_rq import ths_rq
        rq=ths_rq()
        df=rq.get_HK_stock_rot_rank()
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_US_stock_rot_rank(self):
        '''
        同花顺 美股热度排行
        '''
        func='''
        from trader_tool.ths_rq import ths_rq
        rq=ths_rq()
        df=rq.get_US_stock_rot_rank()
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_futurn_hot_rank(self):
        '''
        同花顺热期货排行
        '''
        func='''
        from trader_tool.ths_rq import ths_rq
        rq=ths_rq()
        df=rq.get_futurn_hot_rank()
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def  get_individual_stocks_add_concept(self,date='2024-08-02'):
        '''
        同花顺个股新添加的概念
        '''
        func='''
        from trader_tool.ths_new_concept import ths_new_concept
        api=ths_new_concept()
        df=api.get_individual_stocks_add_concept(date='{}')
        print(df)
        '''.format(date)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_all_etf_data_1(self):
        '''
        东方财富全部的etf数据
        '''
        func='''
        from trader_tool.dfcf_etf_data import dfcf_etf_data
        api=dfcf_etf_data()
        df=api.get_all_etf_data_1()
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_all_etf_data(self):
        '''
        东方财富全部的etf数据合并相同的
        '''
        func='''
        from trader_tool.dfcf_etf_data import dfcf_etf_data
        api=dfcf_etf_data()
        df=api.get_all_etf_data()
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_sz_sh_etf(self):
        '''
        深圳etf
        '''
        func='''
        from trader_tool.dfcf_etf_data import dfcf_etf_data
        api=dfcf_etf_data()
        df=api.get_sz_sh_etf()
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_wp_etf_data(self):
        '''
        外盘etf
        '''
        func='''
        from trader_tool.dfcf_etf_data import dfcf_etf_data
        api=dfcf_etf_data()
        df=api.get_wp_etf_data()
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_bond_etf_data(self):
        '''
        债券etf
        '''
        func='''
        from trader_tool.dfcf_etf_data import dfcf_etf_data
        api=dfcf_etf_data()
        df=api.get_bond_etf_data()
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_sp_etf_data(self):
        '''
        债券etf
        '''
        func='''
        from trader_tool.dfcf_etf_data import dfcf_etf_data
        api=dfcf_etf_data()
        df=api.get_sp_etf_data()
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_hot_spot_investment(self):
        '''
        热点投资
        '''
        func='''
        from trader_tool.dfcf_etf_data import dfcf_etf_data
        api=dfcf_etf_data()
        df=api.get_hot_spot_investment()
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_hot_spot_investment_etf(self,code='BK0437'):
        '''
        热点投资etf成分股
        get_hot_spot_investment查询代码
        '''
        func='''
        from trader_tool.dfcf_etf_data import dfcf_etf_data
        api=dfcf_etf_data()
        df=api.get_hot_spot_investment_etf(code='{}')
        print(df)
        '''.format(code)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_stock_hist_data_em(self,stock='600031',start_date='20210101',end_date='20500101',data_type='D',count=8000):
        '''
        股票行情数据
        '''
        func='''
        from trader_tool.stock_data import stock_data
        api=stock_data()
        df=api.get_stock_hist_data_em(stock='{}',start_date='{}',end_date='{}',data_type='{}',count='{}')
        print(df)
        '''.format(stock,start_date,end_date,data_type,count)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_stock_all_trader_data(self,stock='600031'):
        '''
        股票当日tick数据
        '''
        func='''
        from trader_tool.stock_data import stock_data
        api=stock_data()
        df=api.get_stock_all_trader_data(stock='{}')
        print(df)
        '''.format(stock)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_stock_spot_data(self,stock='600031'):
        '''
        股票实时数据
        '''
        func='''
        from trader_tool.stock_data import stock_data
        import pandas as pd
        api=stock_data()
        data=api.get_stock_spot_data(stock='{}')
        df=pd.DataFrame(data.items())
        print(df)    
        '''.format(stock)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_stock_spot_data_1(self,stock='600031'):
        '''
        股票实时数据1
        '''
        func='''
        from trader_tool.stock_data import stock_data
        import pandas as pd
        api=stock_data()
        df=api.get_stock_spot_data_1(stock='{}')
        print(df)    
        '''.format(stock)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_cov_bond_hist_data(self,stock='128090',start='20100101',end='20500101',limit='10000',
                                data_type='D',fqt='1',count=8000):
        '''
        可转债历史数据
        stock 证券代码
        end结束时间
        limit数据长度
        data_type数据类型：
           1 1分钟
           5 5分钟
           15 15分钟
           30 30分钟
           60 60分钟
           D 日线数据
           W 周线数据
           M 月线数据
        fqt 复权
        fq=0股票除权
        fq=1前复权
        fq=2后复权
        '''
        func='''
        from trader_tool.bond_cov_data import bond_cov_data
        api=bond_cov_data()
        df=api.get_cov_bond_hist_data(stock='{}',start='{}',end='{}',limit='{}',
                                        data_type='{}',fqt='{}',count={})
        print(df)
        '''.format(stock,start,end,limit,data_type,fqt,count)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_cov_bond_spot_trader_data(self,stock='128090'):
        '''
        可转债tick数据
        '''
        func='''
        from trader_tool.bond_cov_data import bond_cov_data
        api=bond_cov_data()
        df=api.get_cov_bond_spot_trader_data(stock='{}')
        print(df)
        '''.format(stock)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_cov_bond_spot(self,stock='128090'):
        '''
        可转债实时数据
        '''
        func='''
        from trader_tool.bond_cov_data import bond_cov_data
        import pandas as pd
        api=bond_cov_data()
        data=api.get_cov_bond_spot(stock='{}')
        df=pd.DataFrame(data.items())
        print(df)
        '''.format(stock)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_cov_bond_dish_data(self,stock='128090'):
        '''
        可转债盘口数据
        '''
        func='''
        from trader_tool.bond_cov_data import bond_cov_data
        import pandas as pd
        api=bond_cov_data()
        data=api.get_cov_bond_dish_data(stock='{}')
        df=pd.DataFrame(data.items())
        print(df)
        '''.format(stock)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def jsl_get_all_cov_bond_data(self,jsl_user='19915',jsl_password='L0'):
        '''
        获取全部可转债数据
        '''
        func='''
        from trader_tool import jsl_data
        df=jsl_data.get_all_cov_bond_data(jsl_user='{}',jsl_password='{}')
        print(df)
        '''.format(jsl_user,jsl_password)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_ETF_fund_hist_data(self,stock='159805',end='20500101',limit='1000000',
                                data_type='D',fqt='1',count=8000):
        '''
            获取ETF基金历史数据
            stock 证券代码
            end结束时间
            limit数据长度
            data_type数据类型：
            1 1分钟
            5 5分钟
            15 15分钟
            30 30分钟
            60 60分钟
            D 日线数据
            W 周线数据
            M 月线数据
            fqt 复权
            fq=0股票除权
            fq=1前复权
            fq=2后复权
            '''
        func='''
        from trader_tool.etf_fund_data import etf_fund_data
        api=etf_fund_data()
        df=api.get_ETF_fund_hist_data(stock='{}',end='{}',limit='{}',
                                        data_type='{}',fqt='{}',count={})
        print(df)
        '''.format(stock,end,limit,data_type,fqt,count)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_etf_spot_trader_data(self,stock='159805'):
        '''
        etftick数据
        '''
        func='''
        from trader_tool.etf_fund_data import etf_fund_data
        api=etf_fund_data()
        df=api.get_etf_spot_trader_data(stock='{}')
        print(df)
        '''.format(stock)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_etf_fund_spot_data(self,stock='513100'):
        '''
        etf实时数据
        '''
        func='''
        from trader_tool.etf_fund_data import etf_fund_data
        import pandas as pd
        api=etf_fund_data()
        data=api.get_etf_fund_spot_data(stock='{}')
        df=pd.DataFrame(data.items())
        print(df)
        '''.format(stock)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_hist_hot_spot_rotation(self,type='行业板块',field='涨跌幅'):
        '''
          获取历史数据
        type_dict={'概念板块':'con','行业板块':"industry"}
        field_dict={'涨跌幅':'zf','5日涨跌幅':'zf5','上涨比例':"riseRate",'涨停家数':"riseLimCnt","主力流入":"zljlr"}
        '''
        func='''
        from trader_tool.ths_hot_spot_rotation import ths_hot_spot_rotation
        api=ths_hot_spot_rotation()
        df=api.get_hist_hot_spot_rotation(type='{}',field='{}')
        print(df)
        '''.format(type,field)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_tdx_hy_data(self):
        '''
        获取通达信行业数据
        '''
        func='''
        import pandas as pd
        df=pd.read_excel(r'user_def_data\hyblock.xlsx')
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_tdx_hy_stocks_data(self,name='煤炭开采'):
        '''
        获取通达信行业成分股
        '''
        func='''
        import pandas as pd
        data=pd.read_excel(r'user_def_data\hyblock.xlsx')
        name='{}'
        data=data[data['name']==name]
        stock_list=data['stocks'].tolist()[0].replace('[','').replace(']','').replace("'",'').split(',')
        df=pd.DataFrame()
        df['stocks']=stock_list
        df['name']=data['name'].tolist()[-1]
        df['code']=data['code'].tolist()[-1]
        df['num']=data['num'].tolist()[-1]
        print(df)
        '''.format(name)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_tdx_gn_data(self):
        '''
        获取通达信概念数据
        '''
        func='''
        import pandas as pd
        df=pd.read_excel(r'user_def_data\gnblock.xlsx')
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_tdx_gn_stocks_data(self,name='煤炭开采'):
        '''
        获取通达信概念成分股
        '''
        func='''
        import pandas as pd
        data=pd.read_excel(r'user_def_data\gnblock.xlsx')
        name='{}'
        data=data[data['name']==name]
        stock_list=data['stocks'].tolist()[0].replace('[','').replace(']','').replace("'",'').split(',')
        df=pd.DataFrame()
        df['stocks']=stock_list
        df['name']=data['name'].tolist()[-1]
        df['code']=data['code'].tolist()[-1]
        df['num']=data['num'].tolist()[-1]
        print(df)
        '''.format(name)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_tdx_zs_data(self):
        '''
        获取通指数概念数据
        '''
        func='''
        import pandas as pd
        df=pd.read_excel(r'user_def_data\zsblock.xlsx')
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_tdx_zs_stocks_data(self,name='煤炭开采'):
        '''
        获取通达信指数成分股
        '''
        func='''
        import pandas as pd
        data=pd.read_excel(r'user_def_data\zsblock.xlsx')
        name='{}'
        data=data[data['name']==name]
        stock_list=data['stocks'].tolist()[0].replace('[','').replace(']','').replace("'",'').split(',')
        df=pd.DataFrame()
        df['stocks']=stock_list
        df['name']=data['name'].tolist()[-1]
        #df['code']=data['code'].tolist()[-1]
        df['num']=data['num'].tolist()[-1]
        print(df)
        '''.format(name)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_tdx_fg_data(self):
        '''
        获取通达信风格数据
        '''
        func='''
        import pandas as pd
        df=pd.read_excel(r'user_def_data\fgblock.xlsx')
        print(df)
        '''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_tdx_fg_stocks_data(self,name='煤炭开采'):
        '''
        获取通达信风格成分股
        '''
        func='''
        import pandas as pd
        data=pd.read_excel(r'user_def_data\fgblock.xlsx')
        name='{}'
        data=data[data['name']==name]
        stock_list=data['stocks'].tolist()[0].replace('[','').replace(']','').replace("'",'').split(',')
        df=pd.DataFrame()
        df['stocks']=stock_list
        df['name']=data['name'].tolist()[-1]
        df['code']=data['code'].tolist()[-1]
        df['num']=data['num'].tolist()[-1]
        print(df)
        '''.format(name)
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_bond_spot_fcator(self,date='20241101'):
        '''
        获取可转债实时因子数据
        '''
        func='''
            import pandas as pd
            df=pd.read_csv(r'C:/Users/Administrator/Desktop/集思录数据/data/实时数据\{}.csv')
        '''.format(date)
        info,df=self.get_user_def_data(func=func)
        return info,df



if __name__=='__main__':
    '''
    数据库api
    '''
    xg_data=xg_data()
    info,df=xg_data.get_all_etf_data_1()
    print(df)

    