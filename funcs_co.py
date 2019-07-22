""" 
Global Markets Insights, por Claudio Ortiz
python 3.6.6
"""

# import os
import pandas as pd 
import numpy as np
from scipy import interpolate
from numbers import Number
from itertools import permutations
import funcs_calendario_co as fcc
from datetime import timedelta


def weird_division(n, d):
	""" función división, que en el caso excepcional de dividir x cero --> return: 0"""
	# return n / d if d else float('nan')
	return n / d if d else 0


def float_or_zero(x):
	""" función que fuerza valor a float, de lo contrario --> 0 """
	# TODO: sospecho que sobra el True de esta if condition, algún dia probar
	y = float(x) if isinstance(x,Number)==True else 0
	return round(y,2)


def float_or_None(x):
	""" función que fuerza valor a float, de lo contrario --> o None"""
	if isinstance(x,Number):
		y = float(x)
		return round(y,2)
	else:
		return None



def round_conv_basis(x):
	""" redondea BASIS convención pantallas brokers. aproxima el 1er decimal a "0" o "5"
	 y esquiva los nan's.
 :type x: float
 :returns: number as string """

	y = (5 * round(x/5,1)) if isinstance(x,Number)==True else x
	return y


def round_2d(x):
	""" redondea a dos decimales, y esquiva los nan
 :type x: float
	"""

	y = round(x,2) if isinstance(x,Number)==True else x
	return y



def comp_a_z(dias,i_c,periodicity=182.5):
	""" transforma tasa compuesta --> a tasa zero (a.k.a simple)
	... ver su función inversa: z_a_comp mas abajo ...
	:param
		dias: int, dias de carry efectivo
		i_c: tasa compuesta base 360. i.e 2.85 (notar que 0.0285 NO)
		peridiocity: int, frecuencia de la composición. i.e. 180 dias
	:return:
		tasa zero (tasa simple act/360) """
	if dias <= periodicity:
		return i_c

	i_c = i_c/100
	f = 360 / periodicity

	return 100 * ( ( (1+i_c/f)**(f*dias/360) )-1 ) * 360/dias



def z_a_comp(dias,i_z,periodicity=182.5):
	""" transforma tasa zero (a.k.a simple) --> a compuesta
	... ver su función inversa: comp_a_z mas arriba ...
	:param
		dias: int, dias de carry efectivo
		i_z: tasa zero (tasa simple act/360)
		peridiocity: int, frecuencia de la composición. i.e. 180 dias
	:return:
		tasa compuesta base 360. i.e 2.85 (notar que 0.0285 NO) """
	if dias <= periodicity:
		return i_z

	i_z = i_z/100
	f = 360 / periodicity

	return 100 * f * ( (1+i_z*dias/360)**(360/(f*dias)) -1 )



def iptos(t,spot,iusd,icam,b,tcs,comp=True):
	"""
	funcion que calcula ptos fwd teoricos en función de BASIS y swaps convención COMPUESTA.
	detalles: ver formulario.

	t: tenor en numero de dias
	spot:
	irsusd:
	pesocam:
	b: basis en convención, por eso lo divido por 10000
	tresconseis: en convención, por eso lo divido por 10000
	comp: boolean. i.e. True if return is compounded rate (not simple rate)

	return: iptos
	"""
	iusd = float(iusd)/100
	icam = float(icam)/100
	b    = float(b)/10000
	tcs  = float(tcs)/10000

	t = float(t) / 182.5 # son cupones semestrales

	if comp: # función para caso tasa compuesta
		return spot*(  ((1+icam/2)**t) / ((1+(b+iusd+tcs)/2)**t)  -1 )

	return print('hacer función tasa simple')



def ibasis(t,spot,iusd,icam,ptos,tcs,comp=True):
	"""
	funcion que calcula basis teorico en función de puntos y swaps convención COMPUESTA.
	detalles: ver formulario.

	t: tenor en numero de dias
	spot:
	irsusd:
	pesocam:
	ptos
	tresconseis
	comp: boolean. i.e. True if return is compounded rate (not simple rate)

	return: ibasis
	"""
	iusd = iusd/100
	icam = icam/100
	tcs  = tcs/10000

	if comp==False:
		return print('hacer función tasa simple')

	t = t/182.5  # son cupones semestrales

	return 10000* (((   (spot/(spot+ptos))**(1/t) )*  (1+icam/2)-1)*2-iusd-tcs  )



