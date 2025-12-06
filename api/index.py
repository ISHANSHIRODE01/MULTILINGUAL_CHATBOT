import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.backend.app import app
