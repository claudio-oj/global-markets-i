""" 
GM Insights, por Claudio Ortiz
python 3.6
"""

import os
import pandas as pd 
import numpy as np
from scipy import interpolate
from numbers import Number



def imp_spot():

	""" importa precio spot del closing de tradition """

	return pd.read_excel('Closing_Run_trad.xlsx',usecols='G:H',skiprows=1,nrows=1).mean(axis=1)[0]



def imp_calendar():
	""" importa dias calendario segun traductor trad.calypso """

	cal = pd.read_excel('Traductor tenors Tradition-Calypso.xlsm',sheet_name='calend local',skiprows=3,nrows =59,usecols ='B:C')
	cal.columns= ['name','days']

	botar= [10,11,13,14,16,17,18,19,20] +[x for x in range(23,38,2)] + [x for x in range(39,59,1)]
	cal= cal.loc[~cal.index.isin(botar)]

	return cal.days



def imp_clos_t():

	""" importa closing entero tradition"""

	# importa closing + formatea
	trad = pd.read_excel('Closing_Run_trad.xlsx', sheet_name='Hoja1', nrows=102, usecols='A:R')
	trad.index = np.linspace(0,100,101,dtype=int)
	trad.columns= ['col'+str(x) for x in range(0,17+1)]

	#set new df index
	tenors1= ['tod','tom','1w','2w'] + [str(x)+ 'm' for x in range(1,6+1)]
	tenors2= ['9m','12m','18m'] + [str(x)+'y' for x in range(2,10+1)]
	tenors = tenors1 + tenors2

	df= pd.DataFrame(index= range(0,len(tenors)), columns=['ind','tenor','daysy','days','carry_days','ptosy','ptos','odelta','ddelta',
														   'carry','icam','ilib','tcs','icam_os','fracam_os','basisy',
														   'basis','i_ptos','i_basis'])

	df['ind']= df.index.values
	df['tenor'] = tenors

	# TODO: eliminar la dependencia al archivo Traductor tenors Tradition-Calypso.xlsm
	df['daysy']= imp_calendar().values

	#calendario hoy
	# df['days'] = [1, 2, 7, 14, 30, 62, 93, 121, 154, 184, 274, 366, 549, 730, 1096, 1460, 1827, 2193, 2558, 2922, 3287, 3654]
	df['days'] = df.daysy.copy()

	df['carry_days'] = df.days - int(df.days[0])

	# import yesterday closing fwd points
	df['ptosy'].iloc[2:14]= trad.iloc[31:43,16].values

	#importa basis yesterday closing
	df['basisy'].iloc[11] = trad.iloc[58,4]  # 1yr
	df['basisy'].iloc[12] = trad.iloc[57,4] #18m
	df['basisy'].iloc[13:22]= trad.iloc[59:68,4].values # 2yr-10yrs

	return df



