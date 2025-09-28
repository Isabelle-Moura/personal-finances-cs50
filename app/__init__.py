from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os
import click 

#1. Load Environment Variables
load_dotenv() 

#2. Initialize Extensions (without associating them with the app yet)
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    #3. Initialize the Flask Application
    app = Flask(__name__)
    
    #4. Configure the Application
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    
    #5. Connect Extensions to the Application
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login' 

    #6. Register Blueprints (Routes)
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #7. Add Custom CLI Commands
    @app.cli.command('create-tables')
    @click.option('--drop/--no-drop', default=False, help="Delete existing tables before creating new tables.")
    def create_tables(drop):
        'Creates all database tables based on the defined models.'
        with app.app_context():
            if drop:
                print('Existing tables are being deleted...')
                db.drop_all()
            
            print('Tables are being created...')
            db.create_all()
            print('Tables successfully created.')

    return app 

#8. Create the Final Instance of the App and DB
app = create_app()

#9. Importing models HERE avoids circular import issues
from app import models