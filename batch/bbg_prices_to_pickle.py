""" codigo que importa data de bloomberg, procesa, y descarga un pickle por
 -cada producto-, que contiene +-255 dataframes con [carry_days, Precio]"""

import os # borrar os al momento de subir a heroku (y solucionar ruta llamado funciones co)
os.chdir('D:\Dropbox\Documentos\Git\global-markets-i')

import pandas as pd
import pickle
import funcs_calendario_co as fcc


""" PASO 1. IMPORTO EXCEL PRECIOS BLOOMBERG """

header = ['spot','ff', 'ilib3m','ilib6m'] + ['ilib'+str(x) for x in range(1,11)] +\
	['ilib12','ilib15','ilib20','ilib30'] +\
	['tcs6m'] + ['tcs'+str(x) for x in range(1,11)] + ['tcs12','tcs15','tcs20','tcs30'] +\
	['icam1d','icam3m','icam6m','icam9m','icam1','icam18m'] + ['icam'+str(x) for x in range(2,11)] + ['icam12','icam15','icam20','icam30']+\
	['ptos1w','ptos2w'] + ['ptos'+str(x) for x in range(1,7)] + ['ptos9m','ptos12m','ptos18m','ptos24m'] +\
	['basis'+str(x) for x in range(1,11)] + ['basis12','basis15','basis20']

dfb = pd.read_excel('batch/bbg_hist_dnlder_excel.xlsx', sheet_name='valores', header=None,
					names=header, skiprows=6, index_col=0, parse_dates=[0])

dfb.sort_index(inplace=True)




""" 2. PRODUCTO SWAP LIBOR + TCS """

tenors_us = ['o/n','3m','6m']+[str(x)+'y' for x in range(1,11)]+['12y','15y','20y','30y']
meses_us  = [0,3,6]+[12*int(x) for x in range(1,11)]+[12*12,15*12,20*12,30*12]

ilib_dict={}
for d in dfb.index:

	df_us = pd.DataFrame(index=tenors_us, columns=['meses','val','carry_dias','ilib'])

	# numero de meses para cada tenor
	df_us.meses = meses_us

	# fecha settle del tenor o/n
	df_us.val['o/n'] = fcc.next_lab_settle(d,2,cal_ny=True)

	# fecha settle para los tenors largos en base al 1er settle
	df_us.val = df_us.apply(lambda x: fcc.settle_rule(df_us.val['o/n'],x.meses), axis=1)

	# calcula carry days en base al primer settle date
	df_us.carry_dias = (df_us.val - df_us.val[0]).apply(lambda x: x.days)

	df_us.ilib = dfb.loc[d][1:18].values

	ilib_dict[d] = df_us

# p_ilib es el nombre del pickle donde guardamos el diccionario --> Timestamps son las keys
pd.to_pickle(ilib_dict,"./batch/p_ilib.pkl")

# pout = pd.read_pickle("./batch/p_ilib.pkl")
# pout[d]




""" 2.2. PRODUCTO SWAP ICAM """

tenors_cl = ['o/n','3m','6m','9m','1y','18m']+[str(x)+'y' for x in range(2,11)]+['12y','15y','20y','30y']
meses_cl  = [0,3,6,9,12,18]+[12*int(x) for x in range(2,11)]+[12*12,15*12,20*12,30*12]

icam_dict={}
for d in dfb.index:

	df_cl = pd.DataFrame(index=tenors_cl, columns=['meses','val','carry_dias','icam'])

	# numero de meses para cada tenor
	df_cl.meses = meses_cl

	# fecha settle del tenor o/n
	df_cl.val['o/n'] = fcc.next_lab_settle(d,2,cal_ny=True)

	# fecha settle para los tenors largos en base al 1er settle
	df_cl.val = df_cl.apply(lambda x: fcc.settle_rule(df_cl.val['o/n'],x.meses), axis=1)

	# calcula carry days en base al primer settle date
	df_cl.carry_dias = (df_cl.val - df_cl.val[0]).apply(lambda x: x.days)

	df_cl.icam = dfb.loc[d][33:52].values

	icam_dict[d] = df_cl

# p_ilib es el nombre del pickle donde guardamos el diccionario --> Timestamps son las keys
pd.to_pickle(icam_dict,"./batch/p_icam.pkl")




""" 2.3. PRODUCTO PUNTOS FORWARD """

""" 2.4. USDCLP SPOT """

""" 2.5. PRODUCTO IR USDCLP BASIS  """

