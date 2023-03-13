import numpy as np
import pandas as pd

train = pd.read_csv('/kaggle/input/shiftlogs/application_train.csv')
test = pd.read_csv('/kaggle/input/shiftlogs/application_test.csv')

all_data = pd.concat((train, test)).reset_index(drop=True)

house_columns = ['NAME_HOUSING_TYPE', 'APARTMENTS_AVG', 'BASEMENTAREA_AVG', 'YEARS_BEGINEXPLUATATION_AVG', 'YEARS_BUILD_AVG', 'COMMONAREA_AVG',
                 'ELEVATORS_AVG', 'ENTRANCES_AVG', 'FLOORSMAX_AVG', 'FLOORSMIN_AVG', 'LANDAREA_AVG', 'LIVINGAPARTMENTS_AVG', 'LIVINGAREA_AVG',
                 'NONLIVINGAPARTMENTS_AVG', 'NONLIVINGAREA_AVG', 'APARTMENTS_MODE', 'BASEMENTAREA_MODE', 'YEARS_BEGINEXPLUATATION_MODE',
                 'YEARS_BUILD_MODE' ,'COMMONAREA_MODE' , 'ELEVATORS_MODE', 'ENTRANCES_MODE', 'FLOORSMAX_MODE', 'FLOORSMIN_MODE', 'LANDAREA_MODE',
                 'LIVINGAPARTMENTS_MODE', 'LIVINGAREA_MODE', 'NONLIVINGAPARTMENTS_MODE', 'NONLIVINGAREA_MODE' ,'APARTMENTS_MEDI',
                 'BASEMENTAREA_MEDI', 'YEARS_BEGINEXPLUATATION_MEDI', 'YEARS_BUILD_MEDI', 'COMMONAREA_MEDI', 'ELEVATORS_MEDI', 'ENTRANCES_MEDI',
                 'FLOORSMAX_MEDI', 'FLOORSMIN_MEDI', 'LANDAREA_MEDI', 'LIVINGAPARTMENTS_MEDI', 'LIVINGAREA_MEDI', 'NONLIVINGAPARTMENTS_MEDI',
                 'NONLIVINGAREA_MEDI', 'FONDKAPREMONT_MODE', 'HOUSETYPE_MODE', 'TOTALAREA_MODE', 'WALLSMATERIAL_MODE', 'EMERGENCYSTATE_MODE']

application_train_test = pd.DataFrame()

application_train_test['SK_ID_CURR'] = all_data['SK_ID_CURR']

application_train_test['Кол-во документов'] = all_data.loc[:, 'FLAG_DOCUMENT_2': 'FLAG_DOCUMENT_21'].sum(axis=1)

application_train_test['Информация о доме'] = np.where(all_data.loc[:, house_columns].isnull().sum(axis=1) < 30, 1, 0)

application_train_test['Кол-во полных лет'] = abs(all_data['DAYS_BIRTH']/365).apply(np.int64)

application_train_test['Год смены документа'] = abs(all_data['DAYS_BIRTH']/365).apply(np.int64) - abs(all_data['DAYS_REGISTRATION']/365).apply(np.int64)

application_train_test['Признак задержки смены документа'] = np.where(abs(all_data['DAYS_BIRTH']/365).apply(np.int64)
                                                                      - abs(all_data['DAYS_REGISTRATION']/365).apply(np.int64) != 14|20|45, 1, 0)

application_train_test['Доля денег которые клиент отдает на займ за год'] = all_data['AMT_ANNUITY']/all_data['AMT_INCOME_TOTAL']

application_train_test['Среднее кол-во детей в семье на одного взрослого'] = all_data['CNT_CHILDREN'] / (all_data['CNT_FAM_MEMBERS'] - all_data['CNT_CHILDREN']) 

application_train_test['Средний доход на ребенка'] = all_data['AMT_INCOME_TOTAL'] / all_data['CNT_CHILDREN']

application_train_test['Средний доход на взрослого'] = all_data['AMT_INCOME_TOTAL'] / (all_data['CNT_FAM_MEMBERS'] - all_data['CNT_CHILDREN'])

application_train_test['Процентная ставка'] = ((all_data['AMT_CREDIT'] - all_data['AMT_GOODS_PRICE']) / ((all_data['AMT_CREDIT'] / all_data['AMT_ANNUITY']) / 12)) / all_data['AMT_GOODS_PRICE']

application_train_test[['скор внеешних источников1', 'скор внеешних источников2', 'скор внеешних источников3']] = all_data[['EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3']]

result_train = train.groupby(["CODE_GENDER", "NAME_EDUCATION_TYPE"])["AMT_INCOME_TOTAL"].mean().diff()
application_train_test['разница емжду средним доходом в группе и доходом заявителя'] = train['AMT_CREDIT'].diff(result_train)

application_train_test.to_csv('application_train_test.csv', index=False)
