import pandas as pd
import funcs_calendario_co as fcc

df = pd.DataFrame(index=[0,1,2],columns=['name','pub_days','fix','pub','val','fra','fra_rank_hoy',
						   'fra_rank_hist'])

df.loc[0,'name':'pub_days'] = ['short-leg',7]
df.loc[1,'name':'pub_days'] = ['long-leg' ,30]
df.loc[2,'pub_days'] = df.loc[1,'pub_days'] - df.loc[0,'pub_days']

# voy a buscar en la fra -de hoy- asociada a los plazos "short" y "long"
