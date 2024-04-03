from apiflask import APIFlask, Schema
from apiflask.fields import List, Float, Integer, String
from flask import render_template

from ratingcurve.ratings import PowerLawRating

import pandas as pd

from .utils import test_rating, format_rating_table

NAME = 'ratingcurve'
VERSION = '0.1.0'
DESCRIPTION = """
A microservice that fits stage-discharge rating curves using the
<a href="https://github.com/thodson-usgs/ratingcurve">ratingcurve</a>
Python library. 
"""
LICENSE = {
    'name': 'CC0',
    'url': 'https://creativecommons.org/public-domain/cc0/',
}


class ObservationsIn(Schema):
    stage = List(Float, required=True)
    discharge = List(Float, required=True)
    discharge_se = List(Float, required=False)


class RatingOut(Schema):
    stage = List(Float)
    discharge = List(Float)
    median = List(Float)  # discharge_median
    gse = List(Float)  # discharge_gse


class FitPowerLawQuery(Schema):
    segments = Integer(load_default=1)
    format = String(load_default='json')


# Create the ratingcurve application
def create_app():
    """Create and configure an instance of the Flask application."""

    app = APIFlask(
        __name__,
        title=NAME,
        version=VERSION,
        spec_path='/openapi.json',
        docs_path='/',  # serve the Swagger UI at root
    )

    app.description = DESCRIPTION
    app.license = LICENSE
    # precompile the rating model (TODO set compile directory)
    test_rating()

    @app.route('/test', methods=['GET'])
    @app.output(RatingOut)
    def test():
        """Test endpoint that computes and returns a rating table"""
        rating = test_rating(segments=2, iterations=100_000)
        return format_rating_table(rating)

    @app.route('/fit/powerlaw/', methods=['POST'])
    @app.input(ObservationsIn, location='json')
    @app.input(FitPowerLawQuery, location='query')
    @app.output(RatingOut)
    def fit(json_data, query_data):
        """Fit a power-law rating curve with n segments"""
        segments = query_data.get('segments')
        df = pd.DataFrame.from_dict(json_data)

        rating = PowerLawRating(segments=segments)

        _ = rating.fit(
            q=df['discharge'],
            h=df['stage'],
            q_sigma=df['discharge_se'],
            progressbar=True,
        )

        return format_rating_table(rating)

    return app
