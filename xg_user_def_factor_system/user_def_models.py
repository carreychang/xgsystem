import os
import pandas as pd
from trader_tool.tdx_indicator import *
import empyrical
import pandas as pd
from trader_tool.shape_analysis import shape_analysis
from trader_tool.analysis_models import analysis_models
from tdx_strategy_models.six_pulse_excalibur_hist import six_pulse_excalibur_hist
from tdx_strategy_models.small_fruit_band_trading import small_fruit_band_trading
from tdx_strategy_models.the_kirin_trend_line import the_kirin_trend_line
import os
import empyrical as ep
from xg_tdx_func.xg_tdx_func import *
class user_def_models:
    def __init__(self,df,index_df=''):
        '''
        分析模型
        自定义交易算法买入
        '''
        self.df=df
        self.index_df=index_df
        self.path=os.path.dirname(os.path.abspath(__file__))
    def alpha(self):
        '''
        alpha
        '''
        index_shape=self.index_df.shape[0]
        df_shape=self.df.shape[0]
        if index_shape>=df_shape:
            index_df=self.index_df[-df_shape:]
            df=self.df
        else:
            df=self.df[-index_shape:]
            index_df=self.index_df
        alpha=empyrical.alpha(df['close'].pct_change(),index_df['close'].pct_change())
        return alpha
    def max_drawdown(self):
        '''
        最大回撤
        '''
        index_shape=self.index_df.shape[0]
        df_shape=self.df.shape[0]
        if index_shape>=df_shape:
            index_df=self.index_df[-df_shape:]
            df=self.df
        else:
            df=self.df[-index_shape:]
            index_df=self.index_df
        max_drawdown=empyrical.max_drawdown(df['close'].pct_change())
        empyrical.annual_return
        return max_drawdown
    def annual_return(self):
        '''
        年华收益
        '''
        index_shape=self.index_df.shape[0]
        df_shape=self.df.shape[0]
        if index_shape>=df_shape:
            index_df=self.index_df[-df_shape:]
            df=self.df
        else:
            df=self.df[-index_shape:]
            index_df=self.index_df
        annual_return=empyrical.annual_return(df['close'].pct_change())
        return annual_return
    def annual_volatility(self):
        '''
        年华波动率
        '''
        index_shape=self.index_df.shape[0]
        df_shape=self.df.shape[0]
        if index_shape>=df_shape:
            index_df=self.index_df[-df_shape:]
            df=self.df
        else:
            df=self.df[-index_shape:]
            index_df=self.index_df
        annual_volatility=empyrical.annual_volatility(df['close'].pct_change())
        return annual_volatility
    def sharpe_ratio(self):
        '''
        夏普比例
        '''
        index_shape=self.index_df.shape[0]
        df_shape=self.df.shape[0]
        if index_shape>=df_shape:
            index_df=self.index_df[-df_shape:]
            df=self.df
        else:
            df=self.df[-index_shape:]
            index_df=self.index_df
        sharpe_ratio=empyrical.sharpe_ratio(df['close'].pct_change())
        return sharpe_ratio
    def conditional_value_at_risk(self):
        '''
        在险价值
        '''
        index_shape=self.index_df.shape[0]
        df_shape=self.df.shape[0]
        if index_shape>=df_shape:
            index_df=self.index_df[-df_shape:]
            df=self.df
        else:
            df=self.df[-index_shape:]
            index_df=self.index_df
        conditional_value_at_risk=empyrical.conditional_value_at_risk(df['close'].pct_change())
        return conditional_value_at_risk
    def beta_n(self,x=5):
        '''
        5日beta
        '''
        index_shape=self.index_df.shape[0]
        df_shape=self.df.shape[0]
        if index_shape>=df_shape:
            index_df=self.index_df[-df_shape:]
            df=self.df
        else:
            df=self.df[-index_shape:]
            index_df=self.index_df
        beta=empyrical.roll_beta(df['close'].pct_change(),index_df['close'].pct_change(),x)
        return beta.tolist()[-1]
    def alpha_n(self,x=5):
        '''
        5日alpha
        '''
        index_shape=self.index_df.shape[0]
        df_shape=self.df.shape[0]
        if index_shape>=df_shape:
            index_df=self.index_df[-df_shape:]
            df=self.df
        else:
            df=self.df[-index_shape:]
            index_df=self.index_df
        alpha=empyrical.roll_alpha(df['close'].pct_change(),index_df['close'].pct_change(),x)
        return alpha.tolist()[-1]
    def beta(self):
        '''
        beta
        '''
        index_shape=self.index_df.shape[0]
        df_shape=self.df.shape[0]
        if index_shape>=df_shape:
            index_df=self.index_df[-df_shape:]
            df=self.df
        else:
            df=self.df[-index_shape:]
            index_df=self.index_df
        beta=empyrical.beta(df['close'].pct_change(),index_df['close'].pct_change())
        return beta
    
    def mean_line_models(self,x1=3,x2=5,x3=10,x4=15,x5=20):
        '''
        均线模型
        趋势模型
        '''
        df=self.df
        df1=pd.DataFrame()
        df1['date']=df['date']
        df1['x1']=df['close'].rolling(window=x1).mean()
        df1['x2']=df['close'].rolling(window=x2).mean()
        df1['x3']=df['close'].rolling(window=x3).mean()
        df1['x4']=df['close'].rolling(window=x4).mean()
        df1['x5']=df['close'].rolling(window=x5).mean()
        score=0
        #加分的情况
        mean_x1=df1['x1'].tolist()[-1]
        mean_x2=df1['x2'].tolist()[-1]
        mean_x3=df1['x3'].tolist()[-1]
        mean_x4=df1['x4'].tolist()[-1]
        mean_x5=df1['x5'].tolist()[-1]
        #相邻2个均线进行比较
        if mean_x1>=mean_x2:
            score+=25
        if mean_x2>=mean_x3:
            score+=25
        if mean_x3>=mean_x4:
            score+=25
        if mean_x4>=mean_x5:
            score+=25
        return score
    def standing_average_line(self,n=5):
        '''
        站上均线分析
        '''
        df=self.df
        df['n']=df['close'].rolling(n).mean()
        line=df['n'].tolist()[-1]
        price=df['close'].tolist()[-1]
        if price>=line:
            return 1
        else:
            return 0
    
    def cacal_price_limit(self):
        '''
        计算涨跌幅
        '''
        df=self.df
        zdf=df['涨跌幅'].tolist()[-1]
        return zdf
    def cacal_n_return(self,n=3):
        df=self.df[-n:]
        return df['涨跌幅'].sum()
    def cross_up(self,x1=5,x2=10):
        '''
        金叉
        '''
        df=self.df
        result=CROSS(S1=MA(df['close'],x1),S2=MA(df['close'],x2))
        return result[-1]
    def cross_down(self,x1=5,x2=10):
        '''
        死叉
        '''
        df=self.df
        result=CROSS(S1=MA(df['close'],x2),S2=MA(df['close'],x1))
        return result[-1]
    def std(self,x=5):
        '''
        标准差
        '''
        df=self.df
        result=STD(S=df['close'],N=x)
        return result[-1]
    def llv(self,x=5):
        '''
        5日支持
        '''
        df=self.df
        result=LLV(S=df['close'],N=x)
        return result[-1]
    def hhv(self,x=5):
        '''
        5日压力
        '''
        df=self.df
        result=HHV(S=df['close'],N=x)
        return result[-1]
    def ema(self,x=5):
        '''
        5日指数移动平均
        '''
        df=self.df
        result=EMA(df['close'],x)
        return result[-1]
    def slope(self,x=5):
        '''
        5日斜率  
        '''
        df=self.df
        result=SLOPE(df['close'],x)
        return result[-1]
    def cci(self):
        '''
        CCI商品路劲指标
        '''
        df=self.df
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        OPEN=df['open']
        result=CCI(CLOSE,HIGH,LOW,N=14)
        return result.tolist()[-1]
    def kdj_k(self):
        '''
        kdj k值
        '''
        df=self.df
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        OPEN=df['open']
        k,d,j=KDJ(CLOSE,HIGH,LOW, N=9,M1=3,M2=3)
        return k.tolist()[-1]
    def kdj_d(self):
        '''
        kdj d值
        '''
        df=self.df
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        OPEN=df['open']
        k,d,j=KDJ(CLOSE,HIGH,LOW, N=9,M1=3,M2=3)
        return d.tolist()[-1]
    def kdj_j(self):
        '''
        kdj j值
        '''
        df=self.df
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        OPEN=df['open']
        k,d,j=KDJ(CLOSE,HIGH,LOW, N=9,M1=3,M2=3)
        return j.tolist()[-1]
    def mfi(self):
        '''
        最近流量指标
        '''
        df=self.df
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        OPEN=df['open']
        VOL=df['volume']
        result=MFI(CLOSE,HIGH,LOW,VOL,N=14)
        return result.tolist()[-1]
    def mtm(self):
        '''
        动量线指标
        '''
        df=self.df
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        OPEN=df['open']
        VOL=df['volume']
        mtm,mtmma=MTM(CLOSE,)
        return mtm.tolist()[-1]
    def mtmma(self):
        '''
        平均动量线指标
        '''
        df=self.df
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        OPEN=df['open']
        VOL=df['volume']
        mtm,mtmma=MTM(CLOSE)
        return mtmma.tolist()[-1]
    def osc(self):
        '''
        变动速度
        '''
        df=self.df
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        OPEN=df['open']
        VOL=df['volume']
        osc,maosc=OSC(CLOSE,)
        return osc.tolist()[-1]
    def maosc(self):
        '''
        平均变动速度
        '''
        df=self.df
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        OPEN=df['open']
        VOL=df['volume']
        osc,maosc=OSC(CLOSE,)
        return maosc.tolist()[-1]
    def roc(self):
        '''
        变动率指标
        '''
        df=self.df
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        OPEN=df['open']
        VOL=df['volume']
        roc,maroc=ROC(CLOSE)
        return roc.tolist()[-1]
    def maroc(self):
        '''
        平均变动率指标
        '''
        df=self.df
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        OPEN=df['open']
        VOL=df['volume']
        roc,maroc=ROC(CLOSE,)
        return maroc.tolist()[-1]
    def rsi1(self):
        '''
        rsi1相对强弱指标
        '''
        df=self.df
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        OPEN=df['open']
        VOL=df['volume']
        rsi1,rsi2,rsi3=RSI(CLOSE, N1=6,N2=12,N3=24)
        return rsi1.tolist()[-1]
    def rsi2(self):
        '''
        rsi2相对强弱指标
        '''
        df=self.df
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        OPEN=df['open']
        VOL=df['volume']
        rsi1,rsi2,rsi3=RSI(CLOSE, N1=6,N2=12,N3=24)
        return rsi2.tolist()[-1]
    def rsi3(self):
        '''
        rsi3相对强弱指标
        '''
        df=self.df
        CLOSE=df['close']
        LOW=df['low']
        HIGH=df['high']
        OPEN=df['open']
        VOL=df['volume']
        rsi1,rsi2,rsi3=RSI(CLOSE, N1=6,N2=12,N3=24)
        return rsi3.tolist()[-1]
    def mean_n_line(self,n=5):
        '''
        N日均线
        '''
        df=self.df
        df['mean_line']=df['close'].rolling(n).mean()   
        return df['mean_line'].tolist()[-1]  
    def bias_n(self,n=5):
        '''
        N日乖离率
        '''
        df=self.df
        CLOSE=df['close']
        BIAS = (CLOSE - MA(CLOSE, n)) / MA(CLOSE, n) * 100
        return BIAS.tolist()[-1]
    def mean_line_models_buy(self,x1=3,x2=5,x3=10,x4=15,x5=20):
        '''
        均线模型
        趋势模型
        '''
        df=self.df
        df1=pd.DataFrame()
        df1['date']=df['date']
        df1['x1']=df['close'].rolling(window=x1).mean()
        df1['x2']=df['close'].rolling(window=x2).mean()
        df1['x3']=df['close'].rolling(window=x3).mean()
        df1['x4']=df['close'].rolling(window=x4).mean()
        df1['x5']=df['close'].rolling(window=x5).mean()
        score=0
        #加分的情况
        mean_x1=df1['x1'].tolist()[-1]
        mean_x2=df1['x2'].tolist()[-1]
        mean_x3=df1['x3'].tolist()[-1]
        mean_x4=df1['x4'].tolist()[-1]
        mean_x5=df1['x5'].tolist()[-1]
        #相邻2个均线进行比较
        if mean_x1>=mean_x2:
            score+=25
        if mean_x2>=mean_x3:
            score+=25
        if mean_x3>=mean_x4:
            score+=25
        if mean_x4>=mean_x5:
            score+=25
        return score
    def standing_average_line(self,n=5):
        '''
        站上均线分析
        '''
        df=self.df
        df['n']=df['close'].rolling(n).mean()
        line=df['n'].tolist()[-1]
        price=df['close'].tolist()[-1]
        if price>=line:
            return 1
        else:
            return 0
    def down_average_line(self,n=5):
        '''
        跌破均线分析
        '''
        df=self.df
        df['n']=df['close'].rolling(n).mean()
        line=df['n'].tolist()[-1]
        price=df['close'].tolist()[-1]
        if line>=price:
            return 1
        else:
            return 0
    def cacal_price_limit(self):
        '''
        计算涨跌幅
        '''
        df=self.df
        zdf=df['涨跌幅'].tolist()[-1]
        return zdf
    def cacal_degree_of_deviation(self,n=5):
        '''
        计算偏离度
        '''
        hist=self.df
        price=hist['close'].tolist()[-1]
        hist['mean_line']=hist['close'].rolling(window=n).mean()
        line=hist['mean_line'].tolist()[-1]
        deviation=((price-line)/line)*100
        return deviation
    def cacal_diurnal_cycle(self):
        '''
        计算日周期
        '''
        df=self.df
        models=six_pulse_excalibur_hist(df=df)
        df=models.six_pulse_excalibur_hist()
        signal=df['signal'].tolist()[-1]
        return signal
    def cacal_diurnal_cycle_amount(self,n=5):
        '''
        计算日周期数量
        '''
        df=self.df
        models=six_pulse_excalibur_hist(df=df)
        df=models.six_pulse_excalibur_hist()
        signal=df['signal'].tolist()[-n:]
        return sum(signal)
    def cacal_diurnal_cycle_lx(self,n=5):
        '''
        连续六脉神剑数量
        '''
        df=self.df
        models=six_pulse_excalibur_hist(df=df)
        df=models.six_pulse_excalibur_hist()
        signal=df['signal']
        amount=BARSLASTCOUNT(S=signal>=5)
        return amount.tolist()[-1]

    def cacal_return_N(self,n=5):
        '''
        N日收益
        '''
        df=self.df
        zdf=df['涨跌幅'].tolist()[-n:]
        return sum(zdf)
    def cacal_slope(self,n=5):
        '''
        线性回归斜率 
        '''
        df=self.df
        value=SLOPE(S=df['close'],N=n)
        return value.tolist()[-1]
    def cacal_bond_stats(self):
        '''
        波段状态
        '''
        df=self.df
        models=small_fruit_band_trading(df)
        df=models.small_fruit_band_trading()
        stats=df['stats'].tolist()[-1]
        return stats
    def cacal_bond_lx_buy(self):
        '''
        连续买波段的数量
        '''
        df=self.df
        models=small_fruit_band_trading(df)
        df=models.small_fruit_band_trading()
        df['stats']=df['stats'].apply(lambda x: 1 if x=='买' else 0)
        stats=df['stats']
        amount=BARSLASTCOUNT(stats>=1)
        return amount.tolist()[-1]
    def cacal_bond_lx_sell(self):
        '''
        连续卖波段的数量
        '''
        df=self.df
        models=small_fruit_band_trading(df)
        df=models.small_fruit_band_trading()
        df['stats']=df['stats'].apply(lambda x: 1 if x=='买' else 0)
        stats=df['stats']
        amount=BARSLASTCOUNT(stats<=0)
        return amount.tolist()[-1]
    def cacal_kirin_stats(self):
        '''
        麒麟趋势状态
        '''
        df=self.df
        models=the_kirin_trend_line(df)
        df=models.the_kirin_trend_line()
        stats=df['stats'].tolist()[-1]
        return stats
    def cacal_kirin_lx_buy(self):
        '''
        麒麟趋势连续买数量
        '''
        df=self.df
        models=the_kirin_trend_line(df)
        df=models.the_kirin_trend_line()
        df['stats']=df['stats'].apply(lambda x: 1 if x=='买' else 0)
        stats=df['stats']
        amount=BARSLASTCOUNT(stats>=1)
        return amount.tolist()[-1]
    def cacal_kirin_lx_sell(self):
        '''
        麒麟趋势连续卖数量
        '''
        df=self.df
        models=the_kirin_trend_line(df)
        df=models.the_kirin_trend_line()
        df['stats']=df['stats'].apply(lambda x: 1 if x=='买' else 0)
        stats=df['stats']
        amount=BARSLASTCOUNT(stats<=0)
        return amount.tolist()[-1]
    def cacal_kirin_score(self):
        '''
        麒麟趋势分数
        '''
        df=self.df
        models=the_kirin_trend_line(df)
        df=models.the_kirin_trend_line()
        score=df['量化评分'].tolist()[-1]
        return score
    def max_drawdown(self,n=5):
        '''
        最大回撤
        '''
        df=self.df
        value=ep.max_drawdown(returns=df['close'].pct_change()[-n:])
        return value*100
    def open_price(self):
        '''
        开盘价
        '''
        df=self.df
        value=df['open'].tolist()[-1]
        return value
    def close_price(self):
        '''
        收盘价
        '''
        df=self.df
        value=df['close'].tolist()[-1]
        return value
    def low_price(self):
        '''
        最低价
        '''
        df=self.df
        value=df['low'].tolist()[-1]
        return value
    def high_price(self):
        '''
        最高价
        '''
        df=self.df
        value=df['high'].tolist()[-1]
        return value
    def volue(self,n=3):
        '''
        成交量
        '''
        df=self.df
        value=df['volume'].rolling(n).sum().tolist()[-1]
        return value
    def amount(self,n=3):
        '''
        成交量额
        '''
        df=self.df
        value=df['成交额'].rolling(n).sum().tolist()[-1]
        return value
    def hsl(self,n=3):
        '''
        换手率
        '''
        df=self.df
        value=df['换手率'].rolling(n).sum().tolist()[-1]
        return value
    def mean_line_n(self,n=3):
        '''
        N日均线
        '''
        df=self.df
        df['value']=df['close'].rolling(n).mean()
        value=df['value'].tolist()[-1]
        return value
    def down_n_mean_line(self,n=3):
        '''
        跌破N日线
        '''
        df=self.df
        df['line']=df['close'].rolling(n).mean()
        line=df['line'].tolist()[-1]
        close=df['close'].tolist()[-1]
        if close<=line:
            return 1
        else:
            return 0
    def upper_n_mean_line(self,n=3):
        '''
        站上3日均线
        '''
        df=self.df
        df['line']=df['close'].rolling(n).mean()
        line=df['line'].tolist()[-1]
        close=df['close'].tolist()[-1]
        if close>line:
            return 1
        else:
            return 0
    def pl_mean_line(self,n=3):
        '''
        偏离3日均线
        '''
        df=self.df
        df['line']=df['close'].rolling(n).mean()
        line=df['line'].tolist()[-1]
        close=df['close'].tolist()[-1]
        zdf=((close-line)/line)*100
        return zdf


    
    
    
    
    

    





    


    


    
    


        
    


            


    