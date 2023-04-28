import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# Create the application object
app = Flask(__name__)

# Configurations for creating the database using SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False

# Create the SQLAlchemy object
db = SQLAlchemy(app)

from shop import routes

