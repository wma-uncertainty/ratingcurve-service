from apiflask import APIFlask, Schema
from apiflask.fields import List, Float
import pandas as pd

from .tests import test_rating

# precompile the rating model
test_rating()

app = APIFlask(
    __name__, title='Ratingcurve API', version='0.1.0', spec_path='/openapi.json'
)


class ObservationsIn(Schema):
    stage = List(Float, required=True)
    discharge = List(Float, required=True)
    discharge_se = List(Float, required=False)


class RatingOut(Schema):
    stage = List(Float)
    discharge = List(Float)
    median = List(Float) #discharge_median
    gse = List(Float) #discharge_gse


@app.route('/', methods=['GET'])
def hello_world():
    """Basic usage info"""
    return 'Hello, World!'


@app.route('/test', methods=['GET'])
@app.output(RatingOut)
def test():
    """Test endpoint that computes and returns a rating table"""
    rating = test_rating(segments=2, iterations=100_000)
    return _format_rating_table(rating)


@app.route('/fit/powerlaw/<int:n>', methods=['POST'])
@app.input(ObservationsIn)
@app.output(RatingOut)
def fit(n):
    """Fit a power-law rating curve with n segments"""
    request = request.get_json()
    df = pd.read_json(request)

    rating = PowerLawRating(segments=n)

    trace = rating.fit(
        q=df['discharge'], h=df['stage'], q_sigma=df['discharge_se'], progressbar=False
    )

    return _format_rating_table(rating)


def _format_rating_table(rating):
    df = rating.table()
    df = df.round(2)
    return df.to_dict('list')
