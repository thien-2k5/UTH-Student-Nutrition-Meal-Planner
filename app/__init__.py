# pyrefly: ignore [missing-import]
from flask import Flask, render_template
import logging
from app.config import Config
from app.database import db

logger = logging.getLogger(__name__)

def create_app(config_class=Config):
    """Flask Application Factory."""
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_class)
    
    # Initialize DB
    db.init_app(app)
    
    # Register blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    # Context processor to inject common variables into templates
    @app.context_processor
    def inject_globals():
        return {
            'app_name': 'UTH Nutrition Planner'
        }
    
    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('components/404.html'), 404
        
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('components/500.html'), 500
        
    # Create tables automatically inside application context
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables verified/created successfully.")
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")
            
    return app
