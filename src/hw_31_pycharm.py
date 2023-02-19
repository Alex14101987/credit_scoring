# %% [markdown]
# Скрипт работает, но долго. Примерно 100 минут на Kaggle. Узким местом являются циклы.
# 
# Подскажите, пожалуйста, почему эта строка выдает только NaN?
# bureau['CREDIT_CURRENCY'] = df12['data.record.AmtCredit'].str['CREDIT_CURRENCY']

# %% [code] {"execution":{"iopub.status.busy":"2023-02-18T07:57:54.432004Z","iopub.execute_input":"2023-02-18T07:57:54.432446Z","iopub.status.idle":"2023-02-18T07:57:54.441858Z","shell.execute_reply.started":"2023-02-18T07:57:54.432409Z","shell.execute_reply":"2023-02-18T07:57:54.440028Z"}}
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

start_time = time.time()

# %% [code] {"execution":{"iopub.status.busy":"2023-02-18T07:57:54.444802Z","iopub.execute_input":"2023-02-18T07:57:54.445433Z","iopub.status.idle":"2023-02-18T07:57:54.455564Z","shell.execute_reply.started":"2023-02-18T07:57:54.445348Z","shell.execute_reply":"2023-02-18T07:57:54.454199Z"}}
uploaded = '/kaggle/input/shiftlogs/POS_CASH_balance_plus_bureau-001.log'

# %% [code] {"execution":{"iopub.status.busy":"2023-02-18T07:57:54.457861Z","iopub.execute_input":"2023-02-18T07:57:54.458351Z","iopub.status.idle":"2023-02-18T07:58:11.885732Z","shell.execute_reply.started":"2023-02-18T07:57:54.458314Z","shell.execute_reply":"2023-02-18T07:58:11.884153Z"}}

log_list = []
posh_log_list = []

with open(uploaded, 'r') as file:
    for line in file:
        #         print(line)
        log_list.append(line)

x = log_list[45052]  # экономим время 1716501
log_list = random.sample(log_list, 17165)  # экономим время 1716501
log_list.append(x)  # экономим время 1716501

df = pd.DataFrame(log_list, columns=['log_list'])

# %% [code] {"execution":{"iopub.status.busy":"2023-02-18T07:58:11.889078Z","iopub.execute_input":"2023-02-18T07:58:11.889473Z","iopub.status.idle":"2023-02-18T07:58:12.087150Z","shell.execute_reply.started":"2023-02-18T07:58:11.889440Z","shell.execute_reply":"2023-02-18T07:58:12.085696Z"}}

df['log_list'] = df['log_list'].apply(lambda x: json.loads(x))

# %% [code] {"execution":{"iopub.status.busy":"2023-02-18T07:58:12.089304Z","iopub.execute_input":"2023-02-18T07:58:12.089762Z","iopub.status.idle":"2023-02-18T07:58:12.136226Z","shell.execute_reply.started":"2023-02-18T07:58:12.089724Z","shell.execute_reply":"2023-02-18T07:58:12.134869Z"}}
# делим датафрейм, вытаскиваем отдельно логи для POS_CASH_balance

df1 = df[df['log_list'].str['type'] != 'bureau']

df11 = df[df['log_list'].str['type'] == 'bureau']

# %% [code] {"execution":{"iopub.status.busy":"2023-02-18T07:58:12.137985Z","iopub.execute_input":"2023-02-18T07:58:12.138725Z","iopub.status.idle":"2023-02-18T07:58:12.191473Z","shell.execute_reply.started":"2023-02-18T07:58:12.138682Z","shell.execute_reply":"2023-02-18T07:58:12.189644Z"}}


df2 = pd.json_normalize(df1['log_list'])

df2


