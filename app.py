from flask import Flask, request, jsonify
from flask_login import LoginManager
from flask_migrate import Migrate
from models import db, User
import os
from flask_wtf.csrf import CSRFProtect
import requests
from urllib.parse import quote

app = Flask(__name__)

# Load configuration from config.py
from config import Config
app.config.from_object(Config)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Add the custom filter for rendering newlines in text
@app.template_filter('better_nl2br')
def better_nl2br(text):
    """
    Convert newlines to <br> tags but handle extra spaces and empty lines properly.
    """
    if not text:
        return ""
    # Replace single newlines with <br> but preserve indentation
    lines = text.split('\n')
    result = ""
    for line in lines:
        if line.strip() == "":  # Empty line
            result += "<br>"
        else:
            # Preserve spaces at start of line by replacing with &nbsp;
            leading_spaces = len(line) - len(line.lstrip())
            if leading_spaces > 0:
                line = "&nbsp;" * leading_spaces + line.lstrip()
            result += line + "<br>"
    # Remove the last <br> if the text doesn't end with a newline
    if not text.endswith('\n'):
        result = result[:-4]
    return result

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/geocode')
def geocode():
    """Geocode a location string to coordinates using Nominatim"""
    location = request.args.get('location', '')
    if not location:
        return jsonify({'error': 'No location provided'}), 400
        
    try:
        # Use Nominatim for geocoding
        url = f'https://nominatim.openstreetmap.org/search?q={quote(location)}&format=json&limit=1'
        headers = {'User-Agent': 'TimelessEchoes/1.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            return jsonify({'error': 'Location not found'}), 404
            
        result = data[0]
        return jsonify({
            'lat': result['lat'],
            'lon': result['lon'],
            'address': {
                'state': result.get('address', {}).get('state'),
                'county': result.get('address', {}).get('county'),
                'village': result.get('address', {}).get('village'),
                'town': result.get('address', {}).get('town'),
                'city': result.get('address', {}).get('city')
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reverse_geocode')
def reverse_geocode():
    """Reverse geocode coordinates to location details using Nominatim"""
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        if not lat or not lon:
            return jsonify({'error': 'Missing coordinates'}), 400
            
        # Use Nominatim for reverse geocoding
        url = f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json'
        headers = {'User-Agent': 'TimelessEchoes/1.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if not data or 'address' not in data:
            return jsonify({'error': 'Location not found'}), 404
            
        return jsonify({
            'address': {
                'state': data['address'].get('state'),
                'county': data['address'].get('county'),
                'village': data['address'].get('village'),
                'town': data['address'].get('town'),
                'city': data['address'].get('city')
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Import routes at the end to avoid circular imports
from routes import *

if __name__ == '__main__':
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
    app.run(debug=True)