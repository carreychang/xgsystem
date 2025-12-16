from trader_tool.unification_data import unification_data
from trader_tool.trader_frame import trader_frame
from trader_tool.analysis_models import analysis_models
from trader_tool.shape_analysis import shape_analysis
from user_def_models import user_def_models
import pandas as pd
from tqdm import tqdm
import numpy as np
import time
import json
from datetime import datetime
import schedule
import yagmail
from trader_tool.base_func import base_func
from trader_tool.decode_trader_password import decode_trader_password
from custom_trading_modules.custom_trading_modules import custom_trading_modules
from custom_hist_trading_modules.custom_hist_trading_modules import custom_hist_trading_modules
from trader_tool.seed_trader_info import seed_trader_info
from trader_tool.del_qmt_userdata_mini import del_qmt_userdata_mini
class trader_strategy:
    def __init__(self,trader_tool='ths',exe='C:/同花顺软件/同花顺/xiadan.exe',tesseract_cmd='C:/Program Files/Tesseract-OCR/tesseract',
                qq='1029762153@qq.com',open_set='否',qmt_path='D:/国金QMT交易端模拟/userdata_mini',
                qmt_account='55009640',qmt_account_type='STOCK',slippage=0.01,data_api='qmt'):
        '''
        参数配置
        '''
        print('################################################################################################')
        print("""
        风险提示：
        1.以下为量化交易模型，主要内容来源于互联网学习加工，分享的核心是交易思路框架，标的范围和参数仅为学习输出的举例，不能直接运用于交易。
        2.思路框架仅供学习参考，各位投资者朋友需根据自己的需求搭建自己的交易体系和具体策略。
        3.量化交易过程中可能涉及数据准确性、系统BUG、操作不当等风险，交易之前请务必自行充分学习。股市有风险，投资需谨慎和自主决策！
              """)
        print('################################################################################################')
        self.data_api=data_api
        self.exe=exe
        self.tesseract_cmd=tesseract_cmd
        self.qq=qq
        self.trader_tool=trader_tool
        self.open_set=open_set
        self.qmt_path=qmt_path
        self.qmt_account=qmt_account
        self.qmt_account_type=qmt_account_type
        self.slippage=slippage
        self.user_def_models=user_def_models(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                 open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                 qmt_account_type=self.qmt_account_type)
        order_frame=trader_frame(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                 open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                 qmt_account_type=self.qmt_account_type,slippage=self.slippage)
        self.trader=order_frame.get_trader_frame()
        data=unification_data(trader_tool=self.trader_tool,data_api=self.data_api)
        self.data=data.get_unification_data()
        self.analysis_models=analysis_models()
        self.shape_analysis=shape_analysis()
        self.base_func=base_func()
        self.password=decode_trader_password()
        

    def connact(self):
        '''
        链接同花顺
        '''
        try:
            self.trader.connect()
            return True
        except Exception as e:
            print("运行错误:",e)
            print('{}连接失败'.format(self.trader_tool))
            return False

    
    def check_cov_bond_av_trader(self,stock='128106'):
        '''
        检查可转债是否可以交易
        '''
        with open(r'分析配置.json',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        del_stock=text['黑名单']
        if stock in del_stock:
            print('{}黑名单'.format(stock))
            return False
        else:
            return True
    def check_stock_is_av_buy(self,stock='128036',price='156.700',amount=10):
        '''
        检查是否可以买入
        '''
        price=float(price)
        amount=float(amount)
        with open(r'分析配置.json',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        hold_limit=text['持股限制']
        stats=self.trader.check_stock_is_av_buy(stock=stock,price=price,amount=amount,hold_limit=hold_limit)
        return stats
    def check_stock_is_av_sell(self,stock='128036',amount=10):
        '''
        检查是否可以卖出
        '''
        stats=self.trader.check_stock_is_av_sell(stock=stock,amount=amount)
        return stats
    def check_av_target_tarder(self,stock='600031',price=2.475,trader_type='buy',name=''):
        '''
        检查目标交易
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        stock=str(stock)
        cash_set=text['多策略资金设置']
        is_open=text['是否开启特殊标的']
        name_list=list(cash_set.keys())
        if name in name_list:
            text1=cash_set[name]
            st_name=text1['策略名称']
            down_type=text1['交易模式']

            value=text1['固定交易资金']
            sell_value=text1['卖出资金']
            value_limit=text1['持有金额限制']

            amount=text1['固定交易数量']
            sell_amount=text1['卖出数量']
            amount_limit=text1['持有数量限制']

            ratio=text1['交易百分比']
            sell_ratio=text1['卖出百分比']
            ratio_limt=text1['持有百分比']

        else:
            text1=cash_set['其他策略']
            st_name=text1['策略名称']
            down_type=text1['交易模式']

            value=text1['固定交易资金']
            sell_value=text1['卖出资金']
            value_limit=text1['持有金额限制']

            amount=text1['固定交易数量']
            sell_value=text1['卖出资金']
            amount_limit=text1['持有数量限制']

            ratio=text1['交易百分比']
            sell_ratio=text1['卖出百分比']
            ratio_limt=text1['持有百分比']
        if is_open=='是':
            special_stock=text['特殊标的']
        else:
            special_stock=[]
        special_value=text['特殊固定交易资金']
        special_limit_value=text['特殊持有金额限制']
        trader_stock=self.trader.select_data_type(stock)
        if stock in special_stock:
            down_type='金额'
            value=special_value
            sell_value=value
            value_limit=special_limit_value
        else:
            pass
        if trader_type=='sell':
            #检查是否可以卖出
            if down_type=='数量':
                stats=self.trader.check_stock_is_av_sell(stock=stock,amount=amount)
                if stats==True:
                    trader_type='sell'
                    amount=amount
                    price=price
                else:
                    trader_type=''
                    amount=amount
                    price=price
            elif down_type=='金额':
                trader_type,amount,price=self.trader.order_value(stock=stock,value=sell_value,price=price,trader_type=trader_type)
            elif down_type=='百分比':
                trader_type,amount,price=self.trader.order_percent(stock=stock,percent=sell_ratio,price=price,trader_type=trader_type)
            else:
                print('未知的交易类型{} 交易类型{} 下单类型{} 数量{}  价格{}'.format(stock,trader_type,down_type,amount,price))
                trader_type=''
                amount=amount
                price=price
        elif trader_type=='buy':
            #检查是否委托
            if down_type=='数量':
                trader_type,amount_1,price=self.trader.order_target_volume(stock=stock,amount=amount_limit,price=price)
                if trader_type=='buy':
                    av_buy=self.trader.check_stock_is_av_buy(stock=stock,amount=amount,price=price)
                    if av_buy==True:
                        trader_type='buy'
                        amount=amount
                        price=price
                    else:
                        trader_type=''
                        amount=amount
                        price=price
            elif down_type=='金额':
                trader_type,amount_1,price=self.trader.order_target_value(stock=stock,value=value_limit,price=price)
                if trader_type=='buy' and amount_1>=10:
                    trader_type,amount,price=self.trader.order_value(stock=stock,value=value,price=price,trader_type=trader_type)
                else:
                    trader_type=''
                    amount=amount
                    price=price
            elif down_type=='百分比':
                trader_type,amount_1,price=self.trader.order_target_percent(stock=stock,target_percent=ratio_limt,price=price)
                if trader_type=='buy' and amount_1>=10:
                    trader_type,amount,price=self.trader.order_percent(stock=stock,percent=ratio,price=price,trader_type=trader_type)
                else:
                    trader_type=''
                    amount=amount
                    price=price
            else:
                print('未知的交易类型{} 交易类型{} 下单类型{} 数量{} 价格{}'.format(stock,trader_type,down_type,amount,price))
                trader_type=''
                amount=amount
                price=price
        else:
            print('未知道下单类型{} 交易类型{} 下单类型{} 数量{} 价格{}'.format(stock,trader_type,down_type,amount,price))
            trader_type=''
            amount=amount
            price=price
            amount=int(amount)
        if trader_type=='sell' and abs(amount)>=10:
            amount=abs(amount)
        else:
            pass
        print('时间{} 策略名称{} 交易类型{} 交易数量{} 交易价格'.format(datetime.now(),st_name,trader_type,amount,price))
        return trader_type,amount,price
    def check_is_trader_date_1(self):
        '''
        检测是不是交易时间
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        password=text['软件授权码']
        trader_time=text['交易时间段']
        start_date=text['交易开始时间']
        end_date=text['交易结束时间']
        start_mi=text['开始交易分钟']
        jhjj=text['是否参加集合竞价']
        stats=self.password.decode_trader_password()
        if stats==True:
            if jhjj=='是':
                jhjj_time=15
            else:
                jhjj_time=30
            loc=time.localtime()
            tm_hour=loc.tm_hour
            tm_min=loc.tm_min
            wo=loc.tm_wday
            if wo<=trader_time:
                if tm_hour>=start_date and tm_hour<=end_date:
                    if tm_hour==9 and tm_min<jhjj_time:
                        return False
                    elif tm_min>=start_mi:
                        return True
                    else:
                        return False
                else:
                    return False    
            else:
                print('周末')
                return False
        else:
            print('**************软件授权码不正确联系作者微信15117320079**************')
            return False
    def run_stock_trader_buy(self):
        '''
        运行交易策略 可转债,买入
        '''
        if self.check_is_trader_date_1()==True:

            with open('分析配置.json','r+',encoding='utf-8') as f:
                com=f.read()
            text=json.loads(com)
            max_zdf=text['买入时间的涨跌幅上限']
            min_zdf=text['买入时间的涨跌幅下限']
            name=text['策略名称']
            today_sell_not_buy=text['是否开启当日卖出不买入模块']
            trader_stats=[]
            df=pd.read_excel(r'买入股票\买入股票.xlsx',dtype='object')
            try:
                del df['Unnamed: 0']
            except Exception as e:
                print("运行错误:",e)
            if df.shape[0]>0:
                if today_sell_not_buy=='是':
                    print('开启当日卖出不买入模块*****')
                    today_entrusts=self.trader.today_entrusts()
                    #剔除列表
                    del_list=[57,54]
                    if today_entrusts.shape[0]>0:
                        today_entrusts['证券代码']=today_entrusts['证券代码'].apply(lambda x: '0'*(6-len(str(x)))+str(x))
                        today_entrusts['剔除']=today_entrusts['委托状态'].apply(lambda x: '是' if x in del_list else '不是')
                        today_entrusts=today_entrusts[today_entrusts['剔除']=='不是']
                        if today_entrusts.shape[0]>0:
                            #委托状态
                            today_entrusts=today_entrusts[today_entrusts['委托类型']==24]
                            if today_entrusts.shape[0]>0:
                                sell_stock_list=today_entrusts['证券代码'].tolist()
                            else:
                                sell_stock_list=[]
                        else:
                            sell_stock_list=[]
                    else:
                        sell_stock_list=[]
                else:
                    print('不开启当日卖出不买入模块')
                    sell_stock_list=[]
                if '策略名称' in df.columns.tolist():
                    pass
                else:
                    df['策略名称']='其他策略'
                df['证券代码']=df['证券代码'].apply(lambda x: '0'*(6-len(str(x)))+str(x))
                for stock,stats,name in zip(df['证券代码'].tolist(),df['交易状态'].tolist(),df['策略名称'].tolist()):
                    stock=str(stock)
                    try:
                        if stats=='未买':
                            if stock in sell_stock_list:
                                print('{} 在当天卖出列表不买入{}'.format(stock))
                                trader_stats.append('已买')
                            else:
                                spot_data=self.data.get_spot_data(stock=stock) 
                                #价格
                                price=spot_data['最新价']
                                lof_list=text['lof基金列表']
                                stock=str(stock)
                                if stock[:6] in lof_list:
                                    price=price/10
                                else:
                                    price=price
                                #实时涨跌幅
                                zdf=spot_data['涨跌幅']
                                if zdf<=max_zdf and zdf>=min_zdf:
                                    trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='buy',name=name)
                                    if trader_type=='buy':
                                        if self.trader_tool=='ths':
                                            self.trader.buy(security=stock,price=price,amount=amount)
                                        else:
                                            self.trader.buy(security=stock,price=price,amount=amount,strategy_name=name,order_remark=name)
                                        msg="""
                                        策略：{},
                                        股票：{},
                                        操作:买入,
                                        价格:{},
                                        数量:{},
                                        时间:{}
                                        """.format(name,stock,price,amount,datetime.now())
                                        self.seed_emial_qq(text=msg)
                                        trader_stats.append('已买')
                                        
                                    else:
                                        trader_stats.append('已买')
                                else:
                                    print('时间{} 代码{} 涨跌幅{}不在涨跌幅范围'.format(datetime.now(),stock,zdf))
                                    trader_stats.append('未买')
                        else:
                            print('{}循环买入{}已经买入'.format(datetime.now(),stock))
                            trader_stats.append('已买')
                    except Exception as e:
                        print("运行错误:",e)
                        print('循环买入{}有问题'.format(stock))
                        trader_stats.append(stats)
                df['交易状态']=trader_stats
                df.to_excel(r'买入股票\买入股票.xlsx') 
            else:
                print('买入可转债为空')
        else:
            print('{}目前不是交易时间'.format(datetime.now()))
    def run_stock_trader_sell(self):
        '''
        运行交易策略 股票,策略卖出
        '''
        if self.check_is_trader_date_1()==True:
            with open('分析配置.json','r+',encoding='utf-8') as f:
                com=f.read()
            text=json.loads(com)
            stats_list=[]
            df=pd.read_excel(r'卖出股票\卖出股票.xlsx',dtype='object')
           
            try:
                del df['Unnamed: 0']
            except Exception as e:
                print("运行错误:",e)
            if df.shape[0]>0:
                if '策略名称' in df.columns.tolist():
                    pass
                else:
                    df['策略名称']='其他策略'
                df['证券代码']=df['证券代码'].apply(lambda x: '0'*(6-len(str(x)))+str(x))
                for stock,stats,name in zip(df['证券代码'].tolist(),df['交易状态'].tolist(),df['策略名称'].tolist()):
                    name=str(name)
                    try:
                    
                        stock=str(stock)
                        if stats=='未卖':
                            spot_data=self.data.get_spot_data(stock=stock)
                            #价格
                            price=spot_data['最新价']
                            lof_list=text['lof基金列表']
                            stock=str(stock)
                            if stock[:6] in lof_list:
                                price=price/10
                            else:
                                price=price
                            stock=str(stock)
                            trader_type,amount,price=self.check_av_target_tarder(stock=stock,price=price,trader_type='sell',name=name)
                            if trader_type=='sell':
                                if self.trader_tool=='ths':
                                    self.trader.sell(security=stock,price=price,amount=amount)
                                else:
                                    self.trader.sell(security=stock,price=price,amount=amount,strategy_name=name,order_remark=name)
                                msg="""
                                    策略：{},
                                    股票：{},
                                    操作:卖出,
                                    价格:{},
                                    数量:{},
                                    时间:{}
                                    """.format(name,stock,price,amount,datetime.now())
                                self.seed_emial_qq(text=msg)
                                stock=str(stock)
                                stats_list.append('已卖')
                                
                            else:
                                stats_list.append('已卖')  
                        else:
                            print("不是卖出状态{}".format(stats))
                            stats_list.append("已卖")
                    
                    except Exception as e:
                        print("运行错误:",e)
                        print('循环卖出{}有问题'.format(stock))
                        stats_list.append(stats)
                        
                df['交易状态']=stats_list
                df.to_excel(r'卖出股票\卖出股票.xlsx')  
            else:
                    print('没有卖出的标的')
        else:
            print('{}目前不是交易时间'.format(datetime.now()))
    def save_account_data(self):
        '''
        保持账户数据
        '''
        #if self.check_is_trader_date_1()==True:
        with open(r'分析配置.json',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        del_stock_list=text['黑名单']
        print(del_stock_list)
        def select_del_stock_list(x):
            if str(x)[:6] in del_stock_list:
                return '是'
            else:
                return '否'
        if True:
            #持股
            try:
                position=self.trader.position()
                position['黑名单']=position['证券代码'].apply(select_del_stock_list)
                position=position[position['黑名单']=='否']
                print('剔除黑名单**********')
                position['标的类型']=position['证券代码'].apply(self.base_func.select_data_type)
                trader_type=text['交易品种']
                if trader_type=='全部':
                    position=position[position['股票余额']>=10]
                    position.to_excel(r'持股数据\持股数据.xlsx')
                else:
                    position=position[position['股票余额']>=10]
                    position=position[position['标的类型']==trader_type]
                print('账户数据获取成功')
                position.to_excel(r'持股数据\持股数据.xlsx')
                print(position)
            except Exception as e:
                print("运行错误:",e)
                print('获取持股失败')
            #账户
            try:
                account=self.trader.balance()
                account.to_excel(r'账户数据\账户数据.xlsx')
                print('获取账户成功')
                print(account)
            except Exception as e:
                print("运行错误:",e)
                print('获取账户失败')
            
    
    def run_user_def_trader_models(self):
        '''
        运行自定义交易模型
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        if True:
            user_def_type=text['自定义函数运行类型']
            user_def_time=text['自定义函数模块运行时间']
            user_def_func=text['自定义函数']
            for def_type,def_time,def_func in zip(user_def_type,user_def_time,user_def_func):
                func='self.user_def_models.{}'.format(def_func)
                if def_type=='定时':
                    schedule.every().day.at('{}'.format(def_time)).do(eval(func))
                    print('{}运行自定义分析模型{}函数在{}'.format(def_type,def_func,def_time))
                else:
                    schedule.every(def_time).minutes.do(eval(func))
                    print('{}运行自定义分析模型{}函数每{}分钟'.format(def_type,def_func,def_time))
    def seed_emial_qq(self,text=','):
        '''
        发生交易通知
        '''
        msg=text
        msg+=','
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        seed_type=text['发送方式']
        seed_qq=text['发送qq']
        qq_paasword=text['qq掩码']
        re_qq=text['接收qq']
        dd_token_list=text['钉钉账户token']
        wx_token_list=text['微信token']
        seed=seed_trader_info(seed_type,
                seed_qq,
                qq_paasword,
                re_qq,
                dd_token_list,
                wx_token_list)
        seed.seed_trader_info(msg)
    def check_is_today_entrusts(self,trader_type='buy',stock='600031.SH',amount=100):
        '''
        检查是否已经委托
        '证券代码','交易类型','委托数量'
        '''
        stock=str(stock)[:6]
        data_list=['证券代码','交易类型','委托数量']
        df=self.trader.today_entrusts()
        if df.shape[0]>0:
            df['交易类型']=df['委托类型'].apply(lambda x: 'buy' if x==23 else 'sell')
            df=df[df['委托状态翻译'] !='已撤']
            df=df[df['证券代码']==stock]
            df=df[df['交易类型']==trader_type]
            df=df[df['委托数量']==amount]
            if df.shape[0]>0:
                print(stock,trader_type,amount,'可能已经委托不重新委托')
                return False
            else:
                print(stock,trader_type,amount,'没有委托可以委托')
                return True
        else:
            print(stock,trader_type,amount,'账户没有委托数据可以委托')
            return True
    
    def run_custom_trading_modules_hold_stock(self):
        '''
        持股运行自定义交易模型
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        user_models=text['自定义交易持股模块']
        tarder_stock=text['监测股票池']
        name_list=list(user_models.keys())
        if self.check_is_trader_date_1()==True:
            now_date=datetime.now()
            trader_date=str(datetime.now())[:10]
            if tarder_stock=='持股':
                df=pd.read_excel(r'持股数据\持股数据.xlsx')
            else:
                df=pd.read_excel(r'自定义股票池\自定义股票池.xlsx')
            if df.shape[0]>0:
                df['证券代码']=df['证券代码'].apply(lambda x: '0'*(6-len(str(x)))+str(x))
            else:
                pass
            log=pd.read_excel(r'自定义模块交易记录\自定义模块交易记录.xlsx')
            log=log[['证券代码','模块名称','交易时间','触发时间','触发的价格','资金类型','交易值','持有值','交易类型']]
            log['触发时间']=log['触发时间'].astype(str)
            log['证券代码']=log['证券代码'].astype(str)
            now_date=datetime.now()
            trader_date=str(datetime.now())[:10]
            #读取今天
            log=log[log['交易时间']==trader_date]
            if df.shape[0]>0:
                df['证券代码']=df['证券代码'].apply(lambda x: '0'*(6-len(str(x)))+str(x))
                for stock,cost_price in zip(df['证券代码'].tolist(),df['成本价'].tolist()):
                    try:
                        for name in name_list:
                            user_set=user_models[name]
                            func=user_set['函数名称']
                            is_open=user_set['是否开启']
                            cash_type=user_set['资金模型']
                            sell_value=user_set['卖出值']
                            buy_value=user_set['买入值']
                            limit_value=user_set['持有值']
                            data_type=user_set['数据类型']
                            is_other_data=user_set['是否开启其他数据']
                            other_data_type=user_set['其他数据类型']
                            #
                            #print(user_set)
                            limit=user_set['是否成本价要求']
                            #最低收益
                            min_zdf=user_set['卖出大于成本价N%']
                            if is_open=='是':
                                spot_data=self.data.get_spot_data(stock=stock)
                                price=spot_data['最新价']
                                #目前的涨跌幅
                                zdf=((price-cost_price)/cost_price)*100

                                lof_list=text['lof基金列表']
                                stock=str(stock)
                                if stock[:6] in lof_list:
                                    price=price
                                else:
                                    price=price
                                if data_type=='历史行情':
                                    hist=self.data.get_hist_data_em(stock=stock)
                                    hist['证券代码']=stock
                                elif data_type=='高频行情':
                                    hist=self.data.get_spot_trader_data(stock=stock)
                                    hist['证券代码']=stock
                                else:
                                    data_dict = {'1分钟行情': '1',
                                                '5分钟行情': '5', 
                                                '15分钟行情': '15',
                                                '30分钟行情': '30',
                                                '60分钟行情': '60',
                                                '日线行情': 'D',
                                                '周线行情': 'W',
                                                '月线行情': 'M'}
                                    hist=self.data.get_hist_data_em(stock=stock,data_type=data_dict.get(data_type,'D'))
                                    hist['证券代码']=stock
                                if is_other_data=='是':
                                    if other_data_type=='历史行情':
                                        other_data=self.data.get_hist_data_em(stock=stock)
                                        other_data['证券代码']=stock
                                    elif other_data_type=='高频行情':
                                        other_data=self.data.get_spot_trader_data(stock=stock)
                                        other_data['证券代码']=stock
                                    else:
                                        data_dict = {'1分钟行情': '1',
                                                    '5分钟行情': '5', 
                                                    '15分钟行情': '15',
                                                    '30分钟行情': '30',
                                                    '60分钟行情': '60',
                                                    '日线行情': 'D',
                                                    '周线行情': 'W',
                                                    '月线行情': 'M'}
                                        other_data=self.data.get_hist_data_em(stock=stock,data_type=data_dict.get(data_type,'D'))
                                        other_data['证券代码']=stock
                                else:
                                    other_data=''

                                models=custom_trading_modules(stock=stock,df=hist,spot_data=spot_data,other_data=other_data)
                                func='models.{}'.format(func)
                                trader_type=eval(func)
                                if trader_type=='buy':
                                    if cash_type=='数量':
                                        #检查目标持股限制
                                        trader_type,amount,price=self.trader.order_target_volume(stock=stock,amount=limit_value,price=price)
                                    elif cash_type=='金额':
                                        trader_type,amount,price=self.trader.order_target_value(stock=stock,value=limit_value,price=price)
                                    elif cash_type=='百分比':
                                        trader_type,amount,price=self.trader.order_target_percent(stock=stock,target_percent=limit_value,price=price)
                                    else:
                                        trader_type=''
                                        amount=''
                                        price=''
                                    if trader_type=='buy':
                                        if cash_type=='数量':
                                            amount=buy_value
                                            if self.trader_tool=='ths':
                                                self.trader.buy(security=stock,price=price,amount=buy_value)
                                            else:
                                                self.trader.buy(security=stock,price=price,amount=buy_value,strategy_name=name,order_remark=name)
                                                
                                        elif cash_type=='金额':
                                            trader_type,amount,price=self.trader.order_value(stock=stock,value=buy_value,price=price,trader_type='buy')
                                            if trader_type=='buy' and amount>=10:
                                                if self.trader_tool=='ths':
                                                    self.trader.buy(security=stock,price=price,amount=amount)
                                                else:
                                                    self.trader.buy(security=stock,price=price,amount=amount,strategy_name=name,order_remark=name)
                                            else:
                                                pass
                                        elif cash_type=='百分比':
                                            trader_type,amount,price=self.trader.order_percent(stock=stock,percent=buy_value,price=price,trader_type='buy')
                                            if trader_type=='buy' and amount>=10:
                                                if self.trader_tool=='ths':
                                                    self.trader.buy(security=stock,price=price,amount=amount)
                                                else:
                                                    self.trader.buy(security=stock,price=price,amount=amount,strategy_name=name,order_remark=name)
                                                msg="""
                                                    策略：{},
                                                    股票：{},
                                                    操作:买入,
                                                    价格:{},
                                                    数量:{},
                                                    时间:{}
                                                    """.format(name,stock,price,amount,datetime.now())
                                                self.seed_emial_qq(text=msg)
                                            else:
                                                pass
                                        else:
                                            pass
                                elif trader_type=='sell': 
                                    if limit=='是':
                                        if zdf>=min_zdf:
                                            if cash_type=='数量':
                                                amount=sell_value
                                                if self.trader_tool=='ths':
                                                    self.trader.sell(security=stock,price=price,amount=sell_value)
                                                else:
                                                    self.trader.sell(security=stock,price=price,amount=sell_value,strategy_name=name,order_remark=name)
                                            elif cash_type=='金额':
                                                trader_type,amount,price=self.trader.order_value(stock=stock,value=sell_value,price=price,trader_type='sell')
                                                if trader_type=='sell' and amount>=10:
                                                    if self.trader_tool=='ths':
                                                        self.trader.sell(security=stock,price=price,amount=amount)
                                                    else:
                                                        self.trader.sell(security=stock,price=price,amount=amount,strategy_name=name,order_remark=name)
                                                    msg="""
                                                        策略：{},
                                                        股票：{},
                                                        操作:卖出,
                                                        价格:{},
                                                        数量:{},
                                                        时间:{}
                                                        """.format(name,stock,price,amount,datetime.now())
                                                    self.seed_emial_qq(text=msg)
                                                else:
                                                    pass
                                            elif cash_type=='百分比':
                                                trader_type,amount,price=self.trader.order_percent(stock=stock,percent=sell_value,price=price,trader_type='sell')
                                                if trader_type=='sell' and amount>=10:
                                                    if self.trader_tool=='ths':
                                                        self.trader.sell(security=stock,price=price,amount=amount)
                                                    else:
                                                        self.trader.sell(security=stock,price=price,amount=amount,strategy_name=name,order_remark=name)
                                                else:
                                                    pass
                                            else:
                                                pass
                                        else:
                                            print(stock,name,'开启了最新成本价收益要求目前成本价收益{} 小于{} 不开始第一次做T卖出'.format(zdf,min_zdf))
                                            trader_type=''
                                    else:
                                        if cash_type=='数量':
                                            amount=sell_value
                                            if self.trader_tool=='ths':
                                                self.trader.sell(security=stock,price=price,amount=sell_value)
                                            else:
                                                self.trader.sell(security=stock,price=price,amount=sell_value,strategy_name=name,order_remark=name)
                                        elif cash_type=='金额':
                                            trader_type,amount,price=self.trader.order_value(stock=stock,value=sell_value,price=price,trader_type='sell')
                                            if trader_type=='sell' and amount>=10:
                                                if self.trader_tool=='ths':
                                                    self.trader.sell(security=stock,price=price,amount=amount)
                                                else:
                                                    self.trader.sell(security=stock,price=price,amount=amount,strategy_name=name,order_remark=name)
                                            else:
                                                pass
                                        elif cash_type=='百分比':
                                            trader_type,amount,price=self.trader.order_percent(stock=stock,percent=sell_value,price=price,trader_type='sell')
                                            if trader_type=='sell' and amount>=10:
                                                if self.trader_tool=='ths':
                                                    self.trader.sell(security=stock,price=price,amount=amount)
                                                else:
                                                    self.trader.sell(security=stock,price=price,amount=amount,strategy_name=name,order_remark=name)
                                            else:
                                                pass
                                        else:
                                            pass
                                else:
                                    trader_type=''
                                if (trader_type=='buy' or trader_type=='sell') and  amount>=10:
                                    df1=pd.DataFrame()
                                    df1['证券代码']=[stock]
                                    df1["模块名称"]=[name]
                                    df1['交易时间']=[trader_date]
                                    df1['触发时间']=[now_date]
                                    df1['触发的价格']=[price]
                                    df1['资金类型']=[cash_type]
                                    if trader_type=='sell':
                                        df1['交易值']=[sell_value]
                                    else:
                                        df1['交易值']=[buy_value]
                                    df1['持有值']=[limit_value]
                                    df1['交易类型']=[trader_type]
                                    df1['交易数量']=[amount]
                                    log=pd.concat([log,df1],ignore_index=True)
                                    log.to_excel(r'自定义模块交易记录\自定义模块交易记录.xlsx')
                                    
                                else:
                                    pass
                            else:
                                print(name,'{} 不开启'.format(now_date))
                    
                    
                    except Exception as e:
                        print(e,stock,name,'有问题************')
                    
                    
            else:
                print('自定义交易持股模块没有持股')   
        else:
            print('自定义交易持股模块{} 目前不是交易时间'.format(datetime.now())) 
    def run_custom_trading_modules(self):
        '''
        自定义股票池运行自定义交易模型
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        user_models=text['自定义交易模块']
        name_list=list(user_models.keys())
        if self.check_is_trader_date_1()==True:
            now_date=datetime.now()
            trader_date=str(datetime.now())[:10]
            df=pd.read_excel(r'自定义股票池\自定义股票池.xlsx')
            log=pd.read_excel(r'自定义模块交易记录\自定义模块交易记录.xlsx')
            log=log[['证券代码','模块名称','交易时间','触发时间','触发的价格','资金类型','交易值','持有值','交易类型']]
            log['触发时间']=log['触发时间'].astype(str)
            log['证券代码']=log['证券代码'].astype(str)
            now_date=datetime.now()
            trader_date=str(datetime.now())[:10]
            #读取今天
            log=log[log['交易时间']==trader_date]
            if df.shape[0]>0:
                df['证券代码']=df['证券代码'].apply(lambda x: '0'*(6-len(str(x)))+str(x))
                for stock in df['证券代码'].tolist():
                    try:
                        for name in name_list:
                            user_set=user_models[name]
                            func=user_set['函数名称']
                            is_open=user_set['是否开启']
                            cash_type=user_set['资金模型']
                            sell_value=user_set['卖出值']
                            buy_value=user_set['买入值']
                            limit_value=user_set['持有值']
                            data_type=user_set['数据类型']
                            is_other_data=user_set['是否开启其他数据']
                            other_data_type=user_set['其他数据类型']
                            if is_open=='是':
                                spot_data=self.data.get_spot_data(stock=stock)
                                price=spot_data['最新价']
                                lof_list=text['lof基金列表']
                                stock=str(stock)
                                if stock[:6] in lof_list:
                                    price=price
                                else:
                                    price=price
                                if data_type=='历史行情':
                                    hist=self.data.get_hist_data_em(stock=stock)
                                    hist['证券代码']=stock
                                elif data_type=='高频行情':
                                    hist=self.data.get_spot_trader_data(stock=stock)
                                    hist['证券代码']=stock
                                else:
                                    data_dict = {'1分钟行情': '1',
                                                '5分钟行情': '5', 
                                                '15分钟行情': '15',
                                                '30分钟行情': '30',
                                                '60分钟行情': '60',
                                                '日线行情': 'D',
                                                '周线行情': 'W',
                                                '月线行情': 'M'}
                                    hist=self.data.get_hist_data_em(stock=stock,data_type=data_dict.get(data_type,'D'))
                                    hist['证券代码']=stock
                                if is_other_data=='是':
                                    if other_data_type=='历史行情':
                                        other_data=self.data.get_hist_data_em(stock=stock)
                                        other_data['证券代码']=stock
                                    elif other_data_type=='高频行情':
                                        other_data=self.data.get_spot_trader_data(stock=stock)
                                        other_data['证券代码']=stock
                                    else:
                                        data_dict = {'1分钟行情': '1',
                                                    '5分钟行情': '5', 
                                                    '15分钟行情': '15',
                                                    '30分钟行情': '30',
                                                    '60分钟行情': '60',
                                                    '日线行情': 'D',
                                                    '周线行情': 'W',
                                                    '月线行情': 'M'}
                                        other_data=self.data.get_hist_data_em(stock=stock,data_type=data_dict.get(data_type,'D'))
                                        other_data['证券代码']=stock
                                else:
                                    other_data=''

                                models=custom_trading_modules(stock=stock,df=hist,spot_data=spot_data,other_data=other_data)
                                func='models.{}'.format(func)
                                trader_type=eval(func)
                                if trader_type=='buy':
                                    if cash_type=='数量':
                                        #检查目标持股限制
                                        trader_type,amount,price=self.trader.order_target_volume(stock=stock,amount=limit_value,price=price)
                                    elif cash_type=='金额':
                                        trader_type,amount,price=self.trader.order_target_value(stock=stock,value=limit_value,price=price)
                                    elif cash_type=='百分比':
                                        trader_type,amount,price=self.trader.order_target_percent(stock=stock,target_percent=limit_value,price=price)
                                    else:
                                        trader_type=''
                                        amount=''
                                        price=''
                                    if trader_type=='buy':
                                        if cash_type=='数量':
                                            amount=buy_value
                                            if self.trader_tool=='ths':
                                                self.trader.buy(security=stock,price=price,amount=buy_value)
                                            else:
                                                self.trader.buy(security=stock,price=price,amount=buy_value,strategy_name=name,order_remark=name)
                                                
                                        elif cash_type=='金额':
                                            trader_type,amount,price=self.trader.order_value(stock=stock,value=buy_value,price=price,trader_type='buy')
                                            if trader_type=='buy' and amount>=10:
                                                if self.trader_tool=='ths':
                                                    self.trader.buy(security=stock,price=price,amount=amount)
                                                else:
                                                    self.trader.buy(security=stock,price=price,amount=amount,strategy_name=name,order_remark=name)
                                            else:
                                                pass
                                        elif cash_type=='百分比':
                                            trader_type,amount,price=self.trader.order_percent(stock=stock,percent=buy_value,price=price,trader_type='buy')
                                            if trader_type=='buy' and amount>=10:
                                                if self.trader_tool=='ths':
                                                    self.trader.buy(security=stock,price=price,amount=amount)
                                                else:
                                                    self.trader.buy(security=stock,price=price,amount=amount,strategy_name=name,order_remark=name)
                                            else:
                                                pass
                                        else:
                                            pass
                                elif trader_type=='sell':
                                    if cash_type=='数量':
                                        amount=sell_value
                                        if self.trader_tool=='ths':
                                            self.trader.sell(security=stock,price=price,amount=sell_value)
                                        else:
                                            self.trader.sell(security=stock,price=price,amount=sell_value,strategy_name=name,order_remark=name)
                                    elif cash_type=='金额':
                                        trader_type,amount,price=self.trader.order_value(stock=stock,value=sell_value,price=price,trader_type='sell')
                                        if trader_type=='sell' and amount>=10:
                                            if self.trader_tool=='ths':
                                                self.trader.sell(security=stock,price=price,amount=amount)
                                            else:
                                                self.trader.sell(security=stock,price=price,amount=amount,strategy_name=name,order_remark=name)
                                        else:
                                            pass
                                    elif cash_type=='百分比':
                                        trader_type,amount,price=self.trader.order_percent(stock=stock,percent=sell_value,price=price,trader_type='sell')
                                        if trader_type=='sell' and amount>=10:
                                            if self.trader_tool=='ths':
                                                self.trader.sell(security=stock,price=price,amount=amount)
                                            else:
                                                self.trader.sell(security=stock,price=price,amount=amount,strategy_name=name,order_remark=name)
                                        else:
                                            pass
                                    else:
                                        pass
                                else:
                                    trader_type=''
                                if (trader_type=='buy' or trader_type=='sell') and  amount>=10:
                                    df1=pd.DataFrame()
                                    df1['证券代码']=[stock]
                                    df1["模块名称"]=[name]
                                    df1['交易时间']=[trader_date]
                                    df1['触发时间']=[now_date]
                                    df1['触发的价格']=[price]
                                    df1['资金类型']=[cash_type]
                                    if trader_type=='sell':
                                        df1['交易值']=[sell_value]
                                    else:
                                        df1['交易值']=[buy_value]
                                    df1['持有值']=[limit_value]
                                    df1['交易类型']=[trader_type]
                                    df1['交易数量']=[amount]
                                    log=pd.concat([log,df1],ignore_index=True)
                                    log.to_excel(r'自定义模块交易记录\自定义模块交易记录.xlsx')
                                    #调整持股
                                    self.adjust_hold_data(stock=stock,trader_type=trader_type,price=price,amount=amount)
                                    #调整账户资金
                                    self.adjust_account_cash(stock=stock,trader_type=trader_type,price=price,amount=amount)
                                else:
                                    pass
                            else:
                                print(name,'{} 不开启'.format(now_date))
                    
                    except Exception as e:
                        print(e,name,'有问题************')
                    
            else:
                print('自定义交易模块没有持股')   
        else:
            print('自定义交易模块{} 目前不是交易时间'.format(datetime.now()))  
    def run_del_qmt_userdata_mini(self):
        '''
        清空qmt缓存数据
        '''
        try:
            print("清空qmt缓存数据**************")
            models=del_qmt_userdata_mini(folder_path=r'{}'.format(self.qmt_path))
            models.del_all_qmt_folder()
        except Exception as e:
            print(e,'清空qmt缓存数据有问题')
if __name__=='__main__':
    '''
    交易策略
    '''
    with open('分析配置.json','r+',encoding='utf-8') as f:
        com=f.read()
    text=json.loads(com)
    trader_tool=text['交易系统']
    exe=text['同花顺下单路径']
    tesseract_cmd=text['识别软件安装位置']
    print(tesseract_cmd)
    qq=text['发送qq']
    test=text['测试']
    open_set=text['是否开启特殊证券公司交易设置']
    qmt_path=text['qmt路径']
    qmt_account=text['qmt账户']
    qmt_account_type=text['qmt账户类型']
    slippage=text['滑点']
    data_api=text['交易数据源']
    trader=trader_strategy(trader_tool=trader_tool
    ,exe=exe,tesseract_cmd=tesseract_cmd,qq=qq,
                           open_set=open_set,qmt_path=qmt_path,qmt_account=qmt_account,
                           qmt_account_type=qmt_account_type,slippage=slippage,data_api=data_api)
    trader.connact()
    #运行就更新账户数据
    trader.save_account_data()
    
    #交易前先保存数据
    user_def_select=text['是否开启自定义函数模块']
    user_def_type=text['自定义函数运行类型']
    user_def_time=text['自定义函数模块运行时间']
    user_def_func=text['自定义函数']
    #同步手动下单数据
    tb_select=text['是否同步数据']
    tb_time=text['同步周期']
    if tb_select=='是':
        print('启动同步数据')
        schedule.every(tb_time).minutes.do(trader.save_account_data)
    else:
        print('不启动同步数据')
    if user_def_select=='是':
        print('开启自定义函数模块')
        trader.run_user_def_trader_models()
    else:
        print('不开启自定义函数模块')
    #高频模块持股
    user_trader=text['是否开启自定义实时持股交易模块']
    user_trader_time=text['自定义交易持股模块更新时间']
    if user_trader=='是':
        print('开启自定义交易持股模块************')
        schedule.every(user_trader_time).minutes.do(trader.run_custom_trading_modules_hold_stock)
    else:
        print('不开启自定义交易持股模块************')
    #循环买入
    cycle_buy_select=text['是否循环买入设置']
    if cycle_buy_select=='是':
        print('循环买入启动')
        cycle_buy_time=text['循环买入刷新时间']
        schedule.every(cycle_buy_time).minutes.do(trader.run_stock_trader_buy)
    else:
        print('不启动循环买入程序')
    #循环卖出
    cycle_sell_select=text['是否循环卖出']
    if cycle_sell_select=='是':
        print('循环卖出启动')
        cycle_sell_time=text['循环卖出刷新时间']
        schedule.every(cycle_sell_time).minutes.do(trader.run_stock_trader_sell)
    else:
        print('不启动循环卖出程序')
    #高频模块自定义股票池
    user_trader=text['是否开启自定义实时交易模块']
    user_trader_time=text['自定义交易模块更新时间']
    if user_trader=='是':
        print('开启自定义股票池交易模块************')
        schedule.every(user_trader_time).minutes.do(trader.run_custom_trading_modules)
    else:
        print('不开启自定义股票池交易模块************')
    
    del_data=text['是否清空缓存数据']
    del_data_time=text['清空缓存时间']
    if del_data=='是':
        print('开启清空缓存数据**************')
        schedule.every(del_data_time).minutes.do(trader.run_del_qmt_userdata_mini)
    else:
        print('不开启清空缓存数据**************')
    while True:
        schedule.run_pending()
        time.sleep(1)

