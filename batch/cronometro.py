import pandas as pd
import time
from batch.crea_calendar_tenors import crea_cal_tenors
st=time.time()

for d in pd.date_range('01-07-2018','04-07-2019'):
	crea_cal_tenors(d)

print("----%.2f----"%(time.time()-st))

