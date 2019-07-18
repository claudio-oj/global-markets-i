""" funciones calculan calendario convenciones de mercado """

import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np

# df feriados
df_h = pd.read_excel("./batch/feriados_base_datos.xlsx", parse_dates=[0])

h_stgo_or_ny = df_h[(df_h.holiday_STGO == True) | (df_h.holiday_NY == True)]['date']
h_stgo = df_h[df_h.holiday_STGO == True]['date']
h_ny = df_h[df_h.holiday_NY == True]['date']
h_both = df_h[(df_h.holiday_STGO == True) & (df_h.holiday_NY == True)]['date']

months_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep',
				   10: 'Oct', 11: 'Nov', 12: 'Dec'}



def next_cal_day(d0, offset):
	""" calcula siguiente dia habil, incluyendo calendario de feriados STGO
	para estimar el 1w y el 2w

	PARAMETERS:
		d0: pandas timestamp
		offset: int

	RETURNS:
			pandas timestamp: next_cal_day
	"""

	d1 = d0 + pd.DateOffset(offset)

	if d1 in h_stgo:
		d2 = d1 + pd.tseries.offsets.CustomBusinessDay(1, holidays=h_stgo)
		return d2

	else:
		return d1



def next_lab_settle(d0, offset, cal_spot=False, cal_cl=False, cal_ny=False):
	""" calcula el dia laboral siguiente, segun calendarios de feriados
	PARAMETERS:
		d: pandas timestamp
		offset: int
		cal_spot: boolean, intersección calendario holidays STGO & NY
		cal_cl: boolean, calendario holidays STGO
		cal_ny: boolean, calendario holidays NY
	RETURNS:
			next_lab_settle """

	# SPOT
	if cal_spot:
		return d0 + pd.tseries.offsets.CustomBusinessDay(offset, holidays=h_stgo_or_ny)

	# NDF entre locales, off shore, o cruzado.
	elif cal_cl:
		return d0 + pd.tseries.offsets.CustomBusinessDay(offset, holidays=h_stgo)

	elif cal_ny:
		return d0 + pd.tseries.offsets.CustomBusinessDay(offset, holidays=h_ny)

	else:
		return 'ajustar booleans'


def settle_rule(d0, m):
	"""settle calendar rule calculator, including end of month rule
	le sumo un mes a d0. Si cae feriado le sumo un día, si ese dia saltó al mes siguiente -->
	 le resto días tal que quedemos en el business month end.

	PARAMETERS:
		d0: pd.Timestamp, starting date
		m: int, # of months offset

	RETURNS:
		pd.Timestamp, settle day a partir de d0, m meses en adelante

	"""
	if d0 is None:
		return None

	d1 = d0 + pd.DateOffset(months=m)  # le sumo un mes exacto

	if d1.weekday() in [6, 7]:  # si cae fin de semana, dame el siguiente dia habil
		d2 = next_lab_settle(d1, 1, cal_spot=True)
	else:
		d2 = d1

	# end of month rule TODO: aqui sumé un 1 a m ... veremos...
	if d2.month != d1.month:
		d3 = pd.tseries.offsets.CustomBusinessMonthEnd(holidays=h_both).rollback(d1)
	else:
		d3 = d2

	return d3


