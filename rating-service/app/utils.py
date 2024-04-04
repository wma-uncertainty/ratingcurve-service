from __future__ import annotations
from typing import TYPE_CHECKING

from ratingcurve.ratings import PowerLawRating
from ratingcurve import data

if TYPE_CHECKING:
    from arviz import InferenceData


def test_rating(segments: int = 1, iterations: int = 100) -> InferenceData:
    """Precompile ratingmodel on test data"""
    # load tutorial data
    df = data.load('green channel')

    # initialize the model
    rating = PowerLawRating(segments=segments)

    # fit the model
    _ = rating.fit(
        q=df['q'],
        h=df['stage'],
        q_sigma=df['q_sigma'],
        n=iterations,
    )

    return rating


def format_rating_table(rating: InferenceData):
    """TODO docstring"""
    df = rating.table()
    df = df.round(2)
    return df.to_dict('list')
