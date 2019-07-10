""" codigo PROCESO BATCH

PASO 1. importa y procesa data de bloomberg

PASO 2. a partir del paso1 crea un pickle / producto. con un df [carry_days, Precio] por cada dia de
 la historia (255 dias). Para ilib y icam calculo además `tasa-zero`

PASO 3. crea tasas camara off shore + tasas FRA1m, para cada uno de los 255d, para cada uno de los 255d.
Lo almacena en un diccionario, con un df por cada dia de historia. Almacenado en pickle

PASO 4. Crea historia de la FRA para los plazos 7d-380d + 18m + 24m.
Que es la que van a llamar los callback de la app

"""

import os # borrar os al momento de subir a heroku (y solucionar ruta llamado funciones co)
os.chdir('D:\Dropbox\Documentos\Git\global-markets-i')

import pandas as pd
import numpy as np
import pickle
import funcs_co as fc
import funcs_calendario_co as fcc


""" PASO 1. IMPORTO EXCEL PRECIOS BLOOMBERG """

header = ['spot','ff', 'ilib3m','ilib6m'] + ['ilib'+str(x) for x in range(1,11)] +\
	['ilib12','ilib15','ilib20','ilib30'] +\
	['tcs6m'] + ['tcs'+str(x) for x in range(1,11)] + ['tcs12','tcs15','tcs20','tcs30'] +\
	['icam1d','icam3m','icam6m','icam9m','icam1','icam18m'] + ['icam'+str(x) for x in range(2,11)] + ['icam12','icam15','icam20','icam30']+\
	['ptos1w','ptos2w'] + ['ptos'+str(x) for x in range(1,7)] + ['ptos9m','ptos12m','ptos18m','ptos24m'] +\
	['basis'+str(x) for x in range(1,11)] + ['basis12','basis15','basis20']

dfb = pd.read_excel('./batch/bbg_hist_dnlder_excel.xlsx', sheet_name='valores', header=None,
					names=header, skiprows=6, index_col=0, parse_dates=[0])

dfb.sort_index(inplace=True)

# fecha uso GMI, input manual del MIddle Office
fec_uso = pd.read_excel('./batch/bbg_hist_dnlder_excel.xlsx', sheetname='valores', header=None).iloc[1,1]


# dfb = dfb[-3:] # para que corra + rapido




""" PASO 2.1 PRODUCTO SWAP LIBOR """
tenors_us = ['o/n','3m','6m']+[str(x)+'y' for x in range(1,11)]+['12y','15y','20y','30y']
meses_us  = [0,3,6]+[12*int(x) for x in range(1,11)]+[12*12,15*12,20*12,30*12]

ilib_dict={}
for d in dfb.index:

	df_us = pd.DataFrame(index=tenors_us, columns=['meses','val','carry_dias','ilib','ilib_z'])

	# numero de meses para cada tenor
	df_us.meses = meses_us

	# fecha settle del tenor o/n
	df_us.val['o/n'] = fcc.next_lab_settle(d,2,cal_ny=True)

	# fecha settle para los tenors largos en base al 1er settle
	df_us.val = df_us.apply(lambda x: fcc.settle_rule(df_us.val['o/n'],x.meses), axis=1)

	# calcula carry days en base al primer settle date
	df_us.carry_dias = (df_us.val - df_us.val[0]).apply(lambda x: x.days)

	df_us.ilib = dfb.loc[d][1:18].values

	# transformo tasas act 90/360 ---> a tasas zero act/360. creo que IRS USD no es act, es meses de 30d
	df_us.ilib_z = df_us.apply(lambda x: fc.comp_a_z(x.carry_dias,x.ilib, periodicity=90), axis=1)

	ilib_dict[d] = df_us

# p_ilib es el nombre del pickle donde guardamos el diccionario --> Timestamps son las keys
# pd.to_pickle(ilib_dict,"./batch/p_ilib.pkl")



""" 2.2. PRODUCTO SWAP ICAM """
tenors_cl = ['o/n','3m','6m','9m','1y','18m']+[str(x)+'y' for x in range(2,11)]+['12y','15y','20y','30y']
meses_cl  = [0,3,6,9,12,18]+[12*int(x) for x in range(2,11)]+[12*12,15*12,20*12,30*12]

