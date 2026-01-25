import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env
load_dotenv()

app = create_app()

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    app.run(host="0.0.0.0", port=5000, debug=True)
