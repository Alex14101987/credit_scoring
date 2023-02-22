import json
import os
import numpy as np
import pandas as pd
from dataclasses import dataclass
import time
import json
import random
import warnings
warnings.filterwarnings('ignore')
from dataclasses import asdict

# путь к лог.файлу
path_log = 'POS_CASH_balance_plus_bureau-001.log'
# пути к двум CSV.файлам возвращаемым функцией main
path_bureau = 'bureau.csv'
path_POS_CASH_balance = 'POS_CASH_balance.csv'

# Пользовательские классы
@dataclass
class PosCashBalanceIDs:
    SK_ID_PREV: int
    SK_ID_CURR: int
    NAME_CONTRACT_STATUS: str


@dataclass
class AmtCredit:
    CREDIT_CURRENCY: str
    AMT_CREDIT_MAX_OVERDUE: float
    AMT_CREDIT_SUM: float
    AMT_CREDIT_SUM_DEBT: float
    AMT_CREDIT_SUM_LIMIT: float
    AMT_CREDIT_SUM_OVERDUE: float
    AMT_ANNUITY: float


# Заменяет колонку со словарем на несколько колонок.
def normalize_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    return pd.concat(
        [df,pd.json_normalize(df[column]),],
        axis=1
    ).drop(columns=[column])

# функция для обработки POS_Cash
def POS_CASH_balance_func(df_POS_CASH_balance: pd.DataFrame) -> pd.DataFrame:

    df_POS_CASH_balance = pd.json_normalize(df_POS_CASH_balance['log_list'])
    df_POS_CASH_balance = df_POS_CASH_balance.explode('data.records')
    df_POS_CASH_balance.reset_index(drop=True)
    df_POS_CASH_balance = normalize_column(df_POS_CASH_balance.reset_index(drop=True), 'data.records')
    df_POS_CASH_balance['PosCashBalanceIDs'] = df_POS_CASH_balance['PosCashBalanceIDs'].apply(lambda x: eval(x))
    POS_CASH_balance = pd.DataFrame()
    POS_CASH_balance['SK_ID_PREV'] = df_POS_CASH_balance['PosCashBalanceIDs'].apply(lambda x: x.SK_ID_PREV)
    POS_CASH_balance['SK_ID_CURR'] = df_POS_CASH_balance['PosCashBalanceIDs'].apply(lambda x: x.SK_ID_CURR)
    POS_CASH_balance['MONTHS_BALANCE'] = df_POS_CASH_balance['MONTHS_BALANCE']
    POS_CASH_balance['CNT_INSTALMENT'] = df_POS_CASH_balance['data.CNT_INSTALMENT']
    POS_CASH_balance['CNT_INSTALMENT_FUTURE'] = df_POS_CASH_balance['CNT_INSTALMENT_FUTURE']
    POS_CASH_balance['NAME_CONTRACT_STATUS'] = df_POS_CASH_balance['PosCashBalanceIDs'].apply(lambda x: x.NAME_CONTRACT_STATUS)
    POS_CASH_balance['SK_DPD'] = df_POS_CASH_balance['SK_DPD']
    POS_CASH_balance['SK_DPD_DEF'] = df_POS_CASH_balance['SK_DPD_DEF']

    return POS_CASH_balance

# функция для обработки bureau
def bureau_func(df_bureau: pd.DataFrame) -> pd.DataFrame:

    df_bureau = pd.json_normalize(df_bureau['log_list'])
    df_bureau['data.record.AmtCredit'] = df_bureau['data.record.AmtCredit'].apply(lambda x: eval(x))
    bureau = pd.DataFrame()
    bureau['SK_ID_CURR'] = df_bureau['data.record.SK_ID_CURR']
    bureau['SK_ID_BUREAU'] = df_bureau['data.record.SK_ID_BUREAU']
    bureau['CREDIT_ACTIVE'] = df_bureau['data.record.CREDIT_ACTIVE']
    bureau['CREDIT_CURRENCY'] = df_bureau['data.record.AmtCredit'].apply(lambda x: x.CREDIT_CURRENCY)
    bureau['DAYS_CREDIT'] = df_bureau['data.record.DAYS_CREDIT']
    bureau['CREDIT_DAY_OVERDUE'] = df_bureau['data.record.CREDIT_DAY_OVERDUE']
    bureau['DAYS_CREDIT_ENDDATE'] = df_bureau['data.record.DAYS_CREDIT_ENDDATE']
    bureau['DAYS_ENDDATE_FACT'] = df_bureau['data.record.DAYS_ENDDATE_FACT']
    bureau['AMT_CREDIT_MAX_OVERDUE'] = df_bureau['data.record.AmtCredit'].apply(lambda x: x.AMT_CREDIT_MAX_OVERDUE)
    bureau['CNT_CREDIT_PROLONG'] = df_bureau['data.record.CNT_CREDIT_PROLONG']
    bureau['AMT_CREDIT_SUM'] = df_bureau['data.record.AmtCredit'].apply(lambda x: x.AMT_CREDIT_SUM)
    bureau['AMT_CREDIT_SUM_DEBT'] = df_bureau['data.record.AmtCredit'].apply(lambda x: x.AMT_CREDIT_SUM_DEBT)
    bureau['AMT_CREDIT_SUM_LIMIT'] = df_bureau['data.record.AmtCredit'].apply(lambda x: x.AMT_CREDIT_SUM_LIMIT)
    bureau['AMT_CREDIT_SUM_OVERDUE'] = df_bureau['data.record.AmtCredit'].apply(lambda x: x.AMT_CREDIT_SUM_OVERDUE)
    bureau['CREDIT_TYPE'] = df_bureau['data.CREDIT_TYPE']
    bureau['DAYS_CREDIT_UPDATE'] = df_bureau['data.record.DAYS_CREDIT_UPDATE']
    bureau['AMT_ANNUITY'] = df_bureau['data.record.AmtCredit'].apply(lambda x: x.AMT_ANNUITY)

    return bureau


def main(path_log: str, path_bureau: str, path_POS_CASH_balance: str) -> pd.DataFrame:
    start_time = time.time()

    uploaded = path_log
    log_list = []

    with open(uploaded, 'r') as file:
        for line in file:
            log_list.append(line)

    # x = log_list[45052]  # экономим время 1716501
    # log_list = random.sample(log_list, 17165)  # экономим время 1716501
    # log_list.append(x)  # экономим время 1716501

    df = pd.DataFrame(log_list, columns=['log_list'])
    df['log_list'] = df['log_list'].apply(lambda x: json.loads(x))

    df_POS_CASH_balance = pd.DataFrame()
    df_POS_CASH_balance = df[df['log_list'].str['type'] != 'bureau']
    df_bureau = pd.DataFrame()
    df_bureau = df[df['log_list'].str['type'] == 'bureau']

    POS_CASH_balance_func(df_POS_CASH_balance).to_csv(path_POS_CASH_balance)
    bureau_func(df_bureau).to_csv(path_bureau)

    end_time = time.time()
    print("Execution time: ", (end_time - start_time) / 60, "mins")


main(path_log, path_bureau, path_POS_CASH_balance)