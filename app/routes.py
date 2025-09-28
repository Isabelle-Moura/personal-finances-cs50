# app/routes.py

from flask import Blueprint

# Creates the Blueprint (the route module). 
# The name 'main' is what __init__.py tries to import.
main = Blueprint('main', __name__)

# Example route, so that Flask does not find the empty module
@main.route('/')
def home():
    return '<h1>Application Loaded Successfully!</h1>'

# The other routes (login, registration, dashboard) will come here