def cam_os_simp(dias,spot,ptos,iusd,comp=True):
	""" funcion que calcula tasa camara off-shore, convención simple.
	detalles: ver formulario.

	:param
		dias: int, tenor en numero de dias
		spot: float, usdclp fx spot rate
		iusd: tasa fija swap libor, convención cupones semestrales
		ptos: float, puntos forward
		comp: boolean. i.e. True if return is compounded rate (not simple rate), false if zero rate
	:return:
		camara off shore
	"""
	if dias==0:		# si carry_dias es cero --> return: iusd
		return iusd
	if np.isnan(ptos): 	# si ptos=nan... evalualos cero, para que siga la formula...
		ptos=0

	iusd = iusd/100

	# transforma tasa compuesta a --> tasa simple
	if comp==False:
		iusd= comp_a_z(dias=dias, i_c= iusd)

	return 100 * ( ( (spot+ptos)/spot )  *  (1+iusd*dias/360) -1) *360/dias


def cam_lcl_a_os(dias,spot,ptos,iusd):
	""" funcion que, a partir de la tasa zero camara local, calcula la
	tasa zero camara off shore

	:param:
		dias: int, tenor en numero de dias
		spot: float, usdclp fx spot rate
		iusd: tasa fija swap libor, convención cupones semestrales
		ptos: float, puntos forward
		comp: boolean. i.e. True if return is compounded rate (not simple rate), false if zero rate
	:return:
		tasa zero camara off shore
	"""
	if dias==0:
		return iusd

	iusd = iusd/100

	return 100 * ( ( (spot+ptos)/spot )  *  (1+iusd*dias/360) -1) *360/dias



def fra1m(d_c,ispot_c,d_l,ispot_l,interp=False):
	"""
	d_c: dias tasa corta
	ispot_c: valor tasa spot, corto plazo
	interp: boolean, FRA heuristica interpolacion plazos sin tenor de mercado
	output: tasa fra"""

	ispot_c = ispot_c/100
	ispot_l = ispot_l / 100

	if interp: # if interpolate is True ---> FRA heuristica interpolacion plazos sin tenor de mercado
		meses= (d_l-d_c)/30
		return 100* ( ((1+ispot_l*d_l/360) / (1+ispot_c*d_c/360))**(1/meses) - 1 ) * 360 / 30

	return 100* ( (1+ispot_l*d_l/360) / (1+ispot_c*d_c/360) - 1 ) * 360 / (d_l - d_c)




def fra1m_v2(df,interp=False):
	"""
	DEPRECATED...usar fra1w_v en su lugar. fra 1 semana vectorizada

	Función calcula tasa FRA vectorizada, dataframe pandas
	:param:
		df: dataframe nombres cols: tenor, carry_days, icam_os
			d_c: dias tasa corta
			ispot_c: valor tasa spot, corto plazo
			interp: boolean, FRA heuristica interpolacion plazos sin tenor de mercado
	:return:
		Series tasa fra """

	y = pd.Series(index=df.index)

	d0 = df.carry_days.shift(1)
	x0 = df.icam_os.shift(1)

	d1 = df.carry_days
	x1 = df.icam_os

	if interp:
		meses = (d1 - do) / 30
		y = 100 * (((1 + xq * d1 / 36000) / (1 + x0 * d0 / 36000)) ** (1 / meses) - 1) * 360 / 30
	else:
		y = 100* ( (1+x1*d1/36000) / (1+x0*d0/36000) - 1 ) * 360 / (d1 - d0)

	y[df.carry_days<45] = float('nan')
	y[df.tenor=='1m'] = df.icam_os[df.tenor=='1m']

	return y.values



def fra1w(w2,w1,i2,i1):
	""" Función Calcula tasas FRA de 1 semana. Entre plazos que la distancia
	sea > 1 semana --> promedio compuesto de fra's.
	:param
		w2: Series of int, numero de SEMANAS asociada a la tasa zero, larga
		w1: Series of int, numero de SEMANAS asociada a la tasa zero, corta
		i2: Series of floats, same lenght, tasa de interés en base 360, x100... i.e. 2.89, larga
		i1: Series of floats, same lenght, tasa de interés en base 360, x100... i.e. 2.89, corta
	:return:
		Series of floats, tasas de interés FRA 1 semanal. """
	return 5200*(( ((1+i2/5200)**w2) / ((1+i1/5200)**w1) )**(1/(w2-w1)) - 1 )



