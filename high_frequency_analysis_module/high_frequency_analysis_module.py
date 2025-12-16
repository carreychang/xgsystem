from qmt_trader.xtquant import xtdata
from datetime import datetime
class high_frequency_analysis_module:
    def __init__(self,stock,hist,tick,base):
        '''
        qmt高频分析模块
        '''
        self.stock=stock
        self.hist=hist
        self.tick=tick
        self.base=base
    def check_is_up_limit(self):
        '''
        检查是否是涨停
        '''
        askPrice=sum(self.tick['askPrice'])
        if askPrice==0:
            return True
        else:
            return False
    def check_is_down_limit(self):
        '''
        检查是否是跌停
        '''
        askPrice=sum(self.tick['bidPrice'])
        if askPrice==0:
            return True
        else:
            return False
    def get_buy_sell_volume(self):
        '''
        买卖的数量差
        buy-sell
        '''
        tick=self.tick
        volume=sum(tick['bidVol'])-sum(tick['askVol'])
        return volume
    def get_buy_sell_ratio(self):
        '''
        买卖的比例
        '''
        tick=self.tick
        ratio=((sum(tick['bidVol'])-sum(tick['askVol']))/sum(tick['askVol']))/100
        return ratio
    def get_zdf(self):
        '''
        涨跌幅
        '''
        tick=self.tick
        zdf=((tick['lastPrice']-tick['lastClose'])/tick['lastClose'])*100
        return zdf
    def get_spot_price(self):
        '''
        获取最新价
        '''
        tick=self.tick
        return tick['lastPrice']

    def get_sealing_ratio(self):
        '''
        封单比率
        '''
        base=self.base
        tick=self.tick
        FloatVolume=base['FloatVolume']
        bidVol=sum(tick['bidVol'])
        return (FloatVolume/bidVol)*100
    def get_pulse_data(self,n=200,zdf=3):
        '''
        3秒一个tick
        10秒上涨3%
        '''
        hist=self.hist
        lastPrice_list=hist['lastPrice'].tolist()[-n:]
        now_zdf=((lastPrice_list[-1]-lastPrice_list[0])/lastPrice_list[0])*100
        print('脉冲涨跌幅{}'.format(now_zdf))
        if  now_zdf>=zdf:
            return True
        else:
            return False
    def get_conditions_pulse_data(self,n1=5,n=200,zdf=3):
        '''
        条件脉冲
        '''
        total_zdf=n1
        tick_zdf=self.get_zdf()
        hist=self.hist
        lastPrice_list=hist['lastPrice'].tolist()[-n:]
        now_zdf=((lastPrice_list[-1]-lastPrice_list[0])/lastPrice_list[0])*100
        print('{} {} 脉冲涨跌幅{} 目前涨跌幅{}'.format(self.stock,datetime.now(),now_zdf,tick_zdf))
        if  now_zdf>=zdf and tick_zdf>total_zdf:
            return True
        else:
            return False
    def check_the_number_of_plate_openings(self):
        '''
        检查开板次数
        上一个tick涨停,下一个tick没有涨停
        '''
        #剔除集合竞价的数据
        hist=self.hist
        hist['date']=hist.index.tolist()
        hist['date']=hist['date'].apply(lambda x: int(str(x)[8:]))
        hist=hist[hist['date']>=92800]
        hist=hist[hist['date']<=145659]
        hist['stats']=hist['askVol'].apply(lambda x:1 if sum(x)==0 else 0)
        hist['开板']=hist['stats']-hist['stats'].shift(1)
        hist['开板']=hist['开板'].apply(lambda x: '是' if x==1 else '不是')
        amount=hist['开板'].tolist().count('是')
        print('{} {} 开板的次数{}'.format(self.stock,datetime.now(),amount))
        return amount-1,hist
    def get_tick_ratio(self,n=3,ratio=1.1):
        '''
        买卖的比例
        '''
        hist=self.hist[-3:]
        hist['bidVol_1']=hist['bidVol'].apply(lambda x: sum(x))
        hist['askVol_1']=hist['askVol'].apply(lambda x: sum(x))
        bidVol_1=hist['bidVol_1'].sum()
        askVol_1=hist['askVol_1'].sum()
        zdf=bidVol_1/askVol_1
        return zdf
if __name__=='__main__':
    stock_list=['000099.SZ']
    start_time='20241119'
    end_time='20500101'
    count=-1
    xtdata.subscribe_quote(stock_code=stock_list[-1],period='tick',start_time=start_time,end_time=end_time,count=count)
    hist=xtdata.get_market_data_ex(stock_list=stock_list,period='tick',start_time=start_time,end_time=end_time,count=count)
    hist=hist[stock_list[-1]]
    tick=xtdata.get_full_tick(code_list=stock_list)
    tick=tick[stock_list[-1]]
    base=xtdata.get_instrument_detail(stock_code=stock_list[-1])
    models=high_frequency_analysis_module('',hist,tick,base)
    amount=models.get_tick_ratio()
    print(amount)
    
