from apiflask import APIFlask, Schema
from apiflask.fields import List, Float
from flask import render_template, request

from ratingcurve.ratings import PowerLawRating

import pandas as pd

from .tests import test_rating

# precompile the rating model
test_rating()

app = APIFlask(
    __name__, title='ratingcurve API', version='0.1.0', spec_path='/openapi.json'
)


class ObservationsIn(Schema):
    stage = List(Float, required=True)
    discharge = List(Float, required=True)
    discharge_se = List(Float, required=False)


class RatingOut(Schema):
    stage = List(Float)
    discharge = List(Float)
    median = List(Float)  # discharge_median
    gse = List(Float)  # discharge_gse


@app.route('/', methods=['GET'])
def landing():
    """Landing page"""
    return render_template('index.html')


@app.route('/test', methods=['GET'])
@app.output(RatingOut)
def test():
    """Test endpoint that computes and returns a rating table"""
    rating = test_rating(segments=2, iterations=100_000)
    return _format_rating_table(rating)


@app.route('/fit/powerlaw/<int:n>', methods=['POST'])
@app.input(ObservationsIn)
@app.output(RatingOut)
def fit(json_data, n):
    """Fit a power-law rating curve with n segments"""
    df = pd.DataFrame.from_dict(json_data)

    rating = PowerLawRating(segments=n)

    trace = rating.fit(
        q=df['discharge'], h=df['stage'], q_sigma=df['discharge_se'], progressbar=True
    )

    return _format_rating_table(rating)


def _format_rating_table(rating):
    df = rating.table()
    df = df.round(2)
    return df.to_dict('list')
