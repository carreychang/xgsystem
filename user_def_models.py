from xgtrader.stock_data_ths import stock_data_ths
from xgtrader.bond_cov_data_ths import bond_cov_data_ths
from xgtrader.etf_fund_data_ths import etf_fund_data_ths
from xgtrader.xgtrader import xgtrader
from xgtrader.unification_data_ths import unification_data_ths
from trader_tool.ths_limitup_data import ths_limitup_data
from trader_tool.dfcf_rq import popularity
from trader_tool.ths_rq import ths_rq
from trader_tool import jsl_data
from trader_tool.dfcf_theme import dfcf_theme
from trader_tool.stock_upper_data import stock_upper_data
from trader_tool.analysis_models import analysis_models
from trader_tool.shape_analysis import shape_analysis
from trader_tool.trader_frame import trader_frame
from trader_tool.base_func import base_func
import time
import json
import pywencai
import pandas as pd
from trader_tool.stock_em import stock_em
from trader_tool.unification_data import unification_data

from trader_models.global_broad_class_low_correlation_trend_rotation_strategy.global_broad_class_low_correlation_trend_rotation_strategy import global_broad_class_low_correlation_trend_rotation_strategy
from trader_models.global_outer_disc_six_pulse_excalibur_trend_strategy.global_outer_disc_six_pulse_excalibur_trend_strategy import global_outer_disc_six_pulse_excalibur_trend_strategy
from trader_models.global_major_asset_six_pulse_excalibur_rotation_strategy.global_major_asset_six_pulse_excalibur_rotation_strategy import global_major_asset_six_pulse_excalibur_rotation_strategy
from trader_models.small_fruit_small_market_trend_enhancement_strategy.small_fruit_small_market_trend_enhancement_strategy import small_fruit_small_market_trend_enhancement_strategy
from trader_models.global_broad_class_low_correlation_six_pulse_excalibur_trend_rotation_strategy.global_broad_class_low_correlation_six_pulse_excalibur_trend_rotation_strategy import global_broad_class_low_correlation_six_pulse_excalibur_trend_rotation_strategy
from trader_models.global_outboard_trend_strategy.global_outboard_trend_strategy import global_outboard_trend_strategy
from trader_models.simmons_trend_enhancement_strategy_microstock_shares.simmons_trend_enhancement_strategy_microstock_shares import simmons_trend_enhancement_strategy_microstock_shares
from trader_models.simmons_trend_enhancement_zz1000_strategy.simmons_trend_enhancement_zz1000_strategy import simmons_trend_enhancement_zz1000_strategy
from trader_models.simmons_trend_enhancement_zz2000_strategy.simmons_trend_enhancement_zz2000_strategy import simmons_trend_enhancement_zz2000_strategy
from trader_models.global_main_fund_six_pulse_excalibur_trend_strategy.global_main_fund_six_pulse_excalibur_trend_strategy import global_main_fund_six_pulse_excalibur_trend_strategy
from trader_models.global_main_fund_band_trading_strategy.global_main_fund_band_trading_strategy import global_main_fund_band_trading_strategy
from trader_models.simmons_trend_enhancement_band_cov_strategy.simmons_trend_enhancement_band_cov_strategy import simmons_trend_enhancement_band_cov_strategy
from trader_models.simmons_convertible_bond_trading_system.simmons_convertible_bond_trading_system import simmons_convertible_bond_trading_system
from trader_models.simmons_trend_enhancement_gz2000_strategy.simmons_trend_enhancement_gz2000_strategy import simmons_trend_enhancement_gz2000_strategy
from trader_models.simmons_trend_enhancement_xpcz_strategy.simmons_trend_enhancement_xpcz_strategy import simmons_trend_enhancement_xpcz_strategy
from trader_models.simmons_trend_enhancement_A500_strategy.simmons_trend_enhancement_A500_strategy import simmons_trend_enhancement_A500_strategy
from trader_models.simmons_trend_enhancement_zz800_strategy.simmons_trend_enhancement_zz800_strategy import simmons_trend_enhancement_zz800_strategy
from trader_models.simmons_trend_enhancement_hylt_strategy.simmons_trend_enhancement_hylt_strategy import simmons_trend_enhancement_hylt_strategy
from trader_models.simmons_trend_enhancement_hs300_strategy.simmons_trend_enhancement_hs300_strategy import simmons_trend_enhancement_hs300_strategy
from trader_models.simmons_trend_enhancement_zzyq_strategy.simmons_trend_enhancement_zzyq_strategy import simmons_trend_enhancement_zzyq_strategy
from trader_models.simmons_trend_enhancement_dpg_strategy.simmons_trend_enhancement_dpg_strategy import simmons_trend_enhancement_dpg_strategy
from trader_models.simmons_trend_enhancement_gfhg_strategy.simmons_trend_enhancement_gfhg_strategy import simmons_trend_enhancement_gfhg_strategy
from trader_models.simmons_trend_enhancement_zyxjl_strategy.simmons_trend_enhancement_zyxjl_strategy import simmons_trend_enhancement_zyxjl_strategy
from trader_models.simmons_trend_enhancement_zqg_strategy.simmons_trend_enhancement_zqg_strategy import simmons_trend_enhancement_zqg_strategy
from trader_models.simmons_trend_enhancement_fzqg_strategy.simmons_trend_enhancement_fzqg_strategy import simmons_trend_enhancement_fzqg_strategy
from trader_models.simmons_trend_stock_user_def_stock_strategy.simmons_trend_stock_user_def_stock_strategy import simmons_trend_stock_user_def_stock_strategy
from trader_models.simmons_trend_band_cov_user_def_stock_strategy.simmons_trend_band_cov_user_def_stock_strategy import simmons_trend_band_cov_user_def_stock_strategy
from trader_models.simmons_trend_fund_user_def_stock_strategy.simmons_trend_fund_user_def_stock_strategy import simmons_trend_fund_user_def_stock_strategy
from trader_models.simmons_convertible_bond_3_low_system.simmons_convertible_bond_3_low_system import simmons_convertible_bond_3_low_system
from trader_models.simmons_convertible_bond_5_factor_system.simmons_convertible_bond_5_factor_system import simmons_convertible_bond_5_factor_system
from trader_models.global_outboard_trend_strategy.global_outboard_trend_strategy import global_outboard_trend_strategy
class user_def_models:
    def __init__(self,trader_tool='ths',exe='C:/同花顺软件/同花顺/xiadan.exe',tesseract_cmd='C:/Program Files/Tesseract-OCR/tesseract',
                qq='1029762153@qq.com',open_set='否',qmt_path='D:/国金QMT交易端模拟/userdata_mini',
                qmt_account='55009640',qmt_account_type='STOCK',data_api='qmt'):
        '''
        自定义模型
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
        order_frame=trader_frame(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                 open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                 qmt_account_type=self.qmt_account_type)
        self.trader=order_frame.get_trader_frame()
        data=unification_data(trader_tool=self.trader_tool,data_api=self.data_api)
        self.data=data.get_unification_data()
        self.stats=0
        self.base_func=base_func()
        
    def connect(self):
        self.trader.connect()
    def run_global_outboard_trend_strategy(self):
        '''
        全球外盘基金波段趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=global_outboard_trend_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_global_outboard_trend_strategy',data_api=self.data_api)
            models.updata_all_data()
        else:
            print('西蒙斯可转债5因子交易策略不是交易时间')
    def run_simmons_convertible_bond_5_factor_system(self):
        '''
        西蒙斯可转债5因子交易策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_convertible_bond_5_factor_system(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_convertible_bond_5_factor_system',data_api=self.data_api)
            models.updata_all_data()
        else:
            print('西蒙斯可转债5因子交易策略不是交易时间')
    def run_simmons_convertible_bond_3_low_system(self):
        '''
        西蒙斯可转债3低交易策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_convertible_bond_3_low_system(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_convertible_bond_3_low_system',data_api=self.data_api)
            models.updata_all_data()
        else:
            print('西蒙斯可转债3低交易策略不是交易时间')
    def run_simmons_trend_fund_user_def_stock_strategy(self):
        '''
        西蒙斯基金自定义股票池趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_fund_user_def_stock_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_fund_user_def_stock_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯基金自定义股票池趋势增强策略不是交易时间')
    def run_simmons_trend_band_cov_user_def_stock_strategy(self):
        '''
        西蒙斯可转债自定义股票池趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_band_cov_user_def_stock_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_band_cov_user_def_stock_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯可转债自定义股票池趋势增强策略不是交易时间')
    def run_simmons_trend_stock_user_def_stock_strategy(self):
        '''
        西蒙斯股票自定义股票池趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_stock_user_def_stock_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_stock_user_def_stock_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯股票自定义股票池趋势增强策略不是交易时间')
    def run_simmons_trend_enhancement_fzqg_strategy(self):
        '''
        西蒙斯非周期股指数趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_enhancement_fzqg_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_enhancement_fzqg_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯非周期股指数趋势增强策略不是交易时间')

    def run_simmons_trend_enhancement_zqg_strategy(self):
        '''
        西蒙斯周期股指数趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_enhancement_zqg_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_enhancement_zqg_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯周期股指数趋势增强策略不是交易时间')

    def run_simmons_trend_enhancement_zyxjl_strategy(self):
        '''
        西蒙斯自由现金流指数趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_enhancement_zyxjl_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_enhancement_zyxjl_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯自由现金流指数趋势增强策略不是交易时间')
    def run_simmons_trend_enhancement_gfhg_strategy(self):
        '''
        西蒙斯高分红股指数趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_enhancement_gfhg_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_enhancement_gfhg_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯高分红股指数趋势增强策略不是交易时间')
    def run_simmons_trend_enhancement_dpg_strategy(self):
        '''
        西蒙斯大盘股指数趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_enhancement_dpg_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_enhancement_dpg_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯中证央企指数趋势增强策略不是交易时间')
    def run_simmons_trend_enhancement_zzyq_strategy(self):
        '''
        西蒙斯中证央企指数趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_enhancement_zzyq_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_enhancement_zzyq_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯中证央企指数趋势增强策略不是交易时间') 
    def run_simmons_trend_enhancement_hs300_strategy(self):
        '''
        西蒙斯沪深300指数趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_enhancement_hs300_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_enhancement_hs300_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯沪深300指数趋势增强策略不是交易时间') 
    def run_simmons_trend_enhancement_hylt_strategy(self):
        '''
        西蒙斯行业龙头指数趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_enhancement_hylt_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_enhancement_hylt_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯行业龙头指数趋势增强策略不是交易时间') 
    def run_simmons_trend_enhancement_zz800_strategy(self):
        '''
        西蒙斯中证800指数趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_enhancement_zz800_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_enhancement_zz800_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯中证800指数趋势增强策略不是交易时间') 
    def run_simmons_trend_enhancement_A500_strategy(self):
        '''
        西蒙斯中证A500指数趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_enhancement_A500_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_enhancement_A500_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯中证A500指数趋势增强策略不是交易时间') 
    def run_simmons_trend_enhancement_xpcz_strategy(self):
        '''
        西蒙斯小盘成长指数趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_enhancement_xpcz_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_enhancement_xpcz_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯小盘成长指数趋势增强策略不是交易时间') 
    def run_simmons_trend_enhancement_gz2000_strategy(self):
        '''
        西蒙斯国证2000指数趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_enhancement_gz2000_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_enhancement_gz2000_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print(' 西蒙斯国证2000指数趋势增强策略不是交易时间') 
    def run_simmons_convertible_bond_trading_system(self):
        '''
        西蒙斯可转债自定义因子交易策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_convertible_bond_trading_system(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='runn_simmons_trend_enhancement_band_cov_strategy',data_api=self.data_api)
            models.updata_all_data()
        else:
            print('西蒙斯可转债自定义因子交易策略不是交易时间') 
    def runn_simmons_trend_enhancement_band_cov_strategy(self):
        '''
        西蒙斯全市场可转债趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_enhancement_band_cov_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='runn_simmons_trend_enhancement_band_cov_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯全市场可转债趋势增强策略不是交易时间') 
    def run_global_main_fund_band_trading_strategy(self):
        '''
        全球主流基金波段趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=global_main_fund_band_trading_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_global_main_fund_band_trading_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('全球主流基金波段趋势增强策略不是交易时间') 

    def run_global_main_fund_six_pulse_excalibur_trend_strategy(self):
        '''
        全球主流基金六脉神剑趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=global_main_fund_six_pulse_excalibur_trend_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_global_main_fund_six_pulse_excalibur_trend_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('全球主流基金六脉神剑趋势增强策略不是交易时间') 
    def run_simmons_trend_enhancement_zz2000_strategy(self):
        '''
        西蒙斯中证2000指数趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_enhancement_zz2000_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_enhancement_zz2000_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯中证2000指数趋势增强策略不是交易时间') 
    def run_simmons_trend_enhancement_zz1000_strategy(self):
        '''
        西蒙斯中证1000指数趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_enhancement_zz1000_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_enhancement_zz1000_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯中证1000指数趋势增强策略不是交易时间') 
    def run_simmons_trend_enhancement_strategy_microstock_shares(self):
        '''
        西蒙斯通达信微盘股精选趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=simmons_trend_enhancement_strategy_microstock_shares(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_simmons_trend_enhancement_strategy_microstock_shares',data_api=self.data_api)
            models.update_all_data()
        else:
            print('西蒙斯通达信微盘股精选趋势增强策略不是交易时间') 
    def run_global_outboard_trend_strategy(self):
        '''
        全球外盘波段趋势增强策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=global_outboard_trend_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_global_outboard_trend_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('全球外盘波段趋势增强策略不是交易时间') 
    def run_global_broad_class_low_correlation_six_pulse_excalibur_trend_rotation_strategy(self):
        '''
        全球大类低相关性六脉神剑趋势轮动策略
        '''
        if  self.base_func.check_is_trader_date_1():
            models=global_broad_class_low_correlation_six_pulse_excalibur_trend_rotation_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_global_broad_class_low_correlation_six_pulse_excalibur_trend_rotation_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('小果reits基金六脉神剑趋势增强策略不是交易时间') 
    
    

    def sell_all_stock_on_time(self,name='尾盘一键清仓'):
        '''
        尾盘一键清仓
        '''
        df=self.trader.position()
        if df.shape[0]>0:
            for  stock,hold_amount,amount in zip(df['证券代码'].tolist(),
                        df['股票余额'].tolist(),df['可用余额'].tolist()):
                price=self.data.get_spot_data(stock=stock)['最新价']
                if amount>=10:
                    print(name,stock,'持有{} 可以{} 卖出{}'.format(hold_amount,amount,amount))
                    if self.trader_tool=='ths':
                        self.trader.sell(security=stock,price=price,amount=amount)
                    else:
                        self.trader.sell(security=stock,price=price,amount=amount,strategy_name=name,order_remark=name)
                else:
                    print(name,stock,'持有{} 可以{} 卖出{}'.format(hold_amount,amount,amount))

    
    
        
    
        
    
    
    def run_small_fruit_small_market_trend_enhancement_strategy(self):
        '''
        小果小市值趋势增强策略
        '''
        if  self.base_func.check_is_trader_date():
            models=small_fruit_small_market_trend_enhancement_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_small_fruit_small_market_trend_enhancement_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('小果小市值趋势增强策略不是交易时间') 
    
    
    
   

    
    
    def run_global_major_asset_six_pulse_excalibur_rotation_strategy(self):
        '''
        全球大类资产六脉神剑轮动策略
        '''
        if  self.base_func.check_is_trader_date():
            models=global_major_asset_six_pulse_excalibur_rotation_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                    open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                    qmt_account_type=self.qmt_account_type,name='run_global_major_asset_six_pulse_excalibur_rotation_strategy',data_api=self.data_api)
            models.update_all_data()
        else:
            print('全球大类资产六脉神剑轮动策略不是交易时间') 
   
    def run_global_broad_class_low_correlation_trend_rotation_strategy(self):
        '''
        全球大类低相关性波段趋势轮动策略
        '''
        
        models=global_broad_class_low_correlation_trend_rotation_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                qmt_account_type=self.qmt_account_type,name='run_global_broad_class_low_correlation_trend_rotation_strategy',data_api=self.data_api)
        models.update_all_data()
    
    
    
   
    
    def get_bidPrice1(self,stock='204001.SH'):
        '''
        获取价格
        '''
        xtdata.subscribe_whole_quote(code_list=[stock])
        tick=xtdata.get_full_tick(code_list=[stock])
        tick=tick[stock]
        return tick['lastPrice']
    def run_reverse_repurchase_of_treasury_bonds_1(self,buy_ratio=1):
        '''
        国债逆回购1,新的函数
        购买比例buy_ratio
        '''
        try:
            # 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
            account=self.trader.balance()
            av_cash=account['可用金额'].tolist()[-1]
            av_cash=float(av_cash)
            av_cash=av_cash*buy_ratio
            stock_code_sh = '204001.SH'
            stock_code_sz = '131810.SZ'
            price_sh = self.get_bidPrice1(stock_code_sh)
            price_sz = self.get_bidPrice1(stock_code_sz)
            bidPrice1 = max(price_sh,price_sz)
            if price_sh > price_sz:
                stock_code = stock_code_sh
            else:
                stock_code = stock_code_sz
            print(stock_code,bidPrice1)
            price=bidPrice1
            stock=stock_code
            #下单的数量要是1000
            amount = int(av_cash/1000)*10
            #借出钱sell
            if amount>0:
                fix_result_order_id =self.trader.sell(security=stock,amount=amount,price=price)
                text='国债逆回购交易类型 代码{} 价格{} 数量{} 订单编号{}'.format(stock,price,amount,fix_result_order_id)
                print(text)
                return '交易成功',text
            else:
                text='国债逆回购卖出 标的{} 价格{} 委托数量{}小于0有问题'.format(stock,price,amount)
                print(text)
                return '交易失败',text
        except Exception as e:
            print(e)
            return '国债逆回购卖出交易失败'
    def run_reverse_repurchase_of_treasury_bonds_2(self):
        '''
        国债逆回购1,新的函数
        购买比例buy_ratio
        '''
        try:
            self.trader.reverse_repurchase_of_treasury_bonds()
            print('逆回购回购成功****************')
        except Exception as e:
            print(e)
            return '国债逆回购卖出交易失败'
    
    
    

    
   
    
    def run_global_outer_disc_six_pulse_excalibur_trend_strategy(self):
        '''
        全球外盘六脉神剑趋势策略
        '''
        models=global_outer_disc_six_pulse_excalibur_trend_strategy(trader_tool=self.trader_tool,exe=self.exe,tesseract_cmd=self.tesseract_cmd,
                                open_set=self.open_set,qmt_path=self.qmt_path,qmt_account=self.qmt_account,
                                qmt_account_type=self.qmt_account_type,name='run_global_outer_disc_six_pulse_excalibur_trend_strategy',data_api=self.data_api)
        models.update_all_data()
if __name__=='__main__':
    with open('分析配置.json','r+',encoding='utf-8') as f:
        com=f.read()
    text=json.loads(com)
    trader_tool=text['交易系统']
    exe=text['同花顺下单路径']
    tesseract_cmd=text['识别软件安装位置']
    qq=text['发送qq']
    test=text['测试']                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    open_set=text['是否开启特殊证券公司交易设置']
    qmt_path=text['qmt路径']
    qmt_account=text['qmt账户']
    qmt_account_type=text['qmt账户类型']
    data_api=text['交易数据源']
    models=user_def_models(trader_tool=trader_tool,exe=exe,
                           tesseract_cmd=tesseract_cmd,qq=qq,
                           open_set=open_set,
                           qmt_path=r'{}'.format(qmt_path),
                           qmt_account=qmt_account,
                           qmt_account_type=qmt_account_type,
                           data_api=data_api)
    models.connect()
    func_list=text['自定义函数']
    for func in func_list:
        runc_func='models.{}()'.format(func)
        eval(runc_func)
