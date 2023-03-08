import pickle

from src.app.core.hw_10_api import Features, ScoringDecision, ScoringResult
from src.app.core.hw_10_calculator import Calculator


class SimpleModel(object):
    """Класс для моделей c расчетом proba и threshold."""

    _threshold = 0.1

    def __init__(self, model_path: str):
        """Создает объект класса."""
        with open(model_path, 'rb') as pickled_model:
            self._model = pickle.load(pickled_model)

    def _predict_proba(self, features: Features) -> float:
        """Определяет вероятность невозврата займа."""
        return self._model.predict_proba(
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


class AdvancedModel(SimpleModel):
    """Класс для модели, которая выбирает одобренную сумму."""

    def __init__(self, model_path: str):
        """Создает объект класса."""
        super().__init__(model_path)
        self._calculator = Calculator()

    def get_scoring_result(self, features):
        """Вычисляет одобренную сумму."""
        proba = self._predict_proba(features)

        final_decision = ScoringDecision.declined
        approved_amount = 0
        if proba < self._threshold:
            final_decision = ScoringDecision.accepted
            approved_amount = self._calculator.calc_amount(
                proba,
                features,
            )

        return ScoringResult(
            decision=final_decision,
            amount=approved_amount,
            threshold=self._threshold,
            proba=proba,
        )


# flake8 --config=setup.cfg ./src/app/core/hw_10_model.py