# %% [code] {"execution":{"iopub.status.busy":"2023-02-18T07:58:12.193528Z","iopub.execute_input":"2023-02-18T07:58:12.193907Z","iopub.status.idle":"2023-02-18T07:58:12.202209Z","shell.execute_reply.started":"2023-02-18T07:58:12.193866Z","shell.execute_reply":"2023-02-18T07:58:12.200847Z"}}
def normalize_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Заменяет колонку со словарем на несколько колонок.

    Имена новых колонок - ключи словаря
    Значения в новых колонок - значения по заданному ключу в словаре
    """
    return pd.concat(
        [
            df,
            pd.json_normalize(df[column]),
        ],
        axis=1
    ).drop(columns=[column])

# %% [code] {"execution":{"iopub.status.busy":"2023-02-18T07:58:12.204159Z","iopub.execute_input":"2023-02-18T07:58:12.204687Z","iopub.status.idle":"2023-02-18T07:58:12.283346Z","shell.execute_reply.started":"2023-02-18T07:58:12.204648Z","shell.execute_reply":"2023-02-18T07:58:12.281899Z"}}


df3 = df2.explode('data.records')
df3.reset_index(drop=True)
df3 = normalize_column(df3.reset_index(drop=True), 'data.records')

df3

# %% [code] {"execution":{"iopub.status.busy":"2023-02-18T07:58:12.287516Z","iopub.execute_input":"2023-02-18T07:58:12.288082Z","iopub.status.idle":"2023-02-18T07:58:12.297141Z","shell.execute_reply.started":"2023-02-18T07:58:12.288031Z","shell.execute_reply":"2023-02-18T07:58:12.295065Z"}}
# 

from dataclasses import dataclass


@dataclass
class PosCashBalanceIDs:
    SK_ID_PREV: int
    SK_ID_CURR: int
    NAME_CONTRACT_STATUS: str

# df3['PosCashBalanceIDs'] = df3['PosCashBalanceIDs'].apply(lambda x: [eval(doc) for doc in x])

# %% [code] {"execution":{"iopub.status.busy":"2023-02-18T07:58:12.299018Z","iopub.execute_input":"2023-02-18T07:58:12.299504Z","iopub.status.idle":"2023-02-18T07:58:12.398979Z","shell.execute_reply.started":"2023-02-18T07:58:12.299463Z","shell.execute_reply":"2023-02-18T07:58:12.396839Z"}}


df3['PosCashBalanceIDs'] = df3['PosCashBalanceIDs'].apply(lambda x: eval(x))

# for n in range(len(df3)):
#     df3['PosCashBalanceIDs'].loc[n] = eval(df3['PosCashBalanceIDs'].loc[n])

df3

# %% [code] {"execution":{"iopub.status.busy":"2023-02-18T08:19:23.866036Z","iopub.execute_input":"2023-02-18T08:19:23.866941Z","iopub.status.idle":"2023-02-18T08:19:23.927348Z","shell.execute_reply.started":"2023-02-18T08:19:23.866880Z","shell.execute_reply":"2023-02-18T08:19:23.925908Z"}}


POS_CASH_balance = pd.DataFrame()

# POS_CASH_balance["SK_ID_PREV"] = np.nan
# for n in range(len(df3)):
#     POS_CASH_balance['SK_ID_PREV'].loc[n] = df3['PosCashBalanceIDs'].loc[n].SK_ID_PREV
POS_CASH_balance['SK_ID_PREV'] = df3['PosCashBalanceIDs'].str['SK_ID_PREV']

# POS_CASH_balance["SK_ID_CURR"] = 0
# for n in range(len(df3)):
#     POS_CASH_balance['SK_ID_CURR'].loc[n] = df3['PosCashBalanceIDs'].loc[n].SK_ID_CURR
POS_CASH_balance['SK_ID_CURR'] = df3['PosCashBalanceIDs'].str['SK_ID_CURR']

POS_CASH_balance['MONTHS_BALANCE'] = df3['MONTHS_BALANCE']
POS_CASH_balance['CNT_INSTALMENT'] = df3['data.CNT_INSTALMENT']

POS_CASH_balance['CNT_INSTALMENT_FUTURE'] = df3['CNT_INSTALMENT_FUTURE']

# POS_CASH_balance["NAME_CONTRACT_STATUS"] = np.nan
# for n in range(len(df3)):
#     POS_CASH_balance['NAME_CONTRACT_STATUS'].loc[n] = df3['PosCashBalanceIDs'].loc[n].NAME_CONTRACT_STATUS
POS_CASH_balance['NAME_CONTRACT_STATUS'] = df3['PosCashBalanceIDs'].str['NAME_CONTRACT_STATUS']

POS_CASH_balance['SK_DPD'] = df3['SK_DPD']
POS_CASH_balance['SK_DPD_DEF'] = df3['SK_DPD_DEF']

POS_CASH_balance

# %% [code] {"execution":{"iopub.status.busy":"2023-02-18T07:58:12.456813Z","iopub.execute_input":"2023-02-18T07:58:12.457385Z","iopub.status.idle":"2023-02-18T07:58:12.464964Z","shell.execute_reply.started":"2023-02-18T07:58:12.457350Z","shell.execute_reply":"2023-02-18T07:58:12.463604Z"}}
# 

from dataclasses import dataclass


@dataclass
class AmtCredit:
    CREDIT_CURRENCY: str
    AMT_CREDIT_MAX_OVERDUE: float
    AMT_CREDIT_SUM: float
    AMT_CREDIT_SUM_DEBT: float
    AMT_CREDIT_SUM_LIMIT: float
    AMT_CREDIT_SUM_OVERDUE: float
    AMT_ANNUITY: float


# df['AmtCredit'] = df['AmtCredit'].apply(lambda x: [eval(doc) for doc in x])

# %% [code] {"execution":{"iopub.status.busy":"2023-02-18T07:59:54.685532Z","iopub.execute_input":"2023-02-18T07:59:54.686086Z","iopub.status.idle":"2023-02-18T07:59:55.067919Z","shell.execute_reply.started":"2023-02-18T07:59:54.686048Z","shell.execute_reply":"2023-02-18T07:59:55.066439Z"}}
df12 = pd.json_normalize(df11['log_list'])
df12

# %% [code] {"execution":{"iopub.status.busy":"2023-02-18T08:01:28.863207Z","iopub.execute_input":"2023-02-18T08:01:28.863647Z","iopub.status.idle":"2023-02-18T08:01:29.345730Z","shell.execute_reply.started":"2023-02-18T08:01:28.863614Z","shell.execute_reply":"2023-02-18T08:01:29.344374Z"}}


# df11['AmtCredit'] = df11['log_list'].str['data'].str['record'].str['AmtCredit']       
# for n in range(len(df11)):
#     df11['AmtCredit'].loc[n] = eval(df11['AmtCredit'].loc[n])

df12['data.record.AmtCredit'] = df12['data.record.AmtCredit'].apply(lambda x: eval(x))

# %% [code] {"execution":{"iopub.status.busy":"2023-02-18T08:10:16.523347Z","iopub.execute_input":"2023-02-18T08:10:16.523806Z","iopub.status.idle":"2023-02-18T08:10:16.560558Z","shell.execute_reply.started":"2023-02-18T08:10:16.523754Z","shell.execute_reply":"2023-02-18T08:10:16.559092Z"}}


bureau = pd.DataFrame()

bureau['SK_ID_CURR'] = df12['data.record.SK_ID_CURR']
bureau['SK_ID_BUREAU'] = df12['data.record.SK_ID_BUREAU']
bureau['CREDIT_ACTIVE'] = df12['data.record.CREDIT_ACTIVE']

# bureau["CREDIT_CURRENCY"] = np.nan
# for n in range(len(df11)):
#     bureau['CREDIT_CURRENCY'].loc[n] = df11['AmtCredit'].loc[n].CREDIT_CURRENCY
bureau['CREDIT_CURRENCY'] = df12['data.record.AmtCredit'].str['CREDIT_CURRENCY']

# bureau['DAYS_CREDIT'] = df12['log_list'].str['data'].str['record'].str['DAYS_CREDIT']
# bureau['CREDIT_DAY_OVERDUE'] = df12['log_list'].str['data'].str['record'].str['CREDIT_DAY_OVERDUE']
# bureau['DAYS_CREDIT_ENDDATE'] = df12['log_list'].str['data'].str['record'].str['DAYS_CREDIT_ENDDATE']
# bureau['DAYS_ENDDATE_FACT'] = df12['log_list'].str['data'].str['record'].str['DAYS_ENDDATE_FACT']

# # bureau["AMT_CREDIT_MAX_OVERDUE"] = np.nan
# # for n in range(len(df11)):
# #     bureau['AMT_CREDIT_MAX_OVERDUE'].loc[n] = df11['AmtCredit'].loc[n].AMT_CREDIT_MAX_OVERDUE

bureau['CNT_CREDIT_PROLONG'] = df12['log_list'].str['data'].str['record'].str['CNT_CREDIT_PROLONG']

# # bureau["AMT_CREDIT_SUM"] = np.nan
# # for n in range(len(df11)):
# #     bureau['AMT_CREDIT_SUM'].loc[n] = df11['AmtCredit'].loc[n].AMT_CREDIT_SUM

# # bureau["AMT_CREDIT_SUM_DEBT"] = np.nan
# # for n in range(len(df11)):
# #     bureau['AMT_CREDIT_SUM_DEBT'].loc[n] = df11['AmtCredit'].loc[n].AMT_CREDIT_SUM_DEBT

# # bureau["AMT_CREDIT_SUM_LIMIT"] = np.nan
# # for n in range(len(df11)):
# #     bureau['AMT_CREDIT_SUM_LIMIT'].loc[n] = df11['AmtCredit'].loc[n].AMT_CREDIT_SUM_LIMIT

# # bureau["AMT_CREDIT_SUM_OVERDUE"] = np.nan
# # for n in range(len(df11)):
# #     bureau['AMT_CREDIT_SUM_OVERDUE'].loc[n] = df11['AmtCredit'].loc[n].AMT_CREDIT_SUM_OVERDUE

bureau['CREDIT_TYPE'] = df12['log_list'].str['data'].str['CREDIT_TYPE']
bureau['DAYS_CREDIT_UPDATE'] = df12['log_list'].str['data'].str['record'].str['DAYS_CREDIT_UPDATE']

# # bureau["AMT_ANNUITY"] = np.nan
# # for n in range(len(df11)):
# #     bureau['AMT_ANNUITY'].loc[n] = df11['AmtCredit'].loc[n].AMT_ANNUITY

bureau

# %% [code] {"execution":{"iopub.status.busy":"2023-02-18T07:58:12.833012Z","iopub.execute_input":"2023-02-18T07:58:12.833847Z","iopub.status.idle":"2023-02-18T07:58:12.912838Z","shell.execute_reply.started":"2023-02-18T07:58:12.833728Z","shell.execute_reply":"2023-02-18T07:58:12.910826Z"}}
POS_CASH_balance.to_csv('POS_CASH_balance.csv')
bureau.to_csv('bureau.csv')
end_time = time.time()
print("Execution time: ", (end_time - start_time) / 60, "mins")