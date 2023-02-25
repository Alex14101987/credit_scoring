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

df = pd.read_csv('/kaggle/input/shiftlogs/credit_card_balance.csv')

# Для датафрейма credit_card_balance.csv посчитать следующие признаки:
# 	Посчитайте все возможные аггрегаты по картам.
# 	Посчитайте как меняются аггрегаты. например отношение аггрегата за все время к аггрегату за последние 3 месяца или к данных за последний месяц.
#     
# Денежные агрегаты – показатели структуры денежной массы (денежного предложения), виды денег и денежных средств, отличающиеся друг от друга степенью ликвидности, то есть возможностью быстрого превращения в наличные деньги. В разных странах используются разные определения денежных агрегатов.
# 
# В России Центральный банк рассчитывает три агрегата: M0, M1 и M2.
# 
# M0 включает только наличные деньги в национальной валюте в обращении вне банковской системы.
# 
# В M1 входит агрегат M0 и остатки средств в национальной валюте на расчетных, текущих и иных счетах до востребования населения, нефинансовых и финансовых (кроме кредитных) организаций, являющихся резидентами Российской Федерации.
# 
# В показатель M2 включается агрегат M1, а также остатки средств в национальной валюте на счетах срочных депозитов и иных привлеченных на срок средств населения, нефинансовых и финансовых (кроме кредитных) организаций, являющихся резидентами Российской Федерации.
# Подробнее на сайте Banki.ru https://www.banki.ru/wikibank/denejnyie_agregatyi/
# 
credit_card_balance = pd.DataFrame()

credit_card_balance['SK_ID_PREV'] = df['SK_ID_PREV'].drop_duplicates()

credit_card_balance['M0'] = df.groupby('SK_ID_PREV')["AMT_TOTAL_RECEIVABLE"].sum()

credit_card_balance['M1'] = df.groupby('SK_ID_PREV')["AMT_BALANCE"].sum()

credit_card_balance['M2'] = df.groupby('SK_ID_PREV')["AMT_CREDIT_LIMIT_ACTUAL"].sum()

credit_card_balance.to_csv('credit_card_balance.csv', index = False)