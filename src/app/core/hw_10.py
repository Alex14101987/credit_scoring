# Модель

import pickle

class CustomScoringModel:

    def predict_proba(
        self,
        income_category: str,
        age_category: str,
        count_doc: int,
        inf_house: int,
        interest_rate_category: str,
        perc_money: int,
        ext1: int,
        ext2: int,
        ext3: int
    ) -> float:
        proba = 0
        # низкий дефолт 
        if ext1 > 0.7:
            proba -= 0.1
        if ext2 > 0.7:
            proba -= 0.1
        if ext3 > 0.7:
            proba -= 0.1
        # высокий дефолт
        if inf_house == 0:
            proba += 0.1
        if count_doc == 0:
            proba += 0.1
        if income_category == "poor":
            proba += 0.1
        if age_category == 'old' or age_category == 'young':
            proba += 0.1
        if perc_money > 0.25:
            proba += 0.1
        if interest_rate_category == 'disloyal':
            proba += 0.1
        if ext1 < 0.3:
            proba += 0.1
        if ext2 < 0.3:
            proba += 0.1
        if ext3 < 0.3:
            proba += 0.1
        return proba
    def save_model(
        self,
        file_path: str,
    ) -> None:
        """Функция принимает на вход путь, сохраняет по эту пути .pickle с моделью."""
        with open(file_path, 'wb') as file:
            pickle.dump(self, file)


# Инициализируем модель
model = CustomScoringModel()
model

# Сохраним модель
model_path = './model.pickle'
model.save_model('model.pickle')

from dataclasses import dataclass
from enum import Enum, auto


class ScoringDecision(Enum):
    """Возможные решения модели."""

    ACCEPTED = auto()
    DECLINED = auto()


@dataclass
class ScoringResult:
    """Класс, содержащий результаты скоринга."""

    decision: ScoringDecision
    amount: int
    threshold: float
    proba: float

@dataclass
class Features:
    """Фичи для принятия решения об одобрении."""

    income_category: str = 'other'
    age_category: str = 'other'
    count_doc: int = 'other'
    inf_house: int = 'other'
    interest_rate_category: str = 'other'
    perc_money: int = 'other'
    ext1: int = 'other'
    ext2: int = 'other'
    ext3: int = 'other'


class SimpleModel:
    """Класс для моделей c расчетом proba и threshold."""

    _threshold = 0

    def __init__(self, model_path: str):
        """Создает объект класса."""
        with open(model_path, 'rb') as pickled_model:
            self._model = pickle.load(pickled_model)

    def _predict_proba(self, features: Features) -> float:
        """Определяет вероятность невозврата займа."""
        res = self._model.predict_proba(
            features.income_category,
            features.age_category,
            features.count_doc,
            features.inf_house,
            features.interest_rate_category,
            features.perc_money,
            features.ext1,
            features.ext2,
            features.ext3,
        )
        return res

# Инициализируем модель
core_simple_model = SimpleModel('./model.pickle')

class Calculator:
    def calc_amount(
        self,
        proba: str,
        features: Features,
    ) -> int:
        """Функция принимает на вход вероятность дефолта и признаки и расчитывает одобренную сумму."""
        if proba < 0.10 or features.income_category == 'rich':
            return 500
        if features.age_category == 'other':
            return 200
        return 100


# унаследуемся от SimpleModel чтобы не переопределять одинаковый функционал
class AdvancedModel(SimpleModel):

    def __init__(self, model_path: str):
        super().__init__(model_path)
        self._calculator = Calculator()

    def get_scoring_result(self, features):
        p = self._predict_proba(features)

        final_decision = ScoringDecision.DECLINED
        approved_amount = 0
        if p < 0.4:
            final_decision = ScoringDecision.ACCEPTED
            approved_amount = self._calculator.calc_amount(
                p,
                features,
            )

        return ScoringResult(decision=final_decision, amount=approved_amount, threshold=self._threshold, proba=p)


import json
from datetime import datetime


class Service:
    _model = AdvancedModel('./model.pickle')

    def _calculate_income_category(
            self,
            income: int,
    ) -> str:
        if income < 60_000:
            return "poor"
        if income > 135_000:
            return "rich"
        return "other"

    def _calculate_interest_rate_category(
            self,
            interest_rate: int,
    ) -> str:
        if interest_rate < 0.07:
            return "loyal"
        if interest_rate > 0.12:
            return "disloyal"
        return "other"

    def _calculate_age_category(
            self,
            age: int
    ) -> str:
        if age < 25:
            return "young"
        if age > 60:
            return "old"
        return "other"

# Инициализируем сервис
service = Service()

import pandas as pd

# Берем датасет с насчитанными признаками
df = pd.read_csv('application_train_test.csv')
df.rename(columns={"Средний доход на взрослого": "income",
                   "Процентная ставка": "interest_rate",
                  'Кол-во документов': 'count_doc',
                  'Кол-во полных лет': 'age',
                  'Информация о доме': 'inf_house',
                  'Доля денег которые клиент отдает на займ за год': 'perc_money',
                  'скор внеешних источников1': 'ext1',
                  'скор внеешних источников2': 'ext2',
                  'скор внеешних источников3': 'ext3'}, inplace=True)

# насчитаем признаки
df['income_category'] = df['income'].apply(lambda x: service._calculate_income_category(x))
df.drop(columns=['income'], inplace=True)
df['age_category'] = df['age'].apply(lambda x: service._calculate_age_category(x))
df.drop(columns=['age'], inplace=True)
df['interest_rate_category'] = df['interest_rate'].apply(lambda x: service._calculate_interest_rate_category(x))
df.drop(columns=['interest_rate'], inplace=True)

# инициализируем модель
model = AdvancedModel('./model.pickle')

# для каждого "наблюдения" получим решение
df['result'] = df.apply(
    lambda x: model.get_scoring_result(
        Features(
            income_category=x['income_category'],
            age_category=x['interest_rate_category'],
            inf_house=x['inf_house'],
            count_doc=x['count_doc'],
            interest_rate_category=x['interest_rate_category'],
            perc_money=x['perc_money'],
            ext1=x['ext1'],
            ext2=x['ext2'],
            ext3=x['ext3'],
        )
    ),
    axis=1
)

df['decision'] = df['result'].apply(lambda x: x.decision.name)
df['amount'] = df['result'].apply(lambda x: x.amount)
df['proba'] = df['result'].apply(lambda x: x.proba)

