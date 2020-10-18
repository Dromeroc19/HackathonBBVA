from os import listdir
from os.path import isfile, join
from pandas import DataFrame, read_excel, ExcelWriter, read_csv, pivot_table, concat
from locale import atof



#FUNCIONES=====================================================================

def Info(Path): #Función para juntar todos los archivos de una ruta en un DataFrame
    Data = DataFrame()
    for F in listdir(Path): #F := string con el nombre del archivo
        if isfile(join(Path, F)):
            Data_i = read_csv(Path + F, sep = ',', dtype = str)
            Data = Data.append(Data_i, ignore_index = True)
    return Data




#VALORES ENTRADA===============================================================

PathH = 'C:/Users/mromero01/Desktop/TEMP/Hackathon/'
ColG = ['Esc', 'Edo', 'ActEco', 'DesCre', 'Ban', 'Fec', 'CarTip', 'CarTotG', 'CarVigG', 'CarVenG', 'IMR', 'Cre', 'Acr']
ColQ = ['Esc', 'Tam', 'Edo', 'MonTip', 'Ban', 'Fec', 'Apo', 'CarTotQ', 'CarVigQ', 'CarVenQ', 'IMR', 'Acr', 'Cre', 'TasPon', 'PlzPon', 'MonDis', 'TasPonMD', 'PlzPonMd']


Ban = read_excel(PathH + 'Script/InfoGeneral.xlsx', sheet_name = 'Bancos', header = 0, dtype = None)
SofBan = read_excel(PathH + 'Script/InfoGeneral.xlsx', sheet_name = 'Bancos-SOFOM', header = 0, dtype = None)




#CARGA DE INFO================================================================

def InfoEmpresas(PathH, Tipo, ColNam):
    Data040_11 = Info(PathH + '040 - 11' + Tipo + '/')
    Data068_11 = Info(PathH + '068 - 11' + Tipo + '/')
    Data040_11.columns = ColNam
    Data068_11.columns = ColNam
    
    Col = ['CarTot' + Tipo, 'CarVig' + Tipo, 'CarVen' + Tipo]
    if Tipo == 'Q':
        Col = Col + ['TasPon']
    
    for c in Col:
        Data040_11[c] = Data040_11[c].str.replace(',', '').astype(float)
        Data068_11[c] = Data068_11[c].str.replace(',', '').astype(float)
    
    Data068_11.rename(columns={'Ban': 'SofBan'}, inplace = True)
    Data068_11 = Data068_11.merge(SofBan, how = 'inner', on = 'SofBan')
    
    if Tipo == 'Q':
        Pt040_11 = pivot_table(Data040_11.loc[Data040_11.Ban.isin(Ban.Ban)], values = Col, index = ['Fec', 'Edo', 'Ban'], aggfunc = sum, columns = 'Tam').reset_index()
        Pt068_11 = pivot_table(Data068_11.loc[Data068_11.Ban.isin(Ban.Ban)], values = Col, index = ['Fec', 'Edo', 'Ban'], aggfunc = sum, columns = 'Tam').reset_index()
    else:
        Pt040_11 = pivot_table(Data040_11.loc[Data040_11.Ban.isin(Ban.Ban)], values = Col, index = ['Fec', 'Edo', 'Ban'], aggfunc = sum).reset_index()
        Pt068_11 = pivot_table(Data068_11.loc[Data068_11.Ban.isin(Ban.Ban)], values = Col, index = ['Fec', 'Edo', 'Ban'], aggfunc = sum).reset_index()
    
    
    Data = Pt040_11.append(Pt068_11, ignore_index = True)
    Data = pivot_table(Data, values = Col, index = ['Fec', 'Edo', 'Ban'], aggfunc = sum)
    
    if Tipo == 'Q':
        Data.columns = ['_'.join(col) for col in Data.columns]
    
    return Data



DataQ = InfoEmpresas(PathH, 'Q', ColQ)
DataQ.to_csv('C:/Users/mromero01/Desktop/TEMP/Hackathon/Archivo1.csv', sep = ',')


DataG = InfoEmpresas(PathH, 'G', ColG)
DataG.to_csv('C:/Users/mromero01/Desktop/TEMP/Hackathon/Archivo2.csv', sep = ',')



concat([DataQ, DataG], axis=1, sort=False).to_csv('C:/Users/mromero01/Desktop/TEMP/Hackathon/Archivo0.csv', sep = ',')