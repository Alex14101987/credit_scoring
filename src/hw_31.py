# Подскажите, пожалуйста, почему эта строка выдает только NaN?
# bureau['CREDIT_CURRENCY'] = df12['data.record.AmtCredit'].str['CREDIT_CURRENCY']

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

# путь к лог.файлу
path_log = 'POS_CASH_balance_plus_bureau-001.log'
# пути к двум CSV.файлам
path_bureau = 'bureau.csv'
path_POS_CASH_balance = 'POS_CASH_balance.csv'

def main(path_log: str, path_bureau: str, path_POS_CASH_balance: str) -> pd.DataFrame:
    start_time = time.time()

    uploaded = path_log

    log_list = []

    with open(uploaded, 'r') as file:
        for line in file:
            #         print(line)
            log_list.append(line)

    x = log_list[45052]  # экономим время 1716501
    log_list = random.sample(log_list, 17165)  # экономим время 1716501
    log_list.append(x)  # экономим время 1716501

    df = pd.DataFrame(log_list, columns=['log_list'])

    df['log_list'] = df['log_list'].apply(lambda x: json.loads(x))
    # print(df)
    # делим датафрейм, вытаскиваем отдельно логи для POS_CASH_balance

    df1 = df[df['log_list'].str['type'] != 'bureau']

    df11 = df[df['log_list'].str['type'] == 'bureau']

    df2 = pd.json_normalize(df1['log_list'])

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

    df3 = df2.explode('data.records')
    df3.reset_index(drop=True)
    df3 = normalize_column(df3.reset_index(drop=True), 'data.records')

    from dataclasses import dataclass

    @dataclass
    class PosCashBalanceIDs:
        SK_ID_PREV: int
        SK_ID_CURR: int
        NAME_CONTRACT_STATUS: str

    # Вот здесь почему-то не видит название колонки хотя оно есть
    print(df3.columns)
    df3['PosCashBalanceIDs'] = df3['PosCashBalanceIDs'].apply(lambda x: eval(x))

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

    df12 = pd.json_normalize(df11['log_list'])

    # df11['AmtCredit'] = df11['log_list'].str['data'].str['record'].str['AmtCredit']
    # for n in range(len(df11)):
    #     df11['AmtCredit'].loc[n] = eval(df11['AmtCredit'].loc[n])

    df12['data.record.AmtCredit'] = df12['data.record.AmtCredit'].apply(lambda x: eval(x))

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

    POS_CASH_balance.to_csv(path_POS_CASH_balance)
    bureau.to_csv(path_bureau)
    end_time = time.time()
    print("Execution time: ", (end_time - start_time) / 60, "mins")

main(path_log, path_bureau, path_POS_CASH_balance)