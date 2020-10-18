# -*- coding: utf-8 -*-

import pandas as pd
from os import listdir
from os.path import isfile, join
from pandas import DataFrame, read_excel, ExcelWriter, read_csv
from datetime import datetime


Path = 'C:/Users/romer/Documents/APPR/Empresa_Nacional/SH_BM/'

Data = DataFrame()
fechas = pd.date_range(start="2000-12-01",end="2020-06-01", freq='MS',tz=None)
fechas = fechas.astype(str)
for F in listdir(Path):
   if isfile(join(Path, F)):
       Data_i = read_excel(Path + F, sheet_name='Hoja2', header=None, dtype = str)
       banco = F[6:-11]
       Data_i['institucion'] = banco
       Data_i.columns = ['codigo','indicador']+list(fechas)+['Ban']
       Data_i = Data_i.loc[(Data_i['indicador'] == 'Cartera de crédito vigente')|
                           (Data_i['indicador'] == 'Cartera de crédito vencida')]
       Data_i=Data_i[['Ban','indicador']+list(fechas)[193:236]]
       Data = Data.append(Data_i, ignore_index = True)       
        
DataF = DataFrame()
for col in Data.columns:
    if (col != 'Ban') & (col !='indicador'):
        DataF_i = Data[['Ban','indicador', col]]
        DataF_i['Fec'] = col
        DataF_i.rename(columns={col:'val'}, inplace=True)
        
        DataF = DataF.append(DataF_i, ignore_index = True)
        
DataF.to_csv('C:/Users/romer/Documents/APPR/Empresa_Nacional/SH_BM/DataNacional.csv',sep=',',index=False)
        
        
        
        