def fra1w_v(df):
	""" Función Calcula, vectorizado, tasas FRA de 1 semana. Entre plazos que la distancia
	sea > 1 semana --> promedio de fra's.
	:param:
		df: dataframe que contiene estas dos cols:
			tenor: Series of strings, nombre del tenor asociada a la tasa --> se traduce en # weeks
			icam_os: Series of floats, same lenght, tasa de interés en base 360, x100... i.e. 2.89
	:return:
		Series of floats, tasas de interés FRA 1 semanal. """

	# w = {'TOD':0,'TOM':0,'1w':1,'2w':2,'1m':4,'2m':8,'3m':12,'4m':16,'5m':20,'6m':24,
	# 			  '9m':36,'12m':48,'18m':72,'2y':96}
	df.rename({df.columns[0]:'d',df.columns[1]:'i'},axis='columns',inplace=True)
	df['w'] = df.d / 7
	df['w_1'] = df.w.shift(1)
	df['i_1'] = df.i.shift(1)

	# 1yr tiene 52 semanas
	y = 5200*(( ((1+df.i/5200)**df.w) / ((1+df.i_1/5200)**df.w_1) )**(1/(df.w-df.w_1)) - 1 )
	y.loc[0:1] = df.i.loc[0:1].copy()
	return y



def curva_zero(dias, tasas, p):
	""" función que crea curva zero a partir de inputs en formato listas
	dias: list i.e. [1, 3, 7, 180, 3000]
	tasas: list i.e. [2.75, 2.85, 2.95, 3.00, 3.01]
	p: convencion peridiocidad, list i.e ['s', 's', 180, 180, 180] # simples o compuesta semestral
	"""

	# store in dataframe
	df = pd.DataFrame([dias, tasas, p]).T
	df.columns = ['d', 'i', 'p']

	# la tasas que ya son simples, solo las copia en col zero
	df['izero'] = df[df.conv == 's'].i

	# tasas compuestas... transformalas.. --> a simple
	df.loc[df.conv==p, ['izero']] = df[df.conv==p].apply(lambda x: comp_a_z(x.d, x.i, periodicity=p), axis=1)

	# calcula factores de descuento
	df['discf'] = df.apply(lambda x: 1 / (1 + (x.izero / 3600) * x.d), axis=1)

	return df[['d', 'izero', 'discf']]



def rank_perc(x,array):
	""" función calcula el ranking / 100 de el valor de x en un array
	:param:
		x: float or int
		array: np.array of numbers
	:return:
		float, el ranking sobre 100 """
	return int(100 * sum(x > array) / len(array))



