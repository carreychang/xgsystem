from  xg_tdx_func.xg_tdx_func import *
from tdx_strategy_models.small_fruit_band_trading_hist_trader import small_fruit_band_trading_hist_trader
from tdx_strategy_models.small_fruit_band_trading import small_fruit_band_trading
from tdx_strategy_models.six_pulse_excalibur_hist import six_pulse_excalibur_hist
from tdx_strategy_models.small_fruit_high_frequency_measurement_line import small_fruit_high_frequency_measurement_line
from datetime import datetime
class custom_trading_modules:
    def __init__(self,stock='stock',
                df='',spot_data='',other_data=''):
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
        self.other_data=other_data
        self.log=pd.read_excel(r'自定义模块交易记录\自定义模块交易记录.xlsx')
        self.log=self.log[['证券代码','模块名称','交易时间','触发时间','触发的价格','资金类型','交易值','持有值','交易类型','交易数量']]
        self.log['触发时间']=self.log['触发时间'].astype(str)
        self.log['证券代码']=self.log['证券代码'].astype(str)
        self.now_date=datetime.now()
        self.trader_date=str(datetime.now())[:10]
        #读取今天
        self.log=self.log[self.log['交易时间']==self.trader_date]
        print('自定义模块交易记录******************')
        print(self.log)
        if self.log.shape[0]>0:
            self.log['证券代码']=self.log['证券代码'].apply(lambda x: '0'*(6-len(str(x)))+str(x))
        else:
            self.log= self.log

    def calculate_time_diff(self,time_str1, time_str2, time_format="%Y/%m/%d %H:%M:%S", output="seconds"):
        """
        计算两个时间字符串之间的时间差
        
        Args:
            time_str1 (str): 第一个时间字符串，例如 "2025/3/31 13:28:18"
            time_str2 (str): 第二个时间字符串，例如 "2025/3/31 13:29:18"
            time_format (str): 时间格式，默认 "%Y/%m/%d %H:%M:%S"
            output (str): 返回格式，可选：
                - "timedelta"：返回 datetime.timedelta 对象
                - "seconds"：返回总秒数（默认）
                - "minutes"：返回总分钟数
                - "hours"：返回总小时数
                - "days"：返回总天数
                - "auto"：自动返回易读的字符串（如 "1分钟"）
        
        Returns:
            timedelta / float / str: 根据 `output` 返回时间差
        """
        time1 = datetime.strptime(time_str1, time_format)
        time2 = datetime.strptime(time_str2, time_format)
        delta = time2 - time1  # 计算时间差
        
        if output == "timedelta":
            return delta
        elif output == "seconds":
            return delta.total_seconds()
        elif output == "minutes":
            return delta.total_seconds() / 60
        elif output == "hours":
            return delta.total_seconds() / 3600
        elif output == "days":
            return delta.total_seconds() / 86400
        elif output == "auto":
            seconds = delta.total_seconds()
            if seconds < 60:
                return f"{int(seconds)}秒"
            elif seconds < 3600:
                return f"{int(seconds // 60)}分钟"
            elif seconds < 86400:
                return f"{int(seconds // 3600)}小时"
            else:
                return f"{int(seconds // 86400)}天"
        else:
            raise ValueError("Invalid output format. Choose: 'timedelta', 'seconds', 'minutes', 'hours', 'days', or 'auto'.")
    def daily_dynamic_stop_profit(self,name='当日止盈',x1=5):
        '''
        当日止盈
        数据类型行情
        '''
        stock=str(self.stock)
        df=self.df
        close=df['close'].tolist()[-1]
        if self.log.shape[0]>0:
            log=self.log[self.log['模块名称']==name]
            log=log[log['证券代码']==stock]
            if log.shape[0]>0:
                pre_price=log['触发的价格'].tolist()[-1]
                zdf=((close-pre_price)/pre_price)*100
            else:
                zdf=df['涨跌幅'].tolist()[-1]
        else:
            zdf=df['涨跌幅'].tolist()[-1]
        if zdf>=x1:
            print('{} 模块{} 卖出{} 涨跌幅{}大于止盈涨跌幅{} '.format(self.now_date,name,stock,zdf,x1))
            return 'sell'
        else:
            print('{} 模块{} 不符合模型{} 涨跌幅{} '.format(self.now_date,name,stock,zdf))
            return ''
    def daily_dynamic_stop_loss(self,name='当日止盈',x2=-3):
        '''
        当日止损
        数据类型行情
        '''
        stock=str(self.stock)
        df=self.df
        close=df['close'].tolist()[-1]
        if self.log.shape[0]>0:
            log=self.log[self.log['模块名称']==name]
            log=log[log['证券代码']==stock]
            if log.shape[0]>0:
                pre_price=log['触发的价格'].tolist()[-1]
                zdf=((close-pre_price)/pre_price)*100
            else:
                zdf=df['涨跌幅'].tolist()[-1]
        else:
            zdf=df['涨跌幅'].tolist()[-1]
        if zdf<=x2:
            print('{} 模块{} 卖出{} 涨跌幅{}小于止盈涨跌幅{} '.format(self.now_date,name,stock,zdf,x2))
            return 'sell'
        else:
            print('{} 模块{} 不符合模型{} 涨跌幅{} '.format(self.now_date,name,stock,zdf))
            return ''
    def advance_buy_condition_order(self,name='条件单上涨买入',x=2):
        '''
        条件单上涨买入
        '''
        stock=str(self.stock)
        df=self.df
        close=df['close'].tolist()[-1]
        if self.log.shape[0]>0:
            log=self.log[self.log['模块名称']==name]
            log=log[log['证券代码']==stock]
            if log.shape[0]>0:
                pre_price=log['触发的价格'].tolist()[-1]
                zdf=((close-pre_price)/pre_price)*100
            else:
                zdf=df['涨跌幅'].tolist()[-1]
        else:
            zdf=df['涨跌幅'].tolist()[-1]
        if zdf>=x:
            print('{} 模块{} 买入{} 涨跌幅{}大于买入涨跌幅{} '.format(self.now_date,name,stock,zdf,x))
            return 'buy'
        else:
            print('{} 不符合模块{} {} 目前涨跌幅{} 目标涨跌幅{} '.format(self.now_date,name,stock,zdf,x))
            return ''
    def advance_sell_condition_order(self,name='条件单上涨卖出',x=3):
        '''
        条件单上涨卖出
        '''
        stock=str(self.stock)
        df=self.df
        close=df['close'].tolist()[-1]
        if self.log.shape[0]>0:
            log=self.log[self.log['模块名称']==name]
            log=log[log['证券代码']==stock]
            if log.shape[0]>0:
                pre_price=log['触发的价格'].tolist()[-1]
                zdf=((close-pre_price)/pre_price)*100
            else:
                zdf=df['涨跌幅'].tolist()[-1]
        else:
            zdf=df['涨跌幅'].tolist()[-1]
        if zdf>=x:
            print('{} 模块{} 卖出{} 涨跌幅{}大于买入涨跌幅{} '.format(self.now_date,name,stock,zdf,x))
            return 'sell'
        else:
            print('{} 不符合模块{} {} 目前涨跌幅{} 目标涨跌幅{} '.format(self.now_date,name,stock,zdf,x))
            return ''
    def condition_sell_down(self,name='条件单下跌卖出',x=-3):
        '''
        条件单下跌卖出
        '''
        stock=str(self.stock)
        df=self.df
        close=df['close'].tolist()[-1]
        if self.log.shape[0]>0:
            log=self.log[self.log['模块名称']==name]
            log=log[log['证券代码']==stock]
            if log.shape[0]>0:
                pre_price=log['触发的价格'].tolist()[-1]
                zdf=((close-pre_price)/pre_price)*100
            else:
                zdf=df['涨跌幅'].tolist()[-1]
        else:
            zdf=df['涨跌幅'].tolist()[-1]
        if  zdf<=x:
            print('{} 模块{} 卖出{} 涨跌幅{}小于卖出涨跌幅{} '.format(self.now_date,name,stock,zdf,x))
            return 'sell'
        else:
            print('{} 不符合模块{} {} 目前涨跌幅{} 目标涨跌幅{} '.format(self.now_date,name,stock,zdf,x))
            return ''
    def condition_buy_down(self,name='条件单下跌买入',x=-3):
        '''
        条件单下跌买入
        '''
        stock=str(self.stock)
        df=self.df
        close=df['close'].tolist()[-1]
        if self.log.shape[0]>0:
            log=self.log[self.log['模块名称']==name]
            log=log[log['证券代码']==stock]
            if log.shape[0]>0:
                pre_price=log['触发的价格'].tolist()[-1]
                zdf=((close-pre_price)/pre_price)*100
            else:
                zdf=df['涨跌幅'].tolist()[-1]
        else:
            zdf=df['涨跌幅'].tolist()[-1]
        if  zdf<=x:
            print('{} 模块{} 买入{} 涨跌幅{}小于卖出涨跌幅{} '.format(self.now_date,name,stock,zdf,x))
            return 'buy'
        else:
            print('{} 不符合模块{} {} 目前涨跌幅{} 目标涨跌幅{} '.format(self.now_date,name,stock,zdf,x))
            return ''
    def get_mi_pulse_trader_sell(self,name='分钟脉冲卖出',n=10,x=2):
        '''
        分钟脉冲卖出
        '''
        stock=str(self.stock)
        df=self.df
        close_list=df['价格'].tolist()
        price=close_list[-1]
        close_list=close_list[-n*20:]
        if self.log.shape[0]>0:
            log=self.log[self.log['模块名称']==name]
            log=log[log['证券代码']==stock]
            if log.shape[0]>0:
                pre_price=log['触发的价格'].tolist()[-1]
                zdf=((price-pre_price)/pre_price)*100
            else:
                zdf=((price-close_list[1])/close_list[1])*100
        else:
            zdf=((price-close_list[1])/close_list[1])*100
        if zdf>=x:
            print('{} 模块{} 卖出{} 涨跌幅{}大于目标涨跌幅{} '.format(self.now_date,name,stock,zdf,x))
            return 'sell'
        else:
            print('{} 模块{} 不符合交易{} 涨跌幅{} 涨跌幅{} '.format(self.now_date,name,stock,zdf,x))
            return ''
    def get_mi_pulse_trader_buy(self,name='分钟脉冲出买入',n=10,x=-2):
        '''
        分钟脉冲出买入
        '''
        stock=str(self.stock)
        df=self.df
        close_list=df['价格'].tolist()
        price=close_list[-1]
        close_list=close_list[-n*20:]
        if self.log.shape[0]>0:
            log=self.log[self.log['模块名称']==name]
            log=log[log['证券代码']==stock]
            if log.shape[0]>0:
                pre_price=log['触发的价格'].tolist()[-1]
                zdf=((price-pre_price)/pre_price)*100
            else:
                zdf=((price-close_list[1])/close_list[1])*100
        else:
            zdf=((price-close_list[1])/close_list[1])*100
        
        if zdf<=x:
            print('{} 模块{} 卖出{} 涨跌幅{}小于目标涨跌幅{} '.format(self.now_date,name,stock,zdf,x))
            return 'buy'
        else:
            print('{} 模块{} 不符合交易{} 涨跌幅{} 涨跌幅{} '.format(self.now_date,name,stock,zdf,x))
            return ''
    def condition_single_high_fall(self,name='条件单冲高回落',x1=3,x2=1):
        '''
        条件单冲高回落
        x1涨跌幅
        x2回落涨跌幅
        '''
        stock=str(self.stock)
        df=self.df
        df['涨跌幅']=pd.to_numeric(df['涨跌幅'])
        df['价格']=pd.to_numeric(df['价格'])
        cumsum_zdf_list=df['涨跌幅'].tolist()[2:]
        close_list=df['价格'].tolist()
        price=close_list[-1]
        zdf=cumsum_zdf_list[-1]
        if self.log.shape[0]>0:
            log=self.log[self.log['模块名称']==name]
            log=log[log['证券代码']==stock]
            if log.shape[0]>0:
                pre_price=log['触发的价格'].tolist()[-1]
                log_zdf=((price-pre_price)/pre_price)*100
                max_zdf=max(cumsum_zdf_list)
                fall_zdf=max_zdf-zdf
            else:
                log_zdf=zdf
                max_zdf=max(cumsum_zdf_list)
                fall_zdf=max_zdf-zdf
        else:
            log_zdf=zdf
            max_zdf=max(cumsum_zdf_list)
            fall_zdf=max_zdf-zdf
        if log_zdf>=x1 and fall_zdf>=x2:
            print('{} 模块{} 卖出{} 目前涨跌幅{}大于目标涨跌幅{} 回落涨跌幅{}'.format(self.now_date,name,stock,log_zdf,x1,fall_zdf))
            return 'sell'
        else:
            print('{} 模块{} 不符合卖出{} 目前涨跌幅{} 目标涨跌幅{} 回落涨跌幅{}'.format(self.now_date,name,stock,log_zdf,x1,fall_zdf))
            return ''
    def sell_on_condition_of_single_bounce(self,name='条件单反弹卖出',x1=-3,x2=1):
        '''
        条件单反弹卖出
        x1下跌涨跌幅
        x2反弹涨跌幅
        '''
        stock=str(self.stock)
        df=self.df
        df['涨跌幅']=pd.to_numeric(df['涨跌幅'])
        df['价格']=pd.to_numeric(df['价格'])
        close_list=df['价格'].tolist()
        cumsum_zdf_list=df['涨跌幅'].tolist()[2:]
        price=close_list[-1]
        zdf=cumsum_zdf_list[-1]
        if self.log.shape[0]>0:
            log=self.log[self.log['模块名称']==name]
            log=log[log['证券代码']==stock]
            if log.shape[0]>0:
                pre_price=log['触发的价格'].tolist()[-1]
                log_zdf=((price-pre_price)/pre_price)*100
                min_zdf=min(cumsum_zdf_list)
                bounce_zdf=zdf-min_zdf
            else:
                log_df=zdf
                min_zdf=min(cumsum_zdf_list)
                bounce_zdf=zdf-min_zdf
        else:
            log_df=zdf
            min_zdf=min(cumsum_zdf_list)
            bounce_zdf=zdf-min_zdf
        if zdf<=x1 and bounce_zdf>=x2:
            print('{} 模块{} 卖出{} 目前涨跌幅{}小于标涨跌幅{} 反弹涨跌幅{}'.format(self.now_date,name,stock,log_zdf,x1,bounce_zdf))
            return 'sell'
        else:
            print('{} 模块{} 不符合卖出{} 目前涨跌幅{} 目标涨跌幅{} 反弹涨跌幅{}'.format(self.now_date,name,stock,log_zdf,x1,bounce_zdf))
            return ''
    def conditional_single_time_sharing_grid(self,name='条件单分时网格',x1=0.3,x2=-0.3):
        '''
        条件单分时网格
        stock_type=自定义/持股
        '''
        stock=str(self.stock)
        df=self.df
        if False:
            pass
        else:
            df['价格']=pd.to_numeric(df['价格'])
            close_list=df['价格'].tolist()
            base_price=close_list[0]
            price=close_list[-1]
            if self.log.shape[0]>0:
                self.log['证券代码']=self.log['证券代码'].astype(str)
                log=self.log[self.log['模块名称']==name]
                log=log[log['证券代码']==stock]
                if log.shape[0]>0:
                    pre_price=log['触发的价格'].tolist()[-1]
                    zdf=((price-pre_price)/pre_price)*100
                else:
                    
                    zdf=((price-base_price)/base_price)*100
            else:
        
                zdf=((price-base_price)/base_price)*100
            if zdf>=x1:
                print('{} 模块{} 卖出{}  目前涨跌幅{} 大于目前标涨跌幅{} '.format(self.now_date,name,stock,zdf,x1))
                return 'sell'
            elif zdf<=x2:
                print('{} 模块{} 买入{}  目前涨跌幅{} 小于目前标涨跌幅{} '.format(self.now_date,name,stock,zdf,x1))
                return 'buy'
            else:
                print('{} 模块{} 不符合交易{}  目前涨跌幅{} 目前标涨跌幅{} '.format(self.now_date,name,stock,zdf,x1))
                return ''
    def condition_is_15_minutes_gold_fork_dead_fork(self,name='条件单15分钟金叉死叉',x1=5,x2=10):
        '''
        条件单15分钟金叉死叉
        x1短均线
        x2长均线
        '''
        stock=str(self.stock)
        df=self.df
        ma_x1=MA(S=df['close'],N=x1)
        x1_value=ma_x1.tolist()[-1]
        ma_x2=MA(S=df['close'],N=x2)
        x2_value=ma_x2.tolist()[-1]
        gold_fork=CROSS(S1=ma_x1,S2=ma_x2)
        dead_fork=CROSS(S1=ma_x2,S2=ma_x1)
        gold=gold_fork.tolist()[-1]
        dead=dead_fork.tolist()[-1]
        if gold==True:
            print('{} 模块{} 买入{} 金叉 x1值{} x2值{}'.format(self.now_date,name,stock,x1_value,x2_value))
            return 'buy'
        elif dead==True:
            print('{} 模块{} 卖出{} 死叉 x1值{} x2值{}'.format(self.now_date,name,stock,x1_value,x2_value))
            return 'sell'
        else:
            print('{} 模块{} {} 不符合模型 x1值{} x2值{}'.format(self.now_date,name,stock,x1_value,x2_value))
            return ''
    def small_fruit_band_trading_hist_trader(self,name='小果高频T0波段交易',is_open_trand='是',test='是',test_stats='买'):
        '''
        小果高频波段交易
        '''
        stock=str(self.stock)
        if is_open_trand=='是':
            print('{}模块 开启趋势模型'.format(name))
            hist=self.other_data
            trand_models=small_fruit_band_trading(df=hist)
            trand_models=trand_models.small_fruit_band_trading()
            trand=trand_models['stats'].tolist()[-1]
        else:
            print('{}模块 不开启趋势模型'.format(name))
            trand='buy'
        if trand=='buy':
            log=pd.read_excel(r'自定义高频交易记录\自定义高频交易记录.xlsx')
            try:
                log['Unnamed: 0']
            except:
                pass
            if log.shape[0]>0:
                log=log[['时间','股票','交易类型','交易价格','id']]
                id_list=log['id'].tolist()
            else:
                id_list=[]
            stock=str(self.stock)
            df=self.df
            models=small_fruit_band_trading_hist_trader(df=df)
            models=models.small_fruit_band_trading_hist_trader()
            models['证券代码']=stock
            models['id']=models['证券代码']+models['date']+models['stats']
            stats_id=models['id'].tolist()[-1]
            if stats_id not in id_list:
                price=models['close'].tolist()[-1]
                stats=models['stats'].tolist()[-1]
                id=models['id'].tolist()[-1]
                date=models['date'].tolist()[-1]
                if test=='是':
                    print('{} 开启趋势模式实盘记得关闭****************'.format(name))
                    stats=test_stats
                else:
                    stats=stats
                if  stats=='买':
                    df=pd.DataFrame()
                    df['时间']=[date]
                    df['时间']=df['时间'].astype(str)
                    df['股票']=[stock]
                    df['交易类型']=['买']
                    df['交易价格']=[price]
                    df['id']=[id]
                    log=pd.concat([log,df],ignore_index=True)
                    log.to_excel(r'自定义高频交易记录\自定义高频交易记录.xlsx')
                    print('{} 模块{} {} 符合买入'.format(self.now_date,name,stock))
                    return 'buy'
                elif stats=='卖':
                    df=pd.DataFrame()
                    df['时间']=[date]
                    df['时间']=df['时间'].astype(str)
                    df['股票']=[stock]
                    df['交易类型']=['买']
                    df['交易价格']=[price]
                    df['id']=[id]
                    log=pd.concat([log,df],ignore_index=True)
                    log.to_excel(r'自定义高频交易记录\自定义高频交易记录.xlsx')
                    print('{} 模块{} {} 符合卖出'.format(self.now_date,name,stock))
                    return 'sell'
                else:
                    print('{} 模块{} {} 不符合交易模型继续等待'.format(self.now_date,name,stock))
                    return ''
            else:
                print('{} 模块{} {} 在相同时间内已经交易'.format(self.now_date,name,stock))
                return ''
        else:
            print('{} 模块{} {} 不符合趋势模型'.format(self.now_date,name,stock))
            return ''
    def small_fruit_high_frequency_measurement_line(self,name='小果高频量化线'):
        '''
        小果高频量化线
        '''
        log=pd.read_excel(r'自定义高频交易记录\自定义高频交易记录.xlsx')
        try:
            log['Unnamed: 0']
        except:
            pass
        if log.shape[0]>0:
            log=log[['时间','股票','交易类型','交易价格','id']]
            id_list=log['id'].tolist()
        else:
            id_list=[]
        stock=str(self.stock)
        df=self.df
        models=small_fruit_high_frequency_measurement_line(df=df)
        models=models.small_fruit_high_frequency_measurement_line()
        models['证券代码']=stock
        models['id']=models['证券代码']+models['date']+models['stats']
        stats_id=models['id'].tolist()[-1]
        if stats_id not in id_list:
            price=models['close'].tolist()[-1]
            stats=models['stats'].tolist()[-1]
            id=models['id'].tolist()[-1]
            date=models['date'].tolist()[-1]
            if  stats=='买':
                df=pd.DataFrame()
                df['时间']=[date]
                df['时间']=df['时间'].astype(str)
                df['股票']=[stock]
                df['交易类型']=['买']
                df['交易价格']=[price]
                df['id']=[id]
                log=pd.concat([log,df],ignore_index=True)
                log.to_excel(r'自定义高频交易记录\自定义高频交易记录.xlsx')
                print('{} 模块{} {} 符合买入'.format(self.now_date,name,stock))
                return 'buy'
            elif stats=='卖':
                df=pd.DataFrame()
                df['时间']=[date]
                df['时间']=df['时间'].astype(str)
                df['股票']=[stock]
                df['交易类型']=['买']
                df['交易价格']=[price]
                df['id']=[id]
                log=pd.concat([log,df],ignore_index=True)
                log.to_excel(r'自定义高频交易记录\自定义高频交易记录.xlsx')
                print('{} 模块{} {} 符合卖出'.format(self.now_date,name,stock))
                return 'sell'
            else:
                print('{} 模块{} {} 不符合交易模型继续等待'.format(self.now_date,name,stock))
                return ''
        else:
            print('{} 模块{} {} 在相同时间内已经交易'.format(self.now_date,name,stock))
            return ''
    def six_pulse_excalibur_trader(self,name='小果六脉神剑T0交易',buy_amount=5,sell_amount=4):
        '''
        六脉神剑高频T0算法
        '''
        log=pd.read_excel(r'自定义高频交易记录\自定义高频交易记录.xlsx')
        try:
            log['Unnamed: 0']
        except:
            pass
        if log.shape[0]>0:
            log=log[['时间','股票','交易类型','交易价格','id']]
            id_list=log['id'].tolist()
        else:
            id_list=[]
        stock=str(self.stock)
        df=self.df
        models=six_pulse_excalibur_hist(df=df)
        models=models.six_pulse_excalibur_hist()
        models['证券代码']=stock
        models['买']=IF(models['signal']>=buy_amount,'买',None)
        models['卖']=IF(models['signal']<=sell_amount,'卖',None)
        stats_list=[]
        for buy,sell in zip(models['买'],models['卖']):
            if buy !=None:
                stats_list.append(buy)
            elif sell !=None:
                stats_list.append(sell)
            else:
                stats_list.append(None)
        
        models['stats']=stats_list
        models['id']=models['证券代码']+models['date']+models['stats']
        stats_id=models['id'].tolist()[-1]
        signal=models['signal'].tolist()[-1]
        if stats_id not in id_list:
            price=models['close'].tolist()[-1]
            stats=models['stats'].tolist()[-1]
            id=models['id'].tolist()[-1]
            date=models['date'].tolist()[-1]
            
            if  stats=='买':
                df=pd.DataFrame()
                df['时间']=[date]
                df['时间']=df['时间'].astype(str)
                df['股票']=[stock]
                df['交易类型']=['买']
                df['交易价格']=[price]
                df['id']=[id]
                log=pd.concat([log,df],ignore_index=True)
                log.to_excel(r'自定义高频交易记录\自定义高频交易记录.xlsx')
                print('{} 模块{} {} 符合买入 目前信号{}大于买入信号{}'.format(self.now_date,name,stock,signal,buy_amount))
                return 'buy'
            elif stats=='卖':
                df=pd.DataFrame()
                df['时间']=[date]
                df['时间']=df['时间'].astype(str)
                df['股票']=[stock]
                df['交易类型']=['买']
                df['交易价格']=[price]
                df['id']=[id]
                log=pd.concat([log,df],ignore_index=True)
                log.to_excel(r'自定义高频交易记录\自定义高频交易记录.xlsx')
                print('{} 模块{} {} 符合卖出目前信号{} 小于卖出信号{}'.format(self.now_date,name,stock,signal,sell_amount))
                return 'sell'
            else:
                print('{} 模块{} {} 不符合交易模型继续等待目前信号{}'.format(self.now_date,name,stock,signal))
                return ''
        else:
            print('{} 模块{} {} 在相同时间内已经交易目前信号{}'.format(self.now_date,name,stock,signal))
            return ''
    def down_cost_price_sell(self,name='跌破成本线止损',x=-0.5):
        '''
        跌破成本线止损
        '''
        hold_stock=pd.read_excel(r'持股数据\持股数据.xlsx')
        if hold_stock.shape[0]>0:
            hold_stock['证券代码']=hold_stock['证券代码'].apply(lambda x: '0'*(6-len(str(x)))+str(x))
            hold_stock_list=hold_stock['证券代码'].tolist()
        else:
            hold_stock_list=[]
        stock=str(self.stock)
        df=self.df
        close=df['价格'].tolist()[-1]
        if stock in hold_stock_list:
            hold_stock=hold_stock[hold_stock['证券代码']==stock]
            base_price=hold_stock['成本价'].tolist()[-1]
            if self.log.shape[0]>0:
                log=self.log[self.log['模块名称']==name]
                log=log[log['证券代码']==stock]
                if log.shape[0]>0:
                    pre_price=log['触发的价格'].tolist()[-1]
                    zdf=((close-pre_price)/pre_price)*100
                else:
                    zdf=((close-base_price)/base_price)*100
            else:
                zdf=((close-base_price)/base_price)*100
            if zdf<=x:
                print('{} 模块{} 卖出{} 涨跌幅{} 现在价格{}小于成本价{}'.format(self.now_date,name,stock,zdf,close,base_price))
                return 'sell'
            else:
                print('{} 模块{} 不符合模型{} 涨跌幅{}  现在价格{}大于成本价{}'.format(self.now_date,name,stock,zdf,close,base_price))
                return ''
        else:
            print('{} 模块{} 不符合模型{} 没有持股'.format(self.now_date,name,stock))
    def surplus_on_account(self,name='账户止盈注意成本价是变动',x=5):
        ''''
        账户止盈注意成本价是变动
        '''
        hold_stock=pd.read_excel(r'持股数据\持股数据.xlsx')
        if hold_stock.shape[0]>0:
            hold_stock['证券代码']=hold_stock['证券代码'].apply(lambda x: '0'*(6-len(str(x)))+str(x))
            hold_stock_list=hold_stock['证券代码'].tolist()
        else:
            hold_stock_list=[]
        stock=str(self.stock)
        df=self.df
        close=df['价格'].tolist()[-1]
        if stock in hold_stock_list:
            hold_stock=hold_stock[hold_stock['证券代码']==stock]
            base_price=hold_stock['成本价'].tolist()[-1]
            if self.log.shape[0]>0:
                log=self.log[self.log['模块名称']==name]
                log=log[log['证券代码']==stock]
                if log.shape[0]>0:
                    pre_price=log['触发的价格'].tolist()[-1]
                    zdf=((close-pre_price)/pre_price)*100
                else:
                    zdf=((close-base_price)/base_price)*100
            else:
                zdf=((close-base_price)/base_price)*100
            if zdf>=x:
                print('{} 模块{} 卖出{} 涨跌幅{} 现在价格{}大于成本价{} 涨跌幅{}'.format(self.now_date,name,stock,zdf,close,base_price,zdf))
                return 'sell'
            else:
                print('{} 模块{} 不符合模型{} 涨跌幅{}  现在价格{}小于成本价{} 涨跌幅{}'.format(self.now_date,name,stock,zdf,close,base_price,zdf))
                return ''
        else:
            print('{} 模块{} 不符合模型{} 没有持股'.format(self.now_date,name,stock))
    def down_mean_line_sell(self,name='跌破N日均线卖出',n=3):
        '''
        跌破N日均线卖出
        '''
        stock=str(self.stock)
        df=self.df
        df['line']=df['close'].rolling(n).mean()
        line=df['line'].tolist()[-1]
        close=df['close'].tolist()[-1]
        if close<=line:
            print('{} 模块{} 卖出{} 现在价格{} 小于{}日均线{}'.format(self.now_date,name,stock,close,n,line))
            return 'sell'
        else:
            print('{} 模块{} 不卖出{} 现在价格{} 大于{}日均线{}'.format(self.now_date,name,stock,close,n,line))
            return ''
    def down_mean_line_sell_more(self,name='跌破N日均线分批卖出',n=3,x=-0.5):
        '''
        跌破N日均线分批卖出
        '''
        stock=str(self.stock)
        df=self.df
        df['价格']=pd.to_numeric(df['close'])
        close_list=df['价格'].tolist()
        df['line']=df['价格'].rolling(n).mean()
        base_price=df['line'].tolist()[-1]
        price=close_list[-1]
        if self.log.shape[0]>0:
            self.log['证券代码']=self.log['证券代码'].astype(str)
            log=self.log[self.log['模块名称']==name]
            log=log[log['证券代码']==stock]
            if log.shape[0]>0:
                pre_price=log['触发的价格'].tolist()[-1]
                zdf=((price-pre_price)/pre_price)*100
            else:
                zdf=((price-base_price)/base_price)*100
        else:
            zdf=((price-base_price)/base_price)*100
        if zdf<=x:
            print('{} 模块{} 卖出{} 现在价格{} 小于{}日均线相对涨跌幅{}小于目标涨跌幅{}'.format(self.now_date,name,stock,price,n,zdf,x))
            return 'sell'
        else:
            print('{} 模块{} 不卖出{} 现在价格{} 小于{}日均线相对涨跌幅{}小于目标涨跌幅{}'.format(self.now_date,name,stock,price,n,zdf,x))
            return ''
    def sell_off_from_the_ma(self,name='偏离均线卖出',n=5,x=2):
        '''
        偏离均线卖出
        '''
        stock=str(self.stock)
        df=self.df
        df['line']=df['close'].rolling(n).mean()
        price=df['close'].tolist()[-1]
        base_price=df['line'].tolist()[-1]
        if self.log.shape[0]>0:
            self.log['证券代码']=self.log['证券代码'].astype(str)
            log=self.log[self.log['模块名称']==name]
            log=log[log['证券代码']==stock]
            if log.shape[0]>0:
                pre_price=log['触发的价格'].tolist()[-1]
                zdf=((price-pre_price)/pre_price)*100
            else:
                zdf=((price-base_price)/base_price)*100
        else:
            zdf=((price-base_price)/base_price)*100
        if zdf>=x:
            print('{} 模块{} 卖出{} 现在价格{} 大于{}日均线相对涨跌幅{}大于目标涨跌幅{}'.format(self.now_date,name,stock,price,n,zdf,x))
            return 'sell'
        else:
            print('{} 模块{} 不卖出{} 现在价格{} 小于{}日均线相对涨跌幅{}小于目标涨跌幅{}'.format(self.now_date,name,stock,price,n,zdf,x))
            return ''
    def sell_off_from_the_spot_mean_line(self,name='偏离分时均线卖出',start_date=93000,x=1):
        '''
        偏离分时均线卖出
        高频行情
        '''
        stock=str(self.stock)
        df=self.df
        df['价格']=pd.to_numeric(df['价格'])
        df['成交量']=pd.to_numeric(df['成交量'])
        df['分时均线'] = (df['价格'] * df['成交量']).cumsum() / df['成交量'].cumsum()
        df['时间']=pd.to_numeric(df['时间'])
        last_pirce=df['价格'].tolist()[-1]
        mean_price=df['分时均线'].tolist()[-1]
        date=df['时间'].tolist()[-1]
        if date>=start_date:
            zdf=((last_pirce-mean_price)/mean_price)*100
            if zdf>=x:
                print('{} 模块{} 卖出{} 现在价格{} 分时价格{} 涨跌幅{} 大于目标涨跌幅{}'.format(self.now_date,name,stock,last_pirce,mean_price,zdf,x))
                return 'sell'
            else:
                print('{} 模块{} 不卖出{} 现在价格{} 分时价格{} 涨跌幅{} 小于目标涨跌幅{}'.format(self.now_date,name,stock,last_pirce,mean_price,zdf,x))
                return ''
        else:
            print('{} 模块{} 不卖出{} 目前时间{} 小于开始时间{}'.format(self.now_date,name,stock,date,start_date))
            return ''
    def dynamic_deviation_from_the_time_sharing_average_sell(self,name='动态偏离分时均线卖出',start_date=93000,x=1,add_zdf=0.5):
        '''
        动态偏离分时均线卖出
        不断抬升触发价格add_zdf
        '''
        stock=str(self.stock)
        df=self.df
        df['价格']=pd.to_numeric(df['价格'])
        df['成交量']=pd.to_numeric(df['成交量'])
        df['分时均线'] = (df['价格'] * df['成交量']).cumsum() / df['成交量'].cumsum()
        df['时间']=pd.to_numeric(df['时间'])
        last_pirce=df['价格'].tolist()[-1]
        mean_price=df['分时均线'].tolist()[-1]
        date=df['时间'].tolist()[-1]
        if date>=start_date:
            if self.log.shape[0]>0:
                self.log['证券代码']=self.log['证券代码'].astype(str)
                log=self.log[self.log['模块名称']==name]
                log=log[log['证券代码']==stock]
                n=log.shape[0]
                zdf=((last_pirce-mean_price)/mean_price)*100-n*add_zdf
            else:
                zdf=((last_pirce-mean_price)/mean_price)*100
                n=0
            if zdf>=x:
                print('{} 模块{} 卖出{} 现在价格{} 分时价格{} 涨跌幅{} 大于目标涨跌幅{}'.format(self.now_date,name,stock,last_pirce,mean_price,zdf,x))
                return 'sell'
            else:
                print('{} 模块{} 不卖出{} 现在价格{} 分时价格{} 涨跌幅{} 小于目标涨跌幅{}'.format(self.now_date,name,stock,last_pirce,mean_price,zdf,x))
                return ''
        else:
            print('{} 模块{} 不卖出{} 目前时间{} 小于开始时间{}'.format(self.now_date,name,stock,date,start_date))
    def time_division_average_do_t(self,name='分时均线做T',interval=180,start_date=93000,x1=2,x2=-2,ratio=0.6):
        '''
        分时均线做T
        '''
        stock=str(self.stock)
        df=self.df
        df['价格']=pd.to_numeric(df['价格'])
        df['成交量']=pd.to_numeric(df['成交量'])
        df['分时均线'] = (df['价格'] * df['成交量']).cumsum() / df['成交量'].cumsum()
        df['时间']=pd.to_numeric(df['时间'])
        last_pirce=df['价格'].tolist()[-1]
        mean_price=df['分时均线'].tolist()[-1]
        date=df['时间'].tolist()[-1]
        now_date=datetime.now()
        df['大于']=IF(df['价格']>df['分时均线'],1,0)
        total_amount=df.shape[0]>0
        amount=df['大于'].sum()
        now_ratio=amount/total_amount
        if date>=start_date:
            if self.log.shape[0]>0:
                self.log['证券代码']=self.log['证券代码'].astype(str)
                log=self.log[self.log['模块名称']==name]
                log=log[log['证券代码']==stock]
                n=log.shape[0]
                shift_time=log['触发时间'].tolist()[-1]
                zdf=((last_pirce-mean_price)/mean_price)*100
                trader_date=self.calculate_time_diff(time_str1=shift_time,time_str2=now_date)
            else:
                zdf=((last_pirce-mean_price)/mean_price)*100
                trader_date=10000000000000000000000000000
                n=0
            if trader_date>=interval:
                if zdf>=x1:
                    print('{} 模块{} 卖出{} 现在价格{} 分时价格{} 涨跌幅{} 大于目标涨跌幅{}'.format(self.now_date,name,stock,last_pirce,mean_price,zdf,x1))
                    return 'sell'
                elif zdf<=x2:
                    if now_ratio>=ratio:
                        print('{} 模块{} 买入{} 现在价格{} 分时价格{} 涨跌幅{} 小于目标涨跌幅{}'.format(self.now_date,name,stock,last_pirce,mean_price,zdf,x2))
                        return 'buy'
                    else:
                        print('{} 模块{} 不交易{} 目前比例{} 小于强势比例{}'.format(self.now_date,name,stock,now_ratio,ratio))
                        return ''
                else:
                    print('{} 模块{} 不交易{} 现在价格{} 分时价格{} 涨跌幅{} '.format(self.now_date,name,stock,last_pirce,mean_price,zdf))
                    return ''
            else:
                print('{} 模块{} 不交易{} 现在价格{} 分时价格{} 涨跌幅{} 触发时间间隔{} 小于目标间隔{}'.format(self.now_date,name,stock,last_pirce,mean_price,zdf,trader_date,interval))
                return ''
        else:
            print('{} 模块{} 不交易{} 目前时间{} 小于开始时间{}'.format(self.now_date,name,stock,date,start_date))
            return ''
        
    
        
        
        
        
        
        



    
    
    
    







    




    
    
        
    
    

    
    
    
    
















            





        









                














        