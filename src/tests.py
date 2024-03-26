from ratingcurve.ratings import PowerLawRating
from ratingcurve import data


def _precompile_ratingmodel():
    """Precompile ratingmodel on test data"""
    # load tutorial data
    df = data.load('green channel')

    # initialize the model
    powerrating = PowerLawRating(segments=1)

    # fit the model
    # TODO reduce iterations b/c we don't need a good fit
    trace = powerrating.fit(q=df['q'], h=df['stage'], q_sigma=df['q_sigma'])
