#!/usr/bin/env python3
"""
A basic Flask app
"""

from flask import Flask, render_template, request
from flask_babel import Babel, _


class Config:
    """
    Config class
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Determine what locale to use """

    inc_locale = request.args.get('locale')

    if inc_locale in app.config['LANGUAGES']:
        return inc_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def home():
    """Root route"""
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run()
