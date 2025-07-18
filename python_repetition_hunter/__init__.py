"""Python Repetition Hunter - Find code duplications in Python projects"""

__version__ = "1.0.3"
__author__ = "Andres GU"
__email__ = "andres@waza.baby"

from .repetition_hunter import main, find_repetitions, RepetitionResult

__all__ = ["main", "find_repetitions", "RepetitionResult"]