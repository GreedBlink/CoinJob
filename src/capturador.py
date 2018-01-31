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
 

    


def mercados(exch = 'allcoin',moedas = ['ETH','LTC','BTG']):
    if not exch:
        exch = ccxt.allcoin()
    if exch == 'allcoin':    
        exch = ccxt.allcoin()   
    else:
        exch = ccxt.allcoin()   
    markets = exch.load_markets()
    market_pairs = list(markets.keys())
    aux = []
    for pair in market_pairs:
        if (str(moedas[0]) in pair or str(moedas[1]) in pair or str(moedas[2]) in pair) and 'BTC' in pair: 
            aux.append(pair)  
    return(aux)       

class capturador(object):
    

    def __init__(self,max_dias,symbol,time_frame):
        self.time_frame = time_frame
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
                  
            

class db(object):
    
    def __init__(self,exch,symbol,datafim,datainicio,data1):
        self.exch = exch
        self.symbol = symbol
        self.datafim = datafim
        self.datainicio = datainicio
        self.data1 = data1
        
    
    def connecta():
        conn = mysql.connector.connect(user='henriqu2_bianca', password='verao2018',
            host='77.104.156.92',database='henriqu2_storageCoin')
        return(conn)
        
    def save(self):
        conn = connecta()
        cursor = conn.cursor()
        for i in range(len(self.data1.datetime)):    
            cursor.execute('insert into Allcoin(date,timestamp,open,high,close,low,volume,mercado) values("'+str(self.data1.datetime[i]) +'",'+str(self.data1.timestamp[i]) + ','+str(self.data1.open[i]) + ',' +str(self.data1.high[i]) + ',' + str(self.data1.close[i]) + ',' + str(self.data1.low[i]) + ',' +str(self.data1.volume[i]) + ',"' + str(self.symbol) + '")')
            conn.commit()
        conn.close()
    
    def get(self):
        conn = connecta()
        if not self.datainicio or not self.datafim:    
            df =  pd.read_sql('Select * from Allcoin where mercado =' + '"' + str(self.symbol) + '"',conn)
        elif not self.datainicio:
            df =  pd.read_sql('Select * from Allcoin where mercado =' + '"' + str(self.symbol) + '"' + 'and date <= ' + '"' + str(self.datafim) + '"',conn)
        elif not self.datafim:
            df =  pd.read_sql('Select * from Allcoin where mercado =' + '"' + str(self.symbol) + '"' + 'and date >= ' + '"' + str(self.datainicio) + '"' ,conn)
        else:   
            df =  pd.read_sql('Select * from Allcoin where mercado =' + '"' + str(self.symbol) + '"' +  'and date BETWEEN ' + '"' + str(self.datainicio) + '"' + ' and ' + '"' + str(self.datafim) + '"',conn)
        conn.close()
        return df
            
            




