import pandas as pd

df = pd.read_csv('/kaggle/input/shiftlogs/previous_application.csv')
df1 = pd.read_csv('/kaggle/input/shiftlogs/installments_payments.csv')

previous_application = pd.DataFrame()

previous_application['SK_ID_CURR'] = df['SK_ID_CURR'].drop_duplicates()

previous_application['Отношение полученного кредита к ежемесячному платежу'] = df['AMT_CREDIT'] / df['AMT_ANNUITY']

previous_application['Ставка новогокредита'] = df['AMT_APPLICATION'] / df['AMT_CREDIT']

previous_application['когда был последний срок подачи предыдущей заявки'] = df["DAYS_TERMINATION"] - df["DAYS_LAST_DUE"]

previous_application.to_csv('previous_application.csv', index = False)


installments_payments = pd.DataFrame()

installments_payments['SK_ID_CURR'] = df1['SK_ID_CURR'].drop_duplicates()

installments_payments['Новая длительность'] = df1["DAYS_INSTALMENT"] - df1["DAYS_ENTRY_PAYMENT"]

installments_payments['Разница нового платежа'] = df1["AMT_INSTALMENT"] - df1["AMT_PAYMENT"]

installments_payments['Количество версий'] = df1["NUM_INSTALMENT_VERSION"].astype("object")
df1[(df1["NUM_INSTALMENT_VERSION"] != 1) & (df1["NUM_INSTALMENT_VERSION"] != 0) & (df1["NUM_INSTALMENT_VERSION"] != 2) & (df1["NUM_INSTALMENT_VERSION"] != 3)]['NUM_INSTALMENT_VERSION'] = 4


installments_payments.to_csv('installments_payments.csv', index = False)