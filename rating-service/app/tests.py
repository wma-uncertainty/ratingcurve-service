from ratingcurve.ratings import PowerLawRating
from ratingcurve import data


def test_rating(segments=1, iterations=100):
    """Precompile ratingmodel on test data"""
    # load tutorial data
    df = data.load('green channel')

    # initialize the model
    powerrating = PowerLawRating(segments=segments)

    # fit the model
    # TODO reduce iterations b/c we don't need a good fit
    _ = powerrating.fit(
        q=df['q'],
        h=df['stage'],
        q_sigma=df['q_sigma'],
        n=iterations,
    )

    return powerrating