def tables_init(fec0,fec1):
	""" función importa data del batch, para crear los df de table1
	con la data que se inicilizan al iniciar la app
	:param:
		fec0: Timestamp, dia de batch fec0, (un dia antes del dia de uso)
		fec1: Timestamp, dia de batch fec1, (dia de uso calculadora)
	:return: df1 """

	tenors = ['TOD', 'TOM', '1w', '2w'] + [str(x) + 'm' for x in range(1, 6 + 1)]+ ['9m',
				'12m', '18m'] + [str(x) + 'y' for x in range(2, 10 + 1)]

	cols1 = ['ind', 'tenor', 'daysy', 'days', 'carry_days', 'ptosy', 'ptos',
	       'odelta', 'ddelta', 'carry', 'icam','icamz', 'ilib','ilibz', 'tcs', 'icam_osz','icam_os',
	       'fracam_os','basisy', 'basis', 'i_ptos', 'i_basis']

	df = pd.DataFrame(index=range(0,len(tenors)),columns=cols1)

	df['ind']   = df.index.values
	df['tenor'] = tenors


	""" SPOT INICIO """ # TODO: aqui cambié el spot
	# df.odelta[0] = pd.read_pickle("./batch/p_clp_spot.pkl")[-1]
	spot = pd.read_pickle("./batch/p_clp_spot.pkl")[-1]


	""" PUNTOS FORWARD fec0 y fec1 """
	# pub days fecha batch
	_ = (fcc.crea_cal_tenors(fec0).pub - fec0).apply(lambda x: x.days)
	df['daysy'] = _[_.index.isin(tenors)].values

	# pub days batch + 1 = fecha de uso GMI
	_ = (fcc.crea_cal_tenors(fec1).pub - fec1).apply(lambda x: x.days)
	df['days'] = _[_.index.isin(tenors)].values

	df['carry_days'] = df.days - int(df.days[0])

	# voy a buscar los puntos de ayer al pickle, para ponerlos en el df de hoy
	pik_ptos = pd.read_pickle("./batch/p_ptos.pkl")

	# calculo ptos hoy breakeven, par iniciar la mañana con los plazos nuevos y la curva corecta
	_ = pik_ptos[fec0][['carry_days','ptos']].dropna()
	tenor_pts = _.index
	df['ptosy'][df.tenor.isin(tenor_pts)] = np.interp(x=df[df.tenor.isin(tenor_pts)].carry_days,
													  xp=_.carry_days,fp=_.ptos.map(float)).round(2)
	df.loc[1,'ptosy'] = round(np.interp(x=df.loc[1,'days'],xp=_.carry_days,fp=_.ptos.map(float)) ,2)

	df['ptos'] = df.ptosy.copy()

	df[1:].odelta = df[1:].ptos - df[1:].ptosy


	""" ICAM """
	pik_cam = pd.read_pickle("./batch/p_icam.pkl")
	df['icam'] = np.interp(x=df.carry_days,xp=pik_cam[fec0].carry_dias,fp=pik_cam[fec0].icam).round(2)
	df['icamz'][:13] = df['icam'][:13].values
	df['icamz'][13:] = df[13:].apply(lambda x: comp_a_z(x.days,x.icam,periodicity=182.5),axis=1)


	""" ILIB """
	pik_ilib = pd.read_pickle("./batch/p_ilib.pkl")
	df['ilib'] = np.interp(x=df.carry_days,xp=pik_ilib[fec0].carry_dias,fp=pik_ilib[fec0].ilib).round(2)
	df['ilibz']= df.apply(lambda x: comp_a_z(x.days,x.ilib,periodicity=91.25),axis=1)


	""" TRES CON SEIS """
	pik_bt = pd.read_pickle("./batch/p_basis_tcs.pkl")
	df['tcs'].loc[9:] = np.interp(x=df.days[9:],xp=pik_bt[fec0]['6m':'10y'].carry_dias,fp=pik_bt[fec0]['6m':'10y'].tcs.map(float)).round(3)


	""" CALCULO icam_osz , icam_os : primero tasa zero cupon --> después la paso a convención! """
	df['icam_osz'] = df.apply(lambda x: cam_os_simp(dias=x.carry_days,spot=spot,ptos=x.ptos,iusd=x.ilibz),axis=1)
	df['icam_os'][:13] = df['icam_osz'][:13]
	df['icam_os'][13:] = df[13:].apply(lambda x: z_a_comp(x.carry_days,x.icam_osz),axis=1)


	""" CALCULO 	fracam_os, desde icam-os convención mercado... """
	df['fracam_os'] = fra1w_v(df[['carry_days','icam_os']])


	""" BASIS """
	df = df.join(pik_bt[fec0].basis.rename('basisy'), on='tenor',rsuffix='_other')
	df['basisy']= df.basisy_other.map(round_conv_basis) # redondeo convencion basis
	df['basis'] = df.basisy.copy()
	df.drop(labels=['basisy_other'],axis=1,inplace=True)

	return df
# fec0, fec1 = pd.Timestamp(2019,7,18) , pd.Timestamp(2019,7,19)
# tables_init(fec0,fec1)


def update_calc_fx(rows):
	""" Función que crea & calcula calculadora de puntos fwds
	:param: rows
	:return:
	"""

	fra = pd.read_json(rows, orient='index')

	# voy a buscar en la fra -de hoy- asociada a los plazos "short" y "long"
	x = pd.to_numeric(dfc.loc[0:1, 'pub_days'].values, errors='coerce')
	dfc.loc[0:1, 'fra'] = np.interp(x=x, xp=fra['days'].values, fp=fra['fracam_os'].values)


	""" evaluo la 'fra input' respecto a la curva de hoy de la fra: 1-365 +18m+24m son 367 plazos
	son los plazos "operables" en el mercado """
	plazos = np.array([x for x in range(1,366)] + [fra['days'][12],fra['days'][13]])

	fra_todas = np.interp(x=plazos, xp=fra['days'].values, fp=fra['fracam_os'].values)

	df.loc[0:1,'fra_rank_hoy'] = df.loc[0:1].apply(lambda x: rank_perc(x.fra, fra_todas), axis=1)

	# TODO: evaluar la 'fra input' respecto a la historia de un año de su mismo plazo

	return df



