from xms_quants_data_client.xms_quants_data_client  import xms_quants_data_client
client=xms_quants_data_client(
    url='http://124.220.32.224',
    port='8080',
    password='test')
df=client.get_full_tick(stock='513100.SH')
print(df)
