import os
from app import app

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(port=port, debug=True)
