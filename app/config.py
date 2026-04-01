"""
Configuration settings for Section Tracker application.
"""
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration class."""

    
    # Secret key for session management : 
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'section-tracker-super-secret-key-2024'
    
    # Database configuration (SQLite for local development)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(basedir), 'section_tracker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'ppt', 'pptx'}
    
    # Pagination
    ITEMS_PER_PAGE = 12
    
    # Scoring configuration
    POINTS_PROJECT_UPLOAD = 50
    POINTS_FIVE_STAR_BONUS = 20
    POINTS_NOTE_SHARE = 30
    POINTS_DOWNLOAD_BONUS = 15
    POINTS_DOWNLOAD_THRESHOLD = 10
    POINTS_PER_RUN = 1
    POINTS_PER_WICKET = 10
    POINTS_PER_CATCH = 5
    POINTS_RATING_GIVEN = 5
    POINTS_HELPFUL_MARK = 10
    POINTS_EVENT_PARTICIPATION = 20


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # In production, use environment variables for sensitive data
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
