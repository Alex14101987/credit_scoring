import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def confidence_interval(
        s1, s2, n, p
):
    '''
    Вычисление доверительного интервала

    s1 - распределение средних для 1 группы
    s2 - распределение средних для 2 группы
    n - объем смоделируемой выборки
    p = 1-alpha - 95%

    return:
    (s1[l_indx], s1[u_indx]), (s2[l_indx], s2[u_indx]) - доверительные интервалы для 2х групп
    '''
    u_pval = (1 + p) / 2
    l_pval = (1 - u_pval)
    l_indx = int(np.floor(n * l_pval))
    u_indx = int(np.floor(n * u_pval))
    return (s1[l_indx], s1[u_indx]), (s2[l_indx], s2[u_indx])


def bootstrap(
        data1,
        data2,
        n=10000,
        func=np.mean,
        subtr=np.subtract,
        alpha=0.05
):
    '''
    Бутстрап средних значений для двух групп

    data1 - выборка 1 группы
    data2 - выборка 2 группы
    n=10000 - сколько раз моделировать
    func=np.mean - функция отвыборки, например, среднее
    subtr=np.subtract,
    alpha=0.05 - 95% доверительный интервал

    return:
    ci_diff - доверительный интервал разницы средних для двух групп
    s1 - распределение средних для 1 группы
    s2 - распределение средних для 2 группы
    confidence_interval(s1, s2, n, 1 - alpha) - доверительные интервалы для двух групп
    '''
    s1, s2 = [], []
    s1_size = len(data1)
    s2_size = len(data2)

    for i in tqdm(range(n)):
        itersample1 = np.random.choice(data1, size=s1_size, replace=True)
        s1.append(func(itersample1))
        itersample2 = np.random.choice(data2, size=s2_size, replace=True)
        s2.append(func(itersample2))
    s1.sort()
    s2.sort()

    # доверительный интервал разницы
    bootdiff = subtr(s2, s1)
    bootdiff.sort()

    ci_diff = (np.round(bootdiff[np.round(n * alpha / 2).astype(int)], 3),
               np.round(bootdiff[np.round(n * (1 - alpha / 2)).astype(int)], 3))

    return ci_diff, s1, s2, confidence_interval(s1, s2, n, 1 - alpha)


def plot_bootstraping_mean(
        data,
        y,
        feat_name=None,
        val=[0, 1]
):
    '''
    Бутстрап средних значений для любого признака

    data - датафрейм с данными
    y - таргет
    feat_name - название признака, строка

    return:
    cidiff - доверительный интервал разницы в средних значениях для двух групп
    '''
    data1 = data[(y == val[0])][feat_name]
    data2 = data[(y == val[1])][feat_name]
    s1_mean_init = np.mean(data1)
    s2_mean_init = np.mean(data2)

    cidiff, s1, s2, ci = bootstrap(data1, data2)

    plt.hist(x=s1, density='uniform', label=f'target={val[0]}', bins='auto', alpha=0.8, color='darkorange')
    plt.hist(x=s2, density='uniform', label=f'target={val[1]}', bins='auto', alpha=0.6, color='royalblue')
    plt.legend()
    plt.axvline(x=s1_mean_init, color='darkorange')
    plt.axvline(x=s2_mean_init, color='royalblue')
    plt.axvline(x=ci[0][0], color='orange', linestyle='--')
    plt.axvline(x=ci[0][1], color='orange', linestyle='--')
    plt.axvline(x=ci[1][0], color='blue', linestyle='--')
    plt.axvline(x=ci[1][1], color='blue', linestyle='--')
    plt.show()

    return cidiff

def verdict(ci_diff):
    cidiff_min=0.001 #,близкое к 0
    ci_diff_abs = [abs(ele) for ele in ci_diff]
    if (min(ci_diff) <= cidiff_min <= max(ci_diff)):
        print(ci_diff,'Различия в средних статистически незначимы.')
    elif (cidiff_min >= max(ci_diff_abs) >= 0) or (cidiff_min >= min(ci_diff_abs) >= 0):
        print(ci_diff,'Различия в средних статистически незначимы.')
    else:
        print(ci_diff,'Различия в средних статистически значимы.')
        return 1

def main(df):
    important_features = pd.DataFrame()
    list_columns = df.columns

    for i in list_columns:
        cidiff = plot_bootstraping_mean(df, df['TARGET'], feat_name=i)
        verdict(cidiff)
        if verdict(cidiff) == 1:
            important_features[i] = df[i]
            print('find important feature')
    important_features
    important_features.to_csv('important_features.csv')

