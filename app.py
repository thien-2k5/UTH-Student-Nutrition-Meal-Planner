import os
import logging
from app import create_app

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == "__main__":
    host = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_RUN_PORT", "5001"))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    
    logger.info(f"Starting UTH Nutrition Planner web application on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
