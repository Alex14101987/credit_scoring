import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd

df = pd.read_csv('/kaggle/input/shiftlogs/application_train.csv')

fraud_df = pd.DataFrame()
fraud_df['SK_ID_CURR'] = df['SK_ID_CURR']

def alert(df):
    if df['AMT_CREDIT'] >= 1_135_000 and (df['FLAG_OWN_CAR'] == 'N') and (df['FLAG_OWN_REALTY'] == 'N'):
        return 1
    else:
        return 0


fraud_df['fraud_flag_1'] = df.apply(alert, axis=1)

fraud_df['fraud_flag_1'].value_counts()

fraud_df['fraud_flag_2'] = np.where(df['AMT_INCOME_TOTAL'] / 2 < df['AMT_ANNUITY'], 1, 0)

fraud_df['fraud_flag_2'].value_counts()

df = pd.read_csv('/kaggle/input/shiftlogs/credit_card_balance.csv')

df = df[['SK_ID_CURR', 'AMT_DRAWINGS_ATM_CURRENT']]

df['mean'] = df['AMT_DRAWINGS_ATM_CURRENT'].groupby(df['SK_ID_CURR']).mean()

df['fraud_flag_3'] = np.where(df['AMT_DRAWINGS_ATM_CURRENT'] * 10 > df['mean'], 1, 0)

fraud_df = pd.merge(fraud_df, df, on="SK_ID_CURR")