icam_dict={}
for d in dfb.index:

	df_cl = pd.DataFrame(index=tenors_cl, columns=['meses','val','carry_dias','icam','icam_z'])

	# numero de meses para cada tenor
	df_cl.meses = meses_cl

	# fecha settle del tenor o/n
	df_cl.val['o/n'] = fcc.next_lab_settle(d,2,cal_ny=True)

	# fecha settle para los tenors largos en base al 1er settle
	df_cl.val = df_cl.apply(lambda x: fcc.settle_rule(df_cl.val['o/n'],x.meses), axis=1)

	# calcula carry days en base al primer settle date
	df_cl.carry_dias = (df_cl.val - df_cl.val[0]).apply(lambda x: x.days)

	df_cl.icam = dfb.loc[d][33:52].values

	# el segmento money market ya está en convención tasa zero
	df_cl.icam_z.loc['o/n':'18m'] = df_cl.icam.loc['o/n':'18m']

	# transformo tasas act 180/360 ---> a tasas zero act/360
	df_cl.icam_z.loc['2y':] = df_cl.loc['2y':].apply(lambda x: fc.comp_a_z(x.carry_dias,x.icam, periodicity=180), axis=1)

	icam_dict[d] = df_cl

# p_ilib es el nombre del pickle donde guardamos el diccionario --> Timestamps son las keys
# pd.to_pickle(icam_dict,"./batch/p_icam.pkl")


""" 2.3. PRODUCTO PUNTOS FORWARD """
ptos_dict={}
for d in dfb.index:
	df_p = fcc.crea_cal_tenors(d)
	df_p['ptos'] = None
	df_p.ptos['TOD'] = 0
	df_p.ptos.loc[['1w','2w','1m','2m','3m','4m','5m','6m','9m','12m','18m','24m']] = dfb.loc[d][52:64].values
	ptos_dict[d] = df_p

# p_ptos es el nombre del pickle donde guardamos el diccionario --> Timestamps son las keys
# pd.to_pickle(ptos_dict,"./batch/p_ptos.pkl")


""" 2.4. USDCLP SPOT """
# pd.to_pickle(dfb.spot, "./batch/p_clp_spot.pkl")


# """ 2.5. PRODUCTO IR USDCLP BASIS + TCS """
# PENDIENTE... no es necesario para la pestaña FX puntos... si lo vamos a necesitar para la
# pestaña IR Basis.... sobretodo pensando en transformar el basis6m a un basis de 3m




""" PROCESO 3 CREA TASAS CAMARA OFF SHORE: convención simple act/360  y  TASAS FRA 1W """
d_icamos = {}
for d in dfb.index:

	# d = pd.Timestamp('2019-07-03 00:00:00')

	# llamo dict puntos, ese indice necesito, para crear el df donde guardar la icam-os
	dfio = ptos_dict[d][['pubdays','carry_days','ptos']].copy()

	# llamo las ilib-z, las mapeo en dfio, mendiante interpolación
	dfio['ilib_z'] = np.interp(x=dfio.pubdays.values,
							   xp=ilib_dict[d].carry_dias.values, fp=ilib_dict[d].ilib_z.values)

	# primero interpolar curva de puntos faltantes
	X = dfio[['pubdays','ptos']].dropna()
	dfio.ptos = np.interp(x=dfio.pubdays.values, xp=X.pubdays.values, fp=X.ptos.map(float).values)

	# calcula camara off-shore
	dfio['icam_os'] = dfio.apply(lambda x: fc.cam_lcl_a_os(dias=x.carry_days,spot=dfb.loc[d].spot,
														   ptos=x.ptos,iusd=x.ilib_z),axis=1)
	dfio['icam_os1'] = dfio.icam_os.shift(1) # col utilitaria calculo fra


	""" calculo FRA 1 semana """
	dfio['w'] = [0,0,1,2]+[x for x in range(4,76,4)]+[x for x in range(96,984,24)] # inicializo columna para asignar # semanas / tenor
	dfio['w1'] = dfio.w.shift(1)

	dfio['fra1w'] = None # inicializo col para calcular fra's
	dfio.loc['TOD':'1w','fra1w'] = dfio.loc['TOD':'1w','icam_os'].copy()

	dfio.loc['2w':,'fra1w'] = dfio.loc['2w':].apply(lambda x: fc.fra1w(x.w,x.w1,x.icam_os,x.icam_os1), axis=1)

	# guardo solo estas 3 cols para hacer mas ligero el pickle
	d_icamos[d] = dfio[['pubdays','icam_os','fra1w']]

pd.to_pickle(d_icamos, "./batch/icamos_fra.pkl")



""" PASO 4. Crea historia de la FRA para los plazos 7d-380d + 18m + 24m """
# lista de dias 0-380 + dias del 18m, 24m
cols = [str(x) for x in range(1,381)] + fcc.crea_cal_tenors(fec_uso).loc[['18m','24m'],'pubdays'].to_list()

dff = pd.DataFrame(index=dfb.index, columns=cols)

for d in dfb.index:
	dff.loc[d] = np.interp(x=dff.columns.map(int), xp=d_icamos[d].pubdays.values ,fp=d_icamos[d].fra1w.map(float))

# pickle que guarda un df, con la historia diaria, del ultimo año, de cada fra 1d-380d + 18m + 24m
pd.to_pickle(dff.astype('float').round(2),"./batch/hist_fra.pkl")


