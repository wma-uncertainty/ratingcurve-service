from apiflask import APIFlask, Schema
from apiflask.fields import List, Float, Integer, String
from apiflask.validators import OneOf

from ratingcurve.ratings import PowerLawRating

import pandas as pd

from .utils import test_rating, format_rating_table, format_form_to_df

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
    stage = List(Float, required=True, description='Stage observations')
    discharge = List(Float, required=True, description='Discharge observations')
    discharge_se = List(Float, required=False, description='Discharge standard error')


class RatingOut(Schema):
    stage = List(Float, description='Stage')
    discharge = List(Float, description='Expected discharge')
    median = List(Float, description='Median discharge')
    gse = List(Float, description='Geometric standard error')


class FormIn(Schema):
    data = String(
        required=True,
        description='Stage, discharge, and discharge standard error in CSV format',
    )


class FormOut(Schema):
    data = String(
        description='Rating table in CSV format',
    )


class FitPowerLawQuery(Schema):
    segments = Integer(
        load_default=1,
        validate=lambda x: x > 0,
        description='Number of segments in the rating curve',
    )
    method = String(
        load_default='advi',
        validate=OneOf(['advi', 'nuts']),
        description='Fit with ADVI (fast) or NUTS (accurate)',
    )
    # format = String(
    #    load_default='json',
    #    validate=OneOf(['json']),  # csv, html
    #    description='Response format: json',  # csv, or html
    # )


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

    @app.route('/fit/powerlaw/csv/', methods=['POST'])
    @app.input(FormIn, location='form')
    @app.input(FitPowerLawQuery, location='query')
    @app.output(FormOut)
    def fit_csv(form_data, query_data):
        """Fit a power-law rating curve with n segments"""
        segments = query_data.get('segments')
        method = query_data.get('method')
        breakpoint()
        df = format_form_to_df(form_data)

        rating = PowerLawRating(segments=segments)

        _ = rating.fit(
            q=df['discharge'],
            h=df['stage'],
            q_sigma=df['discharge_se'],
            method=method,
            progressbar=True,
        )

        return rating.table().to_csv()

    @app.route('/fit/powerlaw/', methods=['POST'])
    @app.input(ObservationsIn, location='json')
    @app.input(FitPowerLawQuery, location='query')
    @app.output(RatingOut)
    def fit(json_data, query_data):
        """Fit a power-law rating curve with n segments"""
        segments = query_data.get('segments')
        method = query_data.get('method')
        df = pd.DataFrame.from_dict(json_data)

        rating = PowerLawRating(segments=segments)

        _ = rating.fit(
            q=df['discharge'],
            h=df['stage'],
            q_sigma=df['discharge_se'],
            method=method,
            progressbar=True,
        )

        return format_rating_table(rating)

    return app
