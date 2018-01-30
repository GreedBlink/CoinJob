# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 11:58:57 2018

@author: jonatha.costa
"""
 
import urllib, json
import time,datetime
import pandas as pd
import ccxt
import numpy as np
import mysql.connector
 

class capturador(object):
    

    def __init__(self,max_dias,symbol,time_frame):
        self.time_frame = time_frame
        #datainicio é o dias de diferenca ate o dia de hj
        # ou seja, é a janela de dados até o dia de hj
        #datainicio sginifica a quantidade de dias pra captura
        base = datetime.datetime.today()
        data_inicial = (base - datetime.timedelta(days=max_dias)).date()
        time1 = time.mktime(data_inicial.timetuple())
        self.time1 = time1
        self.symbol = symbol
        
    
  
    def get_allcoin_captura(self):
            allcoin = ccxt.allcoin()
            ohclv = allcoin.fetch_ohlcv(symbol=self.symbol,timeframe=self.time_frame,since=self.time1)
            ohclv = np.array(ohclv)
            mercado = self.symbol
            l_timestamp = list(ohclv[:,0]/1000)
            l_date = []
            l_open = list(ohclv[:,1])
            l_high  = list(ohclv[:,2])
            l_close  = list(ohclv[:,3])
            l_low  = list(ohclv[:,4])
            l_volume  = list(ohclv[:,5])
             
            for i in range(len(ohclv)):
                timestamp = l_timestamp[i]
                t = datetime.datetime.fromtimestamp(timestamp)
                #lista_date.append(str(t.year)+'-'+str(t.month)+'-'+str(t.day))
                l_date.append(t)
                #l_timestamp.append(ohclv[i][0]/1000)
                #l_close.append(ohclv[i][2])
            
            struct_df = {
                        "datetime": l_date,
                         "timestamp":l_timestamp,
                         "close":l_close,
                         "high":l_high,
                         "low":l_low,
                         "open":l_open,
                         "volume":l_volume,
                         }
            allcoin = pd.DataFrame(struct_df)
            return(allcoin)
                  
            
def salva_banquinho(data1,symbol):
            conn = mysql.connector.connect(user='henriqu2_bianca', password='verao2018',
            host='77.104.156.92',database='henriqu2_storageCoin')
            cursor = conn.cursor()
            for i in range(len(data1.datetime)):    
                cursor.execute('insert into Allcoin(date,timestamp,open,high,close,low,volume,mercado) values("'+str(data1.datetime[i]) +'",'+str(data1.timestamp[i]) + ','+str(data1.open[i]) + ',' +str(data1.high[i]) + ',' + str(data1.close[i]) + ',' + str(data1.low[i]) + ',' +str(data1.volume[i]) + ',"' + str(symbol) + '")')
            conn.commit()
    

c = capturador(360,'LTC/BTC','1d')
df = c.get_allcoin_captura()
salva_banquinho(df,'LTC/BTC')



