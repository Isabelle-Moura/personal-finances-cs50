from app import create_app, db
from app.models import User, Transaction, Category, Budget
import click
import os

# 1. Create the application
# The app is necessary for extensions (such as db) to work
