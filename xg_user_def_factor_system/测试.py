import pandas as pd
df=pd.read_excel(r'自定义交易股票池.xlsx')
df['证券代码']=df['证券代码'].astype(str)
def adjust_stock(stock='600031.SH'):
        '''
        调整代码
        '''
        if stock[-2:]=='SH' or stock[-2:]=='SZ' or stock[-2:]=='sh' or stock[-2:]=='sz':
            stock=stock.upper()
        else:
            if stock[:3] in ['600','601','603','605','688','689',
                             ] or stock[:2] in ['11','51','58']:
                stock=stock+'.SH'
            else:
                stock=stock+'.SZ'
        return stock
df['证券代码']=df['证券代码'].apply(lambda x: adjust_stock(x))
df['名称']=df['名称'].astype(str)
print(str(df['证券代码'].tolist()).replace("'",'"'))
print(str(df['名称'].tolist()).replace("'",'"'))
