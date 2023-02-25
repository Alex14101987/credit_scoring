import json
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import time
import json
import random
import warnings
warnings.filterwarnings('ignore')
from dataclasses import asdict
from datetime import datetime, date
import io
import numpy as np
import pandas as pd

df = pd.read_csv('/kaggle/input/shiftlogs/bureau.csv')

bureau = pd.DataFrame()

bureau['SK_ID_CURR'] = df['SK_ID_CURR'].drop_duplicates()

bureau['Максимальная сумма просрочки'] = df.groupby('SK_ID_CURR').agg({'AMT_CREDIT_MAX_OVERDUE': ['max']})

bureau['Минимальная сумма просрочки'] = df.groupby('SK_ID_CURR').agg({'AMT_CREDIT_MAX_OVERDUE': ['min']})

bureau['Какую долю суммы от открытого займа просрочил'] = df.groupby('SK_ID_CURR')["AMT_CREDIT_MAX_OVERDUE"].sum() / df.groupby('SK_ID_CURR')["AMT_CREDIT_SUM"].sum()

bureau['Кол-во кредитов определенного типа'] = df.groupby('SK_ID_CURR')["CREDIT_TYPE"].count()

bureau['Кол-во просрочек кредитов определенного типа'] = df.groupby(['SK_ID_CURR', "CREDIT_TYPE"])["CREDIT_DAY_OVERDUE"].count()

bureau['Кол-во закрытых кредитов определенного типа'] = df.groupby(['SK_ID_CURR', "CREDIT_TYPE"])["DAYS_ENDDATE_FACT"].count()

bureau.to_csv('bureau.csv', index = False)