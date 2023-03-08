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

# flake8 --config=setup.cfg ./src/app/core/hw_10_api.py