def spreads_finder(range_days, gap, icamos,fec):
	"""	función para segmentar la curva a los spreads potenciales a analizar.
	Busca las tuplas de plazos compatibles de acuerdo a las restricciones explicitadas.
	:param:
		fec1: pd.Timestamp: la fecha de uso GMI (para filtrar feriados)
		range_days: iterable i.e (7,45), segmento de la curva a analizar: pub days min,max,
		gap: iterable (2,10) restringe la estensión min,max de los spreads a analizar
		icamos: df con index = dias publish 1-370 y 'icamos' = la tasa fra asociada a ese dia
	:return: dataframe cols: "dia corto, dias largo, fra implicita en el spread" 	"""
	l = list(permutations(range(range_days[0], range_days[1] + 1), 2))
	df = pd.DataFrame(l, columns=['short', 'long'])

	df = df[df.long > df.short]
	df = df[(df.long - df.short <= gap[1]) & (df.long - df.short >= gap[0])]

	# re index los dias que faltan, e interpola.
	aux = np.interp(x=np.arange(1,376,1,int), xp=icamos.index.values,fp=icamos.values)

	icamos = icamos.reindex(np.arange(1,376,1,int), fill_value=np.nan)
	icamos = pd.Series(aux,index=icamos.index,name='icamos')

	# slice de solo las fra's que voy a necesitar, segun la consulta
	icamos = icamos[icamos.index.isin(range(range_days[0], range_days[1] + 1))]

	# crea fechas para correr filtros dias inhabiles
	df['date_short'] = df.apply(lambda x: fec+pd.DateOffset(days=int(x.short)),axis=1)
	df['date_long']  = df.apply(lambda x: fec+pd.DateOffset(days=int(x.long)), axis=1)

	# filtro fines de semana
	df['date_s'] = df.date_short.apply(lambda x: x.dayofweek)
	df['date_l'] = df.date_long.apply(lambda x: x.dayofweek)
	df = df[(df.date_s< 5) & (df.date_l < 5)] # sab,dom son 5,6 cueck...

	# filtro feriados
	df = df[~df.date_short.isin(fcc.h_stgo_or_ny.to_list())]
	df = df[~df.date_long.isin( fcc.h_stgo_or_ny.to_list())]

	#calculo spreads
	df['days'] = df.apply(lambda x: str(x.short) + 'x' + str(x.long), axis=1)

	# merge plazos con icamos...
	df = df.merge(icamos, how='left', left_on='short', right_index=True)
	df = df.merge(icamos, how='left', left_on='long', right_index=True)
	df = df.rename(columns={df.columns[-2]: 'i1', df.columns[-1]: 'i2'})

	# calcula fra implicita en el spread
	df['i_rate'] = fra1w(w2=df.long, w1=df.short, i2=df.i2, i1=df.i1)
	df['i_rate'] = df.i_rate.round(2)

	# rankea los spread
	df.sort_values(by=['i_rate'], inplace=True)

	# slice los spread más baratos
	cheap = df[['days', 'i_rate']][:10]

	# slice los spread más caros
	rich = df[['days', 'i_rate']][-10:].sort_values(by=['i_rate'], ascending=False)

	return {'cheap': cheap, 'rich': rich, 'num_s':len(df)}


def suelto_finder(range_days,icamos,valuta,fec):
	"""	función para segmentar la curva a los spreads potenciales a analizar.
	Busca las tuplas de plazos compatibles de acuerdo a las restricciones explicitadas.
	:param:
		fec1: pd.Timestamp: la fecha de uso GMI (para filtrar feriados)
		range_days: iterable i.e (7,45), segmento de la curva a analizar: pub days min,max,
		gap: iterable (2,10) restringe la estensión min,max de los spreads a analizar
		icamos: df con index = dias publish 1-370 y 'icamos' = la tasa fra asociada a ese dia
	:return: dataframe cols: "dia corto, dias largo, fra implicita en el spread" 	"""

	l = np.arange(range_days[0],range_days[1]+1,1,int)
	df = pd.DataFrame(l,columns=['days'])
	df['carry_days'] = df.days - valuta

	df['i_rate'] = np.interp(x=df.carry_days, xp=icamos.index.values,fp=icamos.values).round(2)

	# crea fechas para correr filtros dias inhabiles
	df['date'] = df.apply(lambda x: fec+pd.DateOffset(days=int(x.days)),axis=1)

	# filtro fines de semana
	df['date_s'] = df.date.apply(lambda x: x.dayofweek)
	df = df[(df.date_s< 5)] # sab,dom son 5,6 cueck...

	# filtro feriados
	df = df[~df.date.isin(fcc.h_stgo_or_ny.to_list())]

	#calculo nombre producto TODO: aqui voyyyyy !!!!!
	df['days'] = df.apply(lambda x: str(x.days)+'d', axis=1)

	# rankea los spread
	df.sort_values(by=['i_rate'], inplace=True)

	# slice los spread más baratos
	cheap = df[['days', 'i_rate']][:10]

	# slice los spread más caros
	rich = df[['days', 'i_rate']][-10:]

	return {'cheap': cheap, 'rich': rich}

