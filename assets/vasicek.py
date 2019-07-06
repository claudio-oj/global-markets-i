
""" Crea Vasicek backwrds paths --> para fra_history.csv"""

import pandas as pd

def vasicek_rand_path(rate_ini=0.028, fec_ini='02-01-2018', fec_fin='25-02-2019', lt_level=0.03, speed=0.1, vol=0.004):

	""" crea serie de tiempo dummy de cada fra, de acuerdo a un proceso de drift & diffusion:
	  Vasicek
	  https://en.wikipedia.org/wiki/Vasicek_model

	  returns: pd.Series con datetime index.
	  """

	import pandas as pd
	pd.set_option('mode.chained_assignment', None)

	import numpy as np
	from dateutil import parser

	fec_ini = parser.parse(fec_ini)
	fec_fin = parser.parse(fec_fin)

	dates_range = pd.date_range(start=fec_ini, end=fec_fin)

	N  = len(dates_range)
	dt = 1 / N

	index = pd.RangeIndex(start=0, stop=N, step=1)
	df = pd.DataFrame(index=index)

	df['date'] = dates_range
	df['time'] = df.index / len(index)
	df['rand'] = np.random.randn(len(index))
	df['dr'] = None
	df['r_t'] = float(rate_ini)

	for i in range(0, len(df) - 1):
		df.dr[i + 1] = speed * (lt_level - df.r_t[i]) * dt + (dt ** (0.5)) * vol * df.rand[i + 1]
		df.r_t[i + 1] = df.dr[i + 1] + df.r_t[i]

	# dá vuelta los valores
	df['r_t_bckwrds'] = df.r_t[::-1].values
	return df['r_t_bckwrds']


""" RUN SCRIPT """

# curva FRA actual
fra_curve = {'1m':0.0274,'2m':0.027,'3m':0.0285,'4m':0.029,'5m':0.0276,'6m':0.0283,
			 '9m':0.028,'12m':0.0266,'18m':0.0264,'2y':0.029}

fec_ini='02-01-2018'
fec_fin='25-02-2019'

dates_range = pd.date_range(start=fec_ini, end=fec_fin)

df = pd.DataFrame(index=dates_range, columns= [*fra_curve] )

for name,rate_ini in zip(df.columns, fra_curve.values()):
	df[name] = vasicek_rand_path(rate_ini=rate_ini,speed=0.5, vol=0.002).values
	print(name,rate_ini)

# re ordena las columna para que date sea la primera
df['date'] = df.index.copy()
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]

df.to_csv('fra_history.csv')