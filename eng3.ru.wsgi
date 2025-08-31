#import sys
import logging

sys.path.insert(0, '/home/vpv/web/eng3.ru/public_html')
sys.path.insert(0, '/home/vpv/web/eng3.ru/public_html/venv/lib/python3.10/site-packages/')

# Set up logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Import and run the Flask app
from app.py import app as application