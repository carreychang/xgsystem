from  xg_tdx_func.xg_tdx_func import *
from datetime import datetime
class custom_hist_trading_modules:
    def __init__(self,stock='stock',
                df='',spot_data=''):
        '''
        自定义交易持股模块
        模块只要针对行情分析，高频数据交易分析
        持股模块交易在主程序里面提高计算速度
        stock 股票代码
        name 模块名称
        cash_type 资金模型=数量/金额/百分比
        value 资金值
        limit_value 持有值限制
        data_type=高频/历史
        df 数据
        历史行情数据格式
        历史行情/1分钟行情/5分钟行情/15分钟行情/30分钟行情/60分钟行情/日线行情/周线行情/月线行情
                   date   open  close   high    low   volume           成交额    振幅   涨跌幅   涨跌额   换手率
                0    2021-01-04  33.82  33.37  34.58  32.97  1027586  3.603294e+09  4.80 -0.54 -0.18  1.21
                1    2021-01-05  33.08  35.12  35.37  32.87  1072169  3.824581e+09  7.49  5.24  1.75  1.26
                2    2021-01-06  35.15  35.53  36.03  34.57  1097482  4.029568e+09  4.16  1.17  0.41  1.29
                3    2021-01-07  36.07  38.96  39.23  35.85  1401786  5.461736e+09  9.51  9.65  3.43  1.65
                4    2021-01-08  38.96  38.94  39.95  37.58  1459535  5.862015e+09  6.08 -0.05 -0.02  1.72
                ..          ...    ...    ...    ...    ...      ...           ...   ...   ...   ...   ...
                902  2024-09-23  15.84  16.24  16.31  15.83   508098  8.208300e+08  3.03  2.46  0.39  0.60
                903  2024-09-24  16.37  16.67  16.71  16.09   685346  1.129299e+09  3.82  2.65  0.43  0.81
                904  2024-09-25  16.86  16.70  17.18  16.63   719915  1.219051e+09  3.30  0.18  0.03  0.85
                905  2024-09-26  16.70  17.19  17.19  16.62   714270  1.214062e+09  3.41  2.93  0.49  0.84
                906  2024-09-27  17.49  17.82  17.93  17.33   852418  1.504914e+09  3.49  3.66  0.63  1.01
        高频数据格式
                date     价格   成交量  性质  close     实时涨跌幅       涨跌幅
            0      91500  17.19     2   4  17.19       NaN  0.000000
            1      91503  17.19   133   4  17.19  0.000000  0.000000
            2      91507  17.20   570   4  17.20  0.000582  0.058173
            3      91509  17.20   685   4  17.20  0.000000  0.058173
            4      91512  17.20   762   4  17.20  0.000000  0.058173
            ...      ...    ...   ...  ..    ...       ...       ...
            3617  145651  17.82    23  买盘  17.82  0.000000  3.664921
            3618  145654  17.81    12  卖盘  17.81 -0.000561  3.606748
            3619  145657  17.82    30  买盘  17.82  0.000561  3.664921
            3620  145700  17.82    29  买盘  17.82  0.000000  3.664921
            3621  150000  17.82  2885  卖盘  17.82  0.000000  3.664921
        spot data数据结果字典
        result['最新价']=float(text['f43'])/1000
        result['最高价']=text['f44']/1000
        result['最低价']=text['f45']/1000
        result['今开']=text['f46']/1000
        result['金额']=text['f48']
        result['外盘']=text['f49']
        result['量比']=text['f50']/100
        result['涨停价']=text['f51']/1000
        result['跌停价']=text['f52']/1000
        result['昨收']=text['f60']/1000
        result['涨跌']=text['f169']/1000
        result['内盘']=text['f161']
        result['换手率']=text['f168']/100
        result['涨跌幅']=text['f170']/100
        '''
        self.stock=stock
        self.df=df
        self.spot_data=spot_data
        self.log=pd.read_excel(r'历史自定义模块交易记录\历史自定义模块交易记录.xlsx')
        self.log=self.log[['证券代码','模块名称','交易时间','触发时间','触发的价格','资金类型','交易值','持有值','交易类型','交易数量']]
        self.log['触发时间']=self.log['触发时间'].astype(str)
        self.log['证券代码']=self.log['证券代码'].astype(str)
        self.now_date=datetime.now()
        self.trader_date=str(datetime.now())[:10]
        #读取今天
        self.log=self.log.sort_values(by='交易时间',ascending=True)
        if self.log.shape[0]>0:
            self.log['证券代码']=self.log['证券代码'].apply(lambda x: '0'*(6-len(str(x)))+str(x))
        else:
            self.log=self.log
    def conditional_single_account_balance(self,name='条件单账户止盈',x=8):
        '''
        条件单账户止盈
        '''
        stock=str(self.stock)
        hold_stock=pd.read_excel(r'持股数据\持股数据.xlsx')
        df=self.df
        close=df['close'].tolist()[-1]
        if hold_stock.shape[0]>0:
            hold_stock['证券代码']=hold_stock['证券代码'].apply(lambda x: '0'*(6-len(str(x)))+str(x))
            hold_stock=hold_stock[hold_stock['可用余额']>=10]
            if hold_stock.shape[0]>0:
                hold_stock=hold_stock[hold_stock['证券代码']==stock]
                if hold_stock.shape[0]>0:
                    cost_price=hold_stock['成本价'].tolist()[-1]
                    if self.log.shape[0]>0:
                        log=self.log[self.log['模块名称']==name]
                        log=log[log['证券代码']==stock]
                        if log.shape[0]>0:
                            pre_price=log['触发的价格'].tolist()[-1]
                            zdf=((close-pre_price)/pre_price)*100
                        else:
                            zdf=((close-cost_price)/cost_price)*100
                    else:
                        zdf=((close-cost_price)/cost_price)*100
                    if zdf>=x:
                        print('{} 模块{} 卖出{} 账户{}大于目标涨跌幅{} '.format(self.now_date,name,stock,zdf,x))
                        return 'sell'
                    else:
                        print('{} 模块{} 不符合卖出{} 账户{}小于目标涨跌幅{} '.format(self.now_date,name,stock,zdf,x))
                        return ''
                else:
                    print('{} 模块{} 不符合卖出{} 没有持股 '.format(self.now_date,name,stock))
                    return ''
            else:
                print('{} 模块{} 不符合卖出{} 没有持股 '.format(self.now_date,name,stock))
                return ''
        else:
            print('{} 模块{} 不符合卖出{} 没有持股 '.format(self.now_date,name,stock))
            return ''
    def conditional_single_account_stop_loss(self,name='条件单账户止损',x=-3):
        '''
        条件单账户止损
        '''
        stock=str(self.stock)
        hold_stock=pd.read_excel(r'持股数据\持股数据.xlsx')
        df=self.df
        close=df['close'].tolist()[-1]
        if hold_stock.shape[0]>0:
            hold_stock['证券代码']=hold_stock['证券代码'].apply(lambda x: '0'*(6-len(str(x)))+str(x))
            hold_stock=hold_stock[hold_stock['可用余额']>=10]
            if hold_stock.shape[0]>0:
                hold_stock=hold_stock[hold_stock['证券代码']==stock]
                if hold_stock.shape[0]>0:
                    cost_price=hold_stock['成本价'].tolist()[-1]
                    if self.log.shape[0]>0:
                        log=self.log[self.log['模块名称']==name]
                        log=log[log['证券代码']==stock]
                        if log.shape[0]>0:
                            pre_price=log['触发的价格'].tolist()[-1]
                            zdf=((close-pre_price)/pre_price)*100
                        else:
                            zdf=((close-cost_price)/cost_price)*100
                    else:
                        zdf=((close-cost_price)/cost_price)*100
                    if zdf<=x:
                        print('{} 模块{} 卖出{} 账户{}小于目标涨跌幅{} '.format(self.now_date,name,stock,zdf,x))
                        return 'sell'
                    else:
                        print('{} 模块{} 不符合卖出{} 账户{}大于目标涨跌幅{} '.format(self.now_date,name,stock,zdf,x))
                        return ''
                else:
                    print('{} 模块{} 不符合卖出{} 没有持股 '.format(self.now_date,name,stock))
                    return ''
            else:
                print('{} 模块{} 不符合卖出{} 没有持股 '.format(self.now_date,name,stock))
                return ''
        else:
            print('{} 模块{} 不符合卖出{} 没有持股 '.format(self.now_date,name,stock))
            return ''