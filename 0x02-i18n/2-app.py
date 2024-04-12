#!/usr/bin/env python3
"""
A basic Flask app
"""

from flask import Flask, render_template
from flask_babel import Babel


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


@babel.localselector
def get_locale():
    """Determine what locale to use """
    request.accept_languages.best_match(app.config.LANGUAGES)


@app.route('/')
def home():
    """Root route"""
    return render_template('2-index.html')


if __name__ == '__main__':
    app.run()
