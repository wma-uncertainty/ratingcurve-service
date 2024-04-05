from apiflask import APIFlask
from flask import send_file

from io import BytesIO

import pandas as pd

from .schema import ObservationsIn, RatingOut, RRTIn, RRTOut, FitPowerLawQuery
from .utils import test_rating, fit_powerlaw_rating, format_rating_table, rrt_file_to_df

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

    @app.route('/test/powerlaw', methods=['GET'])
    @app.output(RatingOut)
    def test():
        """Test endpoint that computes and returns a rating table"""
        rating = test_rating(segments=2, iterations=100_000)
        return format_rating_table(rating)

    @app.route('/fit/powerlaw/rrt/', methods=['POST'])
    @app.input(FitPowerLawQuery, location='query')
    @app.input(RRTIn, location='files')
    @app.output(RRTOut)
    def fit_rrt(files_data, query_data):
        """Fit a power-law rating curve (RRT version)"""
        segments = query_data.get('segments')
        method = query_data.get('method')
        rrt_csv = files_data.get('csv')
        df = rrt_file_to_df(rrt_csv)

        # rating = fit_powerlaw_rating(df, segments=segments, method=method)
        # out = rating_to_rrt(rating)

        # testing REMOVE
        rrt_csv.stream.seek(0)
        out = BytesIO(rrt_csv.stream.read())

        return send_file(
            out,
            as_attachment=True,
            download_name='rating_table.csv',
        )

    @app.route('/fit/powerlaw/', methods=['POST'])
    @app.input(ObservationsIn, location='json')
    @app.input(FitPowerLawQuery, location='query')
    @app.output(RatingOut)
    def fit(json_data, query_data):
        """Fit a power-law rating curve with n segments"""
        segments = query_data.get('segments')
        method = query_data.get('method')
        df = pd.DataFrame.from_dict(json_data)
        rating = fit_powerlaw_rating(df, segments=segments, method=method)

        return format_rating_table(rating)

    # precompile the rating model (TODO set compile directory)
    test_rating()

    return app
