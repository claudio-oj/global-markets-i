""" funciones calculan calendario convenciones de mercado """

import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np

# df feriados
df_h = pd.read_excel('batch/feriados_base_datos.xlsx', parse_dates=[0])

h_stgo_or_ny = df_h[(df_h.holiday_STGO == True) | (df_h.holiday_NY == True)]['date']
h_stgo = df_h[df_h.holiday_STGO == True]['date']
h_ny = df_h[df_h.holiday_NY == True]['date']
h_both = df_h[(df_h.holiday_STGO == True) & (df_h.holiday_NY == True)]['date']



def next_cal_day(d0, offset):
	""" calcula dias calendario, incluyendo calendario de feriados STGO !!!
	para estimar el 1w y el 2w """

	d1 = d0 + pd.DateOffset(offset)

	if d1 in h_stgo:
		d2 = d1 + pd.tseries.offsets.CustomBusinessDay(1, holidays=h_stgo)
		return d2

	else:
		return d1


def next_lab_settle(d0, offset, cal_spot=False, cal_cl=False, cal_ny=False):
	""" calcula el dia laboral siguiente, segun calendarios de feriados
	d: pandas timestamp
	cal_spot, cal_ndf: boolean"""

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
	le sumo 30 dias a d0. Si es feriado le sumo un día, si ese dia cambió de mes --> le resto días tal que
	quedemos en el business month end.

	d0: starting date
	m: # of months offset
	"""
	if d0 is None:
		return None

	d1 = d0 + pd.DateOffset(months=m)  # le sumo un mes exacto

	if d1.weekday() in [6, 7]:  # si cae fin de semana, dame el siguiente dia habil
		d2 = next_lab_settle(d1, 1, cal_spot=True)
	else:
		d2 = d1

	# end of month rule
	if d2.month != d1.month:
		d3 = d0 + pd.tseries.offsets.CustomBusinessMonthEnd(m, holidays=h_both)
	else:
		d3 = d2

	return d3


def crea_cal_tenors(tod):

	# tod = pd.Timestamp(2019,7,4)

	# df feriados
	# df_h = pd.read_excel('batch/feriados_base_datos.xlsx', parse_dates=[0])
	#
	# h_stgo_or_ny = df_h[(df_h.holiday_STGO == True) | (df_h.holiday_NY == True)]['date']
	# h_stgo       = df_h[df_h.holiday_STGO == True]['date']
	# h_ny         = df_h[df_h.holiday_NY == True]['date']
	# h_both       = df_h[(df_h.holiday_STGO == True) & (df_h.holiday_NY == True)]['date']


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
	 '11m', '12m', '13m', '14m', '15m', '16m', '17m', '18m', '24m', '30m', '3yrs', '3.5yrs',
	 '4yrs', '4.5yrs', '5yrs', '5.5yrs', '6yrs', '6.5yrs', '7yrs', '7.5yrs', '8yrs', '8.5yrs',
	 '9yrs', '9.5yrs', '10yrs', '10.5yrs', '11yrs', '11.5yrs', '12yrs', '12.5yrs', '13yrs',
	 '13.5yrs', '14yrs', '14.5yrs', '15yrs', '15.5yrs', '16yrs', '16.5yrs', '17yrs', '17.5yrs',
	 '18yrs', '18.5yrs', '19yrs', '19.5yrs', '20yrs'],
					   columns=['pubdays','fix','pub','val','tenor_s'])

	df3['tenor_s'] = np.arange(1,18+1).tolist() + np.arange(24,240+1,6).tolist()

	df3['val'] = df3.apply(lambda x: settle_rule(tod_v,x.tenor_s), axis=1)

	df3['fix'] = df3.apply(lambda x: next_lab_settle(x.val,-2,cal_spot=True), axis=1)

	df3['pub'] = df3.apply(lambda x: next_lab_settle(x.fix, 1,cal_cl=True), axis=1)

	df = pd.concat([df1,df2,df3])

	df.pubdays = (df.pub - tod).apply(lambda x: x.days)

	df['carry_days'] = ( df.pub - df.pub[0] ).apply(lambda x: x.days)

	return df
