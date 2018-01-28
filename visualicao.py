#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 11:42:19 2018

@author: john
"""
#visualizacao

import numpy as np
import mysql.connector
import pandas as pd
import MySQLConnection
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
py.init_notebook_mode(connected=True)



conn = connection_sql()
df = pd.read_sql_query('select * from Allcoin limit 200;',conn)


btc_trace = go.Scatter(x=df.index, y=df['close'])
py.iplot([btc_trace])