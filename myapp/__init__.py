from flask import Flask
from flask_login import LoginManager
from supabase import create_client
from .config import Config

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize Supabase client
    supabase = create_client(
        app.config['SUPABASE_URL'],
        app.config['SUPABASE_KEY']
    )
    
    # Initialize login manager
    login_manager.init_app(app)
    
    # Register blueprints
    from myapp.app import main
    app.register_blueprint(main)
    
    return app