def crea_cal_tenors(tod):
	""" función que crea calendario completo

	:param
		tod:
	:return:
		df calendario completo """

	# today's value date
	tod_v = next_lab_settle(tod,2,cal_spot=True)

	df1 = pd.DataFrame(index=['TOD', 'TOM'], columns=['pubdays','fix','pub','val','tenor_s'])



	""" La logica de calendario es que se comienza de fix date=HOY, luego fix y pub dates se fijan segun calendario STGO
	val dates se fija segun calendario conjunto STGO & NY"""

	df1['fix']['TOD'] = tod
	df1['pub']['TOD'] = next_lab_settle(tod,1,cal_cl=True)
	df1['val']['TOD'] = tod_v

	df1['fix']['TOM'] = next_lab_settle(tod,1,cal_cl=True)
	df1['pub']['TOM'] = next_lab_settle(df1['fix']['TOM'],1,cal_cl=True)
	df1['val']['TOM'] = next_lab_settle(df1['fix']['TOM'],2,cal_spot=True)


	""" para 1w, y 2w no aplica la regla "cambia mes". Aca se comienza a escribir a partir de HOY + tenor sugerido --> pub date """
	df2 = pd.DataFrame(index=['1w','2w'], columns=['pubdays','fix','pub','val','tenor_s']) # tenor_s: tenor sugerido

	df2['tenor_s'] = (7,14)
	df2['pub']     = df2.apply(lambda x: next_cal_day(tod, x.tenor_s), axis=1)
	df2['fix']     = df2['pub'].apply(lambda x: next_cal_day(x,-1))
	df2['val']     = df2['pub'].apply(lambda x: next_cal_day(x, 1))



	""" tenors sugeridos en base mensual, se calculan a partir de la fecha settle"""

	df3 = pd.DataFrame(index=['1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m', '10m',
		'11m', '12m', '13m', '14m', '15m', '16m', '17m', '18m', '2y', '2.5y', '3y', '3.5y',
		'4y', '4.5y', '5y', '5.5y', '6y', '6.5y', '7y', '7.5y', '8y', '8.5y', '9y', '9.5y',
		'10y', '10.5y', '11y', '11.5y', '12y', '12.5y', '13y','13.5y', '14y', '14.5y', '15y',
		'15.5y', '16y', '16.5y', '17y', '17.5y', '18y', '18.5y', '19y', '19.5y', '20y'],
					   columns=['pubdays','fix','pub','val','tenor_s'])

	df3['tenor_s'] = np.arange(1,18+1).tolist() + np.arange(24,240+1,6).tolist()

	df3['val'] = df3.apply(lambda x: settle_rule(tod_v,x.tenor_s), axis=1)

	df3['fix'] = df3.apply(lambda x: next_lab_settle(x.val,-2,cal_spot=True), axis=1)

	df3['pub'] = df3.apply(lambda x: next_lab_settle(x.fix, 1,cal_cl=True), axis=1)

	df = pd.concat([df1,df2,df3])

	df.pubdays = (df.pub - tod).apply(lambda x: x.days)

	df['carry_days'] = ( df.pub - df.pub[0] ).apply(lambda x: x.days)

	return df

y = crea_cal_tenors(pd.Timestamp(2019,7,8))


def crea_cal_IRS_us(d):
	""" CREA CALENDARIO DE TASAS US, sirve para irs usd, basis usdclp, y tcs
	:param:
		d: Timestamp, dia de calculo del calendario
	:return: df con el calendario crado """

	tenors_us = ['o/n','3m','6m','12m']+[str(x)+'y' for x in range(2,11)]+['12y','15y','20y','30y']
	meses_us  = [0,3,6]+[12*int(x) for x in range(1,11)]+[12*12,15*12,20*12,30*12]

	# df = pd.DataFrame(index=tenors_us, columns=['meses', 'val', 'carry_dias', 'ilib', 'ilib_z'])
	df = pd.DataFrame(index=tenors_us, columns=['meses', 'val', 'carry_dias'])

	# numero de meses para cada tenor
	df.meses = meses_us

	# fecha settle del tenor o/n
	df.val['o/n'] = next_lab_settle(d, 2, cal_ny=True)

	# fecha settle para los tenors largos en base al 1er settle
	df.val = df.apply(lambda x: settle_rule(df.val['o/n'], x.meses), axis=1)

	# calcula carry days en base al primer settle date
	df.carry_dias = (df.val - df.val[0]).apply(lambda x: x.days)
	return df


def date_output(fec1,pub):
	""" función que calcula los dias fix-pub-value en formato mercado fx
	:param:
		fec1: pd.Timestamp , fecha de hoy
		pub: int
	:return string """

	# pub date: fecha input usuario
	pub = fec1 + pd.DateOffset(pub)

	# fix date
	# fix = next_cal_day(pub, -1)
	fix = pub + pd.tseries.offsets.CustomBusinessDay(-1, holidays=h_stgo)

	# settle date
	val = next_lab_settle(fix, 2, cal_spot=True)

	if pub.day_name() in ['Saturday','Sunday']:
		return pub.day_name()

	elif fix in h_stgo.to_list() or pub in h_stgo.to_list():
		return 'stgo_holiday'

	else:
		return str(fix.day) + '-' + str(pub.day) + '-' + str(val.day) + ' ' + months_dict[val.month]
