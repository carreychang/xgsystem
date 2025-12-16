import pandas as pd
from tqdm import tqdm
import numpy as np
import json
from  trader_tool import jsl_data
from qmt_trader.qmt_trader_ths import qmt_trader_ths
from xgtrader.xgtrader import xgtrader
import numpy as np
import os
from datetime import datetime
import time
from trader_tool.unification_data import unification_data
from trader_tool.xms_quant_bond_user_factor_trader import xms_quant_bond_user_factor_trader
class simmons_convertible_bond_3_low_system:
    def __init__(self,trader_tool='ths',exe='C:/同花顺软件/同花顺/xiadan.exe',tesseract_cmd='C:/Program Files/Tesseract-OCR/tesseract',
                qq='1029762153@qq.com',open_set='否',qmt_path='D:/国金QMT交易端模拟/userdata_mini',
                qmt_account='55009640',qmt_account_type='STOCK',
                name='run_simmons_convertible_bond_3_low_system',
                data_api='qmt'):
        '''
        西蒙斯可转债3低交易策略     
        '''
        self.data_api=data_api
        self.exe=exe
        self.tesseract_cmd=tesseract_cmd
        self.qq=qq    
        self.trader_tool=trader_tool
        self.open_set=open_set
        self.qmt_path=qmt_path
        self.qmt_account=qmt_account
        self.qmt_account_type=qmt_account_type
        if trader_tool=='ths':
            self.trader=xgtrader(exe=self.exe,tesseract_cmd=self.tesseract_cmd,open_set=open_set)
        else:
            self.trader=qmt_trader_ths(path=qmt_path,account=qmt_account,account_type=qmt_account_type)
       
        self.path=os.path.dirname(os.path.abspath(__file__))
        self.name=name
        with open(r'{}/西蒙斯可转债3低交易策略.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        self.url=text['服务器']
        self.port=text['端口']
        self.unification_data=unification_data(data_api=self.data_api,trader_tool=self.trader_tool)
        self.data=self.unification_data.get_unification_data()
        with open(r'分析配置.json',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        cash_set=text['多策略资金设置']
        name_list=list(cash_set.keys())
        if  self.name in name_list:
            hold_limit=cash_set[self.name]['持股限制']
        else:
            hold_limit=cash_set['其他策略']['持股限制']
        with open(r'{}\西蒙斯可转债3低交易策略.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        text['持股限制']=hold_limit
        text['持有限制']=hold_limit
        #保存
        with open(r'{}\西蒙斯可转债3低交易策略.json'.format(self.path),'w',encoding='utf-8') as f:
            json.dump(text, f,ensure_ascii=False,indent=2)
        self.trader.connect()
        self.redeem=pd.DataFrame()
    def save_position(self):
        '''
        保存持股数据
        '''
        with open(r'分析配置.json',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        del_df=pd.read_excel(r'{}\黑名单\黑名单.xlsx'.format(self.path),dtype='object')
        del_trader_stock=text['黑名单']
        if del_df.shape[0]>0:
            del_df['证券代码']=del_df['证券代码'].apply(lambda x : str(x).split('.')[0])
            del_df['证券代码']=del_df['证券代码'].apply(lambda x: '0'*(6-len(str(x)))+str(x))
            del_stock_list=del_df['证券代码'].tolist()
        else:
            del_stock_list=[]
        for del_stock in del_trader_stock:
            del_stock_list.append(del_stock)
        def select_del_stock_list(x):
            if str(x)[:6] in del_stock_list:
                return '是'
            else:
                return '否'
        df=self.trader.position()
        def select_bond_cov(x):
            '''
            选择可转债
            '''
            if x[:3] in ['110','113','123','127','128','111','118'] or x[:2] in ['11','12']:
                return '是'
            else:
                return '不是'
        try:
            if df==False:
                print('获取持股失败')
        except:
            if df.shape[0]>0:
                df['选择']=df['证券代码'].apply(select_bond_cov)
                try:
                    df['持股天数']=df['持股天数'].replace('--',1)
                except:
                    df['持股天数']=1
                df1=df[df['选择']=='是']
                df1=df1[df1['股票余额']>=10]
                df1['黑名单']=df1['证券代码'].apply(select_del_stock_list)
                df1=df1[df1['黑名单']=='否']
                print('剔除黑名单**********')
                df1.to_excel(r'持股数据\持股数据.xlsx')
                return df1
            else:
                df=pd.DataFrame()
                df['账号类型']=None
                df['资金账号']=None
                df['证券代码']=None
                df['股票余额']=None
                df['可用余额']=None
                df['成本价']=None
                df['市值']=None
                df['选择']=None
                df['持股天数']=None
                df['交易状态']=None
                df['明细']=None
                df['证券名称']=None
                df['冻结数量']=None
                df['市价']=None	
                df['盈亏']=None
                df['盈亏比(%)']=None
                df['当日买入']=None	
                df['当日卖出']=None
                df.to_excel(r'持股数据\持股数据.xlsx')
                return df
        print(df)
    def select_bond_cov(self,x):
        '''
        选择证券代码
        '''
        if x[:3] in ['110','113','123','127','128','111'] or x[:2] in ['11','12']:
            return '是'
        else:
            return '不是'
    def save_balance(self):
        '''
        保持账户数据
        '''
        with open(r'{}/西蒙斯可转债3低交易策略.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        df=self.trader.balance()
        df.to_excel(r'账户数据\账户数据.xlsx')
        return df
    def get_trader_list(self,stock='000001',start_date='19990101',end_date='20500101'):
        '''
        获取交易日历
        '''
        hist=self.data.get_hist_data_em(stock=stock,end_date=end_date,start_date=start_date)
        date_list=hist.index.tolist()
        return date_list
    def get_select_stock(self):
        with open(r'{}/西蒙斯可转债3低交易策略.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        test=text['是否测试']
        test_date=text['测试时间']
        table=text['数据表']
        print('读取{} 表数据**************************'.format(table))
        if test=='是':
            print('开启测试数据***************实盘关闭')
            now_date=test_date
        else:
            now_date=''.join(str(datetime.now())[:10].split('-'))
        api=xms_quant_bond_user_factor_trader(
            data_type=table,
            url=self.url,
            port=self.port,
            text=text,
            date=now_date
            )
        stats,df,self.redeem=api.get_select_result()
        
        if df.shape[0]>0:
            print(now_date,'可转债获取成功*********************')
            stats,df=stats,df
        else:
            stats=False
            df=pd.DataFrame()
        return stats,df
        
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    def get_buy_sell_stock(self):
        '''
        获取买卖数据
        '''
        with open('{}/西蒙斯可转债3低交易策略.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        buy_num=text['持有排名前N']
        hold_rank_num=text['持有排名前N']
        hold_limit=text['持有限制']
        stats,df=self.get_select_stock()
        if stats==True or stats=='True' or stats=='true':
            df['证券代码']=df['转债代码']
            df['证券代码']=df['证券代码'].astype(str)
            print('可转债数据获取成功开始分析**********')
            hold_stock=pd.read_excel(r'持股数据\持股数据.xlsx')
            if hold_stock.shape[0]>0:
                hold_stock=hold_stock[hold_stock['股票余额']>=10]
                if hold_stock.shape[0]>0:
                    hold_stock['证券代码']=hold_stock['证券代码'].astype(str)
                    hold_stock['品种']=hold_stock['证券代码'].apply(lambda x: self.trader.select_data_type(x))
                    hold_stock=hold_stock[hold_stock['品种']=='bond']
                    if hold_stock.shape[0]>0:
                        hold_stock_list=hold_stock['证券代码'].tolist()
                    else:
                        hold_stock_list=[]
                else:
                    hold_stock_list=[]
            else:
                hold_stock_list=[]
            sell_list=[]
            buy_list=[]
            if len(hold_stock_list)>0:
                buy_ranK_stock=df['证券代码'].tolist()[:buy_num]
                hold_rank_stock=df['证券代码'].tolist()[:hold_rank_num]
                for stock in hold_stock_list:
                    if stock not in hold_rank_stock:
                        print(stock,'不在持有排行前{}卖出'.format(hold_rank_num))
                        sell_list.append(stock)
                    else:
                        print(stock,'在持有排名前{} 大于{}继续持有'.format(hold_rank_stock.index(stock),hold_rank_num))
                for stock in buy_ranK_stock:
                    if stock not in hold_stock_list:
                        print(stock,'在买入排名前{}没有持股买入'.format(buy_ranK_stock.index(stock)))
                        buy_list.append(stock)
                    else:
                        print(stock,'在买入排名前{}在持股不买入'.format(hold_rank_stock.index(stock)))
            else:
                sell_list=[]
                buy_list=df['证券代码'].tolist()[:hold_limit]
            #剔除强制赎回自动卖出
            if self.redeem.shape[0]>0:
                print('剔除强制赎回自动卖出*******************,强制赎回代码')
                self.redeem['转债代码']=self.redeem['转债代码'].astype(str)
                redeem_list=self.redeem['转债代码'].tolist()
                print(redeem_list)
                for stock in hold_stock_list:
                    if str(stock) in redeem_list:
                        print(stock,'持股在强制数据里面自动卖出')
                        sell_list.append(stock)
                    else:
                        pass
            else:
                print('剔除强制赎回自动卖出没有持股数据')
            hold_amount=len(hold_stock_list)
            sell_amount=len(sell_list)
            av_amount=(hold_limit-hold_amount)+sell_amount
            if av_amount>0:
                av_amount=av_amount
            else:
                print('达到持股限制{} 不买入'.format(hold_limit))
                av_amount=0
            buy_list=buy_list[:av_amount]  
            buy_df=pd.DataFrame()
            buy_df['证券代码']=buy_list
            buy_df['策略名称']=self.name
            buy_df['交易状态']='未买'
            buy_df.to_excel(r'买入股票\买入股票.xlsx')
            sell_df=pd.DataFrame()
            sell_df['证券代码']=sell_list
            sell_df['策略名称']=self.name
            sell_df['交易状态']='未卖'
            sell_df.to_excel(r'卖出股票\卖出股票.xlsx')
            print('买入股票*******************')
            print(buy_df)
            print('卖出股票*******************')
            print(sell_df)
        else:
            print('没有符合选股轮动的**************')
    def get_time_rotation(self):
        '''
        轮动方式
        '''
        with open('{}/西蒙斯可转债3低交易策略.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        now_date=''.join(str(datetime.now())[:10].split('-'))
        now_time=time.localtime()                               
        trader_type=text['轮动方式']                               
        trader_wday=text['每周轮动时间']                               
        moth_trader_time=text['每月轮动时间']
        specific_time=text['特定时间']
        year=now_time.tm_year
        moth=now_time.tm_mon
        wday=now_time.tm_wday
        daily=now_time.tm_mday
        if trader_type=='每天':
            print('轮动方式每天')
            return True
        elif trader_type=='每周':
            if trader_wday==wday:
                return True
            elif trader_wday<wday:
                print('安周轮动 目前星期{} 轮动时间星期{} 目前时间大于轮动时间不轮动'.format(wday+1,trader_wday+1))
                return False
            else:
                print('安周轮动 目前星期{} 轮动时间星期{} 目前时间小于轮动时间不轮动'.format(wday+1,trader_wday+1))
                return False
        elif trader_type=='每月轮动时间':
            stats=''
            for date in moth_trader_time:
                data=''.join(data.split('-'))
                if int(moth_trader_time)==int(date):
                    print('安月轮动 目前{} 轮动时间{} 目前时间等于轮动时间轮动'.format(now_date,date))
                    stats=True
                    break
                elif int(moth_trader_time)<int(date):
                    print('安月轮动 目前{} 轮动时间{} 目前时间小于轮动时间轮动'.format(now_date,date))
                    stats=False
                else:
                    print('安月轮动 目前{} 轮动时间{} 目前时间大于轮动时间轮动'.format(now_date,date))
                    stats=False
            return stats
        else:
            #特别时间
            stats=''
            for date in specific_time:
                data=''.join(data.split('-'))
                if int(specific_time)==int(date):
                    print('安月轮动 目前{} 轮动时间{} 目前时间等于轮动时间轮动'.format(now_date,date))
                    stats=True
                    break
                elif int(specific_time)<int(date):
                    print('安月轮动 目前{} 轮动时间{} 目前时间小于轮动时间轮动'.format(now_date,date))
                    stats=False
                else:
                    print('安月轮动 目前{} 轮动时间{} 目前时间大于轮动时间轮动'.format(now_date,date))
                    stats=False
            return stats  
    def updata_all_data(self):
        '''
        更新全部数据
        '''
        with open(r'{}/西蒙斯可转债3低交易策略.json'.format(self.path),encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        if self.get_time_rotation()==True:
            print("今天{} 是轮动时间".format(datetime.now()))
            self.save_position()
            self.save_balance()
            self.get_buy_sell_stock()
            
        else:
            print("今天{} 不是是轮动时间".format(datetime.now()))