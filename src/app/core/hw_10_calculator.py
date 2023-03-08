from src.app.core.hw_10_api import Features


class Calculator(object):
    """Класс принимает на вход признаки и расчитывает одобренную сумму."""

    def calc_amount(
        self,
        proba: str,
        features: Features,
    ) -> int:
        """Функция принимает на вход признаки и расчитывает одобренную сумму."""
        if proba < self._threshold and features.income_category == 'rich':
            return 500
        if features.age_category == 'other':
            return 200
        return 100

# flake8 --config=setup.cfg ./src/app/core/hw_10_calculator.py
