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