from flask import Flask
import os

from tests import test_rating

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # precompile the model
    test_rating()

    app.run(debug=True, host='0.0.0.0', port=port)
