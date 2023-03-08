from src.app.core.hw_10_calculator import Calculator
from src.app.core.hw_10_api import Features
import pytest


class TestCalculator:
    """Тест калькулятора."""

    @pytest.mark.parametrize(
        'proba, income_category, age_category, expected_amount',
        [
            # 500k
            (0, '> 50_000', 'young', 500_000),
            (0, '> 50_000', 'old', 500_000),
            (0, '> 50_000', 'other', 500_000),
            # 200k
            (0, '< 10_000', 'other', 200_000),
            (0, 'other', 'other', 200_000),
            (1, '< 10_000', 'other', 200_000),
            (1, '> 50_000', 'other', 200_000),
            (1, 'other', 'other', 200_000),
            # 100k
            (0, '< 10_000', 'young', 100_000),
            (0, 'other', 'old', 100_000),
            (1, '< 10_000', 'young', 100_000),
            (1, '> 50_000', 'old', 100_000),
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

