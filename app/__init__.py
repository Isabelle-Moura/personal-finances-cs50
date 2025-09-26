from flask import Flask # 1. Import the main Flask class
from flask_sqlalchemy import SQLAlchemy # 2. Import the database tool
from flask_login import LoginManager # 3. Import the login management tool
from dotenv import load_dotenv # 4. Imports the tool to read .env files
import os # 5. Imports the native module to interact with the operating system

# 1. Load Environment Variables
load_dotenv() # 6. Reads your .env and .flaskenv, making variables (such as SECRET_KEY) accessible.

# 2. Initialize Extensions (without associating with the app yet)
db = SQLAlchemy() # 7. Create the database object (without knowing which app to use yet)
login_manager = LoginManager() # 8. Creates the object that will manage user sessions

def create_app():
    # 3. Initialize the Flask Application
    app = Flask(__name__) # 9. Creates the main instance of the Flask application.

    # 4. Configure the Application
    # Use the SECRET_KEY from the .env file
    app.config[‘SECRET_KEY’] = os.environ.get(‘SECRET_KEY’) # 10. Configure Flask's secret key, crucial for session security.

    # Use the DATABASE_URL from the .env file
    app.config[‘SQLALCHEMY_DATABASE_URI’] = os.environ.get(‘DATABASE_URL’) # 11. Tells SQLAlchemy where your PostgreSQL database is located.
    app.config[‘SQLALCHEMY_TRACK_MODIFICATIONS’] = False # 12. Disables an old feature that is no longer needed, making the code cleaner.

    # 5. Connect Extensions to the Application
    db.init_app(app) # 13. Finally, connect the database object (db) to the application (app).
    login_manager.init_app(app) # 14. Connect the login manager (login_manager) to the application.

    # Configure where Flask-Login should redirect the user to log in
    login_manager.login_view = ‘main.login’ # 15. Tells Flask-Login which route to send the user to when they try to access a protected page without being logged in.

    # 6. Register Blueprints (Routes)
    # Blueprints are modules that organize routes and functions into smaller parts.
    from app.routes import main as main_blueprint # 16. Import the ‘main’ variable from your routes.py and call it main_blueprint.
    app.register_blueprint(main_blueprint) # 17. Add all routes from main_blueprint to your main Flask application.

    return app # 18. Return the application instance, now fully configured.

# 7. Create the Final Instance of the App and DB
app = create_app() # 19. Call the function to create the final ‘app’ object.

# Importing models HERE avoids circular import issues
from app import models # 20. Import the models.py file. This needs to be done here so that models.py can use the ‘db’ variable correctly.