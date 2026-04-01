"""
Section Tracker - Flask Application Factory
CSE-32(B)
"""
import os
from flask import Flask
from flask_login import LoginManager

from .models import db, User
from .config import config


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'অনুগ্রহ করে লগইন করুন।'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))


def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Create upload directories
    upload_dirs = [
        os.path.join(app.config['UPLOAD_FOLDER'], 'profiles'),
        os.path.join(app.config['UPLOAD_FOLDER'], 'projects'),
        os.path.join(app.config['UPLOAD_FOLDER'], 'notes')
    ]
    for directory in upload_dirs:
        os.makedirs(directory, exist_ok=True)
    
    # Register blueprints
    from .routes import auth, dashboard, profile, projects, sports, notes, leaderboard, events, social, public
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(projects.bp)
    app.register_blueprint(sports.bp)
    app.register_blueprint(notes.bp)
    app.register_blueprint(leaderboard.bp)
    app.register_blueprint(events.bp)
    app.register_blueprint(social.bp)
    app.register_blueprint(public.bp)
    
    # Context processors
    @app.context_processor
    def inject_globals():
        """Inject global variables into all templates."""
        return {
            'app_name': 'CSE-32(B)',
            'current_year': 2026
        }
    
    return app

