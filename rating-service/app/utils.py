from __future__ import annotations
from typing import TYPE_CHECKING

import pandas as pd
import re

from io import BytesIO
from ratingcurve.ratings import PowerLawRating
from ratingcurve import data

if TYPE_CHECKING:
    from arviz import InferenceData
    from pandas import DataFrame
    from werkzeug.datastructures import FileStorage


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


def fit_powerlaw_rating(
    df: DataFrame, segments: int = 1, method: str = 'advi', **kwargs
) -> PowerLawRating:
    """Fit a power-law rating curve"""

    rating = PowerLawRating(segments=segments)
    _ = rating.fit(
        q=df['discharge'],
        h=df['stage'],
        q_sigma=df['discharge_se'],
        method=method,
        **kwargs,
    )

    return rating


def format_rating_table(rating: InferenceData):
    """TODO docstring"""
    df = rating.table()
    df = df.round(2)
    return df.to_dict('list')


def rrt_file_to_df(rrt_csv: FileStorage) -> DataFrame:
    """Convert RRT file to a pandas DataFrame"""
    rrt_csv.stream.seek(0)
    df = pd.read_csv(rrt_csv)

    # filter RRT data where "Use" is True
    df = df.loc[df.Use]

    # drop units from column names, which are in parentheses
    # eg., 'stage (ft)' -> 'stage'
    df = df.rename(columns=lambda x: re.sub(' \(.*\)', '', x))

    # TODO save these names as globals
    df = df.rename(columns={'Gage height': 'stage', 'Discharge': 'discharge'})

    # TODO include or compute uncertainty in discharge
    df['discharge_se'] = 0.0

    return df


def rating_to_rrt(rating: PowerLawRating) -> BytesIO:
    """Convert rating to RRT table"""
    df = rating.table()
    out = BytesIO('dump the csv here')
    rating.rrt().to_csv(out, index=False)
    out.seek(0)
    return out