def live(col='icam'):

	"""
	https://stackoverflow.com/questions/32496062/how-can-i-interpolate-based-on-index-values-when-using-a-pandas-multiindex """

	""" importa closing entero tradition"""

	# importa closing + formatea
	trad = pd.read_excel('Closing_Run_trad.xlsx', sheet_name='Hoja1', nrows=102, usecols='A:R')
	trad.index = np.linspace(0, 100, 101, dtype=int)
	trad.columns = ['col' + str(x) for x in range(0, 17 + 1)]

	# set new df index
	tenors1= ['tod','tom','1w','2w'] + [str(x)+ 'm' for x in range(1,6+1)]
	tenors2= ['9m','12m','18m'] + [str(x)+'y' for x in range(2,10+1)]
	tenors = tenors1 + tenors2

	df = pd.DataFrame(index=range(0, len(tenors)),
					  columns=['ind', 'tenor', 'daysy', 'days', 'ptosy', 'ptos', 'odelta', 'ddelta',
							   'carry', 'icam', 'ilib', 'tcs', 'icam_os', 'fracam_os', 'basisy',
							   'basis', 'i_ptos', 'i_basis'])

	df['ind'] = df.index.values
	df['tenor'] = tenors

	# calendario yesterday
	df['daysy'] = imp_calendar().values

	# calendario hoy
	# df['days'] = [1, 2, 7, 14, 30, 62, 93, 121, 154, 184, 274, 366, 549, 730, 1096, 1460, 1827, 2193, 2558, 2922, 3287,
	#               3654]
	df['days'] = df.daysy.copy()


	# import icam live  desde la fuente: "yesterday closing " --> CAMBIAR EN EL FUTURO !!

	if col=='icam':
		df['icam'][df.tenor == 'tod'] = 3.00
		df['icam'][df.tenor == '3m' ] = 3.00
		for t,i in zip(df.tenor.iloc[9:22], range(11,24)):
			df['icam'][df.tenor == t] = trad.iloc[i, 12]
		df['icam'] = df['icam'].astype(float).interpolate(method='index')
		return df['icam'].round(2).values

	if col=='ilib':
		dfilib = pd.read_csv('ICESwapRateHistoricalRates.csv', header=None, index_col=0).squeeze()
		df['ilib'][df.tenor == 'tod'] = 2.38863
		df['ilib'][df.tenor == '3m' ] = 2.63863
		df['ilib'][df.tenor == '6m' ] = 2.69313
		df['ilib'][df.tenor == '12m'] = dfilib[0]
		df['ilib'][13:22] = dfilib[1:-3]
		df['ilib'] = df['ilib'].astype(float).interpolate(method='index')
		return df['ilib'].round(2).values






###############################################################################
###############################################################################

def float_or_zero(x):
	""" función que fuerza valor a float o zero"""
	y = float(x) if isinstance(x,Number)==True else 0
	return round(y,2)

# float_or_zero(2)


def weird_division(n, d):
	""" función división, que en el caso excepcional de dividir x cero --> 0"""
	return n / d if d else float('nan')




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

	t = t/180  # son cupones semestrales

	return 10000* (((   (spot/(spot+ptos))**(1/t) )*  (1+icam/2)-1)*2-iusd-tcs  )



def comp_a_z(dias,i_c,periodicity=180):
	""" transforma tasa compuesta --> a tasa zero (a.k.a simple)
	:param
		dias: int, dias de carry efectivo
		i_c: tasa compuesta base 360. i.e 2.85 (notar que 0.0285 NO)
		peridiocity: int, frecuencia de la composición. i.e. 180 dias
	:return:
		tasa zero (tasa simple act/360)
	"""
	if dias==0:
		return i_c

	i_c = i_c/100
	f = 360 / periodicity

	return 100 * ( ( (1+i_c/f)**(f*dias/360) )-1 ) * 360/dias



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


# df = pd.DataFrame([['1w',6,2.78],['2w',13,2.79],['1m',29,2.85],['2m',59,2.00],['3m',89,3.00]], columns= ['tenor','carry_days','icam_os'])
#
# fra1m_v2(df)


def fra1w(w2,w1,i2,i1):
	""" Función Calcula tasas FRA de 1 semana. Entre plazos que la distancia
	sea > 1 semana --> promedio de fra's.
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

	# w = {'tod':0,'tom':0,'1w':1,'2w':2,'1m':4,'2m':8,'3m':12,'4m':16,'5m':20,'6m':24,
	# 			  '9m':36,'12m':48,'18m':72,'2y':96}
	df['w'] = df.days / 7
	df['w_1'] = df.w.shift(1)
	df['icam_os_1'] = df.icam_os.shift(1)

	# 1yr tiene 52 semanas
	y = 5200*(( ((1+df.icam_os/5200)**df.w) / ((1+df.icam_os_1/5200)**df.w_1) )**(1/(df.w-df.w_1)) - 1 )
	y.loc[0:1] = df.icam_os.loc[0:1].copy()
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

