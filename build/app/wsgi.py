#!/usr/bin/env python3

"""
WSGI entry point for the Flask application.
This file is used by gunicorn to import and run the Flask app.
"""

from app import app

if __name__ == "__main__":
    app.run()