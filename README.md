🕰️ Timeless Echoes

A full-stack web application that brings historical stories to life — connecting people with places, memories, and echoes of the past through interactive maps, multilingual translation, and user-contributed stories.

🌐 Live Demo: https://timeless-echoes.onrender.com


⚠️ Hosted on Render's free tier — may take 30–60 seconds to wake up on first load.




🌍 About the Project

Timeless Echoes is a community-driven platform where users can explore and share historical narratives tied to real-world locations. Stories are pinned to geographic coordinates on an interactive map, and the platform supports multilingual translation so history can be experienced across language barriers.


✨ Features


🗺️ Interactive Map — Browse stories pinned to real locations using geocoding and reverse geocoding via OpenStreetMap Nominatim
📖 Story Sharing — Users can write and submit historical stories tied to specific places
🌐 Multilingual Translation — Built-in translation support using deep-translator so content is accessible in multiple languages
🔐 User Authentication — Secure login, registration, and session management with Flask-Login
📍 Geocoding API — Convert place names to coordinates and vice versa
🐳 Docker Support — Containerized for easy deployment
🗄️ Database Migrations — Managed with Flask-Migrate



🛠️ Tech Stack

LayerTechnologyBackendPython, FlaskDatabaseSQLAlchemy (SQLite / PostgreSQL)AuthFlask-Login, Flask-WTF (CSRF)Translationdeep-translatorGeocodingOpenStreetMap Nominatim, geopyFrontendHTML, CSS, JavaScript, Jinja2 TemplatesDeploymentDocker, Gunicorn


📁 Project Structure

Timeless-Echoes-Main/
├── app.py              # Main Flask application & API routes
├── routes.py           # Page routes and view logic
├── models.py           # Database models (User, Story, etc.)
├── forms.py            # WTForms form definitions
├── config.py           # App configuration
├── templates/          # Jinja2 HTML templates
├── static/             # CSS, JS, images
├── migrations/         # Flask-Migrate database migrations
├── Requirements.txt    # Python dependencies
└── Dockerfile          # Docker container setup


🚀 Getting Started

Try it live: https://timeless-echoes.onrender.com

Or run it locally:

Prerequisites


Python 3.9+
pip


Installation

1. Clone the repository

bashgit clone https://github.com/khvs09/Timeless-Echoes-Main.git
cd Timeless-Echoes-Main

2. Create a virtual environment

bashpython -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

3. Install dependencies

bashpip install -r Requirements.txt

4. Set up environment variables

Create a .env file in the root directory:

envSECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///timeless_echoes.db

5. Initialize the database

bashflask db upgrade

6. Run the app

bashpython app.py

Visit http://localhost:5000 in your browser.


🐳 Running with Docker

bashdocker build -t timeless-echoes .
docker run -p 5000:5000 timeless-echoes


🔌 API Endpoints

MethodEndpointDescriptionGET/geocode?location=<name>Convert a place name to lat/lon coordinatesGET/api/reverse_geocode?lat=<lat>&lon=<lon>Convert coordinates to a place name


📦 Key Dependencies


Flask — Web framework
Flask-SQLAlchemy — Database ORM
Flask-Login — User session management
Flask-WTF — Form handling with CSRF protection
Flask-Migrate — Database schema migrations
deep-translator — Multi-language translation
geopy — Geocoding utilities
gunicorn — Production WSGI server



🌐 Deployment

This project is deployed on Render and accessible at:

👉 https://timeless-echoes.onrender.com

Deployed using Gunicorn as the production WSGI server with Docker containerization.

📄 License

This project is for educational purposes.
