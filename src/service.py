from flask import Flask, jsonify
import os
import pandas as pd

from .tests import test_rating

app = Flask(__name__)


@app.route('/')
def hello_world():
    # provide basic usage info
    return jsonify(message='Hello, World!')


@app.route('/test')
def test():
    breakpoint()
    rating = test_rating(segments=2)
    df = rating.table()
    # return df.to_json()
    return df.to_html(index=False)


@app.route('/fit/powerlaw/<int:segments>', methods=['POST'])
def fit(segments):
    """Add option to return html or json"""
    request = request.get_json()
    breakpoint()
    df = pd.DataFrame(request['data'])


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # precompile the model
    test_rating()

    app.run(debug=True, host='0.0.0.0', port=port)
