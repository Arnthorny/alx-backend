#!/usr/bin/env python3
"""
A basic Flask app
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from typing import Dict, Optional


class Config:
    """
    Config class
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Determine what locale to use """

    inc_locale = request.args.get('locale')

    if inc_locale in app.config['LANGUAGES']:
        return inc_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user() -> Optional[Dict]:
    """ Mock user login """
    mock_user_id = request.args.get('login_as')
    try:
        return users.get(int(mock_user_id))
    except (KeyError, ValueError, TypeError):
        return None


@app.before_request
def before_request() -> None:
    """ Adds a user to global object f """
    g.user = get_user()


@app.route('/')
def home():
    """Root route"""
    return render_template('5-index.html', user=g.user)


if __name__ == '__main__':
    app.run()
