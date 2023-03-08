# from src.app.core.hw_10_calculator import Calculator
# from src.app.core.hw_10_api import Features
# импорты почему-то не работали...

import pytest

from dataclasses import dataclass
from enum import Enum, auto


class ScoringDecision(Enum):
    """Возможные решения модели."""

    accepted = auto()
    declined = auto()


@dataclass
class ScoringResult(object):
    """Класс, содержащий результаты скоринга."""

    decision: ScoringDecision
    amount: int
    threshold: float
    proba: float


@dataclass
class Features(object):
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

class Calculator(object):
    """Класс принимает на вход признаки и расчитывает одобренную сумму."""

    def calc_amount(
        self,
        proba: str,
        features: Features,
    ) -> int:
        """Функция принимает на вход признаки и расчитывает одобренную сумму."""
        if proba < 0.1 and features.income_category == 'rich':
            return 500
        if features.age_category == 'other':
            return 200
        return 100

class TestCalculator:
    """Тест калькулятора."""

    @pytest.mark.parametrize(
        'proba, income_category, age_category, expected_amount',
        [
            # 500k
            (0, 'rich', 'young', 500),
            (0, 'rich', 'old', 500),
            (0, 'rich', 'other', 500),
            # 200k
            (0, 'poor', 'other', 200),
            (1, 'rich', 'other', 200),
            (1, 'poor', 'other', 200),
            # 100k
            (0, 'poor', 'young', 100),
            (0, 'poor', 'old', 100),
            (1, 'poor', 'young', 100),
            (1, 'rich', 'old', 100),
        ]
    )
    def test_calc_amount(
        self,
        proba,
        income_category,
        age_category,
        expected_amount,
    ):
        features = Features(
            income_category=income_category,
            age_category=age_category,
        )
        calculator = Calculator()
        assert calculator.calc_amount(
            proba,
            features,
        ) == expected_amount

