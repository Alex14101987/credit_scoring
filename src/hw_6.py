import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

import time
start_time = time.time()

all_data = pd.read_csv('application_train.csv')

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

application_train_test['TARGET'] = all_data['TARGET']

application_train_test['Кол-во документов'] = all_data.loc[:, 'FLAG_DOCUMENT_2': 'FLAG_DOCUMENT_21'].sum(axis=1)

application_train_test['Информация о доме'] = np.where(all_data.loc[:, house_columns].isnull().sum(axis=1) < 30, 1, 0)

application_train_test['Кол-во полных лет'] = abs(all_data['DAYS_BIRTH']/365).apply(np.int64)

application_train_test['Год смены документа'] = application_train_test['Кол-во полных лет'] - abs(all_data['DAYS_REGISTRATION']/365).apply(np.int64)

application_train_test['Признак задержки смены документа'] = np.where(application_train_test['Год смены документа'] != 14|20|45, 1, 0)

application_train_test['Доля денег которые клиент отдает на займ за год'] = all_data['AMT_ANNUITY']/all_data['AMT_INCOME_TOTAL']

application_train_test['Среднее кол-во детей в семье на одного взрослого'] = all_data['CNT_CHILDREN'] / (all_data['CNT_FAM_MEMBERS'] - all_data['CNT_CHILDREN'])

application_train_test['Средний доход на ребенка'] = all_data['AMT_INCOME_TOTAL'] / all_data['CNT_CHILDREN']

application_train_test['Средний доход на взрослого'] = all_data['AMT_INCOME_TOTAL'] / (all_data['CNT_FAM_MEMBERS'] - all_data['CNT_CHILDREN'])

application_train_test['Процентная ставка'] = ((all_data['AMT_CREDIT'] - all_data['AMT_GOODS_PRICE']) / ((all_data['AMT_CREDIT'] / all_data['AMT_ANNUITY']) / 12)) / all_data['AMT_GOODS_PRICE']

application_train_test[['скор внеешних источников1', 'скор внеешних источников2', 'скор внеешних источников3']] = all_data[['EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3']]

feature_1 = 'Год смены документа'
min_feature_1 = application_train_test[feature_1].min()
max_feature_1 = application_train_test[feature_1].max()
feature_2 = 'Кол-во полных лет'
min_feature_2 = application_train_test[feature_2].min()
max_feature_2 = application_train_test[feature_2].max()

application_train_test[application_train_test['TARGET']==0].plot(x=feature_1, y=feature_2, marker='.', linestyle='')

application_train_test[application_train_test['TARGET']==0][['Кол-во документов', 'Информация о доме',
       'Кол-во полных лет', 'Год смены документа',
       'Признак задержки смены документа',
       'Доля денег которые клиент отдает на займ за год',
       'Среднее кол-во детей в семье на одного взрослого',
       'Средний доход на ребенка', 'Средний доход на взрослого',
       'Процентная ставка', 'скор внеешних источников1',
       'скор внеешних источников2', 'скор внеешних источников3']].corr()

application_train_test['скор внеешних источников1'] = application_train_test['скор внеешних источников1'].fillna(application_train_test['скор внеешних источников1'].mean())
application_train_test['скор внеешних источников2'] = application_train_test['скор внеешних источников2'].fillna(application_train_test['скор внеешних источников2'].mean())
application_train_test['скор внеешних источников3'] = application_train_test['скор внеешних источников3'].fillna(application_train_test['скор внеешних источников3'].mean())
application_train_test['Процентная ставка'] = application_train_test['Процентная ставка'].fillna(application_train_test['Процентная ставка'].mean())
application_train_test.replace([np.inf, -np.inf], 0, inplace=True)

number_inf = application_train_test.isna().sum()

from sklearn.linear_model import LinearRegression

X = application_train_test[application_train_test['TARGET']==0][feature_1].values.reshape(-1, 1)
y = application_train_test[application_train_test['TARGET']==0][feature_2]

reg = LinearRegression()
reg.fit(X, y)

plt.plot(X, y, '.')
plt.plot(X, reg.predict(X))

sns.scatterplot(x=application_train_test[feature_1], y=application_train_test[feature_2], hue=application_train_test['TARGET'])

train_X = application_train_test[application_train_test['TARGET'].isin([0, 1])][[feature_1, feature_2]]
train_y = application_train_test[application_train_test['TARGET'].isin([0, 1])]['TARGET']

X = np.linspace(-8, 8, 100)
# plt.plot(X, 1/(1+np.exp(-X)))
X = np.linspace(-4, 4)
# plt.plot(X, np.log2(1+np.exp(-X)))
# plt.plot(X, (-np.sign(X)+1)/2)

from sklearn.linear_model import LogisticRegression

logreg = LogisticRegression()
logreg.fit(train_X, train_y)

_x = np.linspace(min_feature_1, max_feature_1, 100)
_y = np.linspace(min_feature_2, max_feature_2, 100)
xv, yv = np.meshgrid(_x, _y)
grid = np.vstack([xv.flatten(), yv.flatten()]).T
_pred = logreg.predict(grid)
sns.scatterplot(x=train_X[feature_1], y=train_X[feature_2], hue=train_y)
sns.scatterplot(x=grid[:,0], y=grid[:,1], hue=_pred, alpha=0.1)

from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree

tree = DecisionTreeClassifier()
tree.fit(train_X, train_y)
_x = np.linspace(min_feature_1, max_feature_1, 100)
_y = np.linspace(min_feature_2, max_feature_2, 100)
xv, yv = np.meshgrid(_x, _y)
grid = np.vstack([xv.flatten(), yv.flatten()]).T
_pred = tree.predict(grid)

sns.scatterplot(x=train_X[feature_1], y=train_X[feature_2], hue=train_y)
sns.scatterplot(x=grid[:,0], y=grid[:,1], hue=_pred, alpha=0.1)

plt.figure(figsize=(150, 50))
_ = plot_tree(tree)

print("--- %s seconds ---" % (time.time() - start_time))
