from datetime import datetime
from datetime import date

import pandas as pd
now = datetime.today().date()
# now = datetime.strptime('2018-01-15','%Y-%m-%d').date()
if(bool(len(pd.bdate_range(now,now)))):
    with open
