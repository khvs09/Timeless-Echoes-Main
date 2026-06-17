# 🕰️ Timeless Echoes

A full-stack web application that brings historical stories to life — connecting people with places, memories, and echoes of the past through interactive maps, multilingual translation, and user-contributed stories.

---

## 🌍 About the Project

**Timeless Echoes** is a community-driven platform where users can explore and share historical narratives tied to real-world locations. Stories are pinned to geographic coordinates on an interactive map, and the platform supports multilingual translation so history can be experienced across language barriers.

---

## ✨ Features

- 🗺️ **Interactive Map** — Browse stories pinned to real locations using geocoding and reverse geocoding via OpenStreetMap Nominatim
- 📖 **Story Sharing** — Users can write and submit historical stories tied to specific places
- 🌐 **Multilingual Translation** — Built-in translation support using `deep-translator` so content is accessible in multiple languages
- 🔐 **User Authentication** — Secure login, registration, and session management with Flask-Login
- 📍 **Geocoding API** — Convert place names to coordinates and vice versa
- 🐳 **Docker Support** — Containerized for easy deployment
- 🗄️ **Database Migrations** — Managed with Flask-Migrate

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLAlchemy (SQLite / PostgreSQL) |
| Auth | Flask-Login, Flask-WTF (CSRF) |
| Translation | deep-translator |
| Geocoding | OpenStreetMap Nominatim, geopy |
| Frontend | HTML, CSS, JavaScript, Jinja2 Templates |
| Deployment | Docker, Gunicorn |

---

## 📁 Project Structure

```
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
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/khvs09/Timeless-Echoes-Main.git
cd Timeless-Echoes-Main
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r Requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the root directory:
```env
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///timeless_echoes.db
```

**5. Initialize the database**
```bash
flask db upgrade
```

**6. Run the app**
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## 🐳 Running with Docker

```bash
docker build -t timeless-echoes .
docker run -p 5000:5000 timeless-echoes
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/geocode?location=<name>` | Convert a place name to lat/lon coordinates |
| GET | `/api/reverse_geocode?lat=<lat>&lon=<lon>` | Convert coordinates to a place name |

---

## 📦 Key Dependencies

- `Flask` — Web framework
- `Flask-SQLAlchemy` — Database ORM
- `Flask-Login` — User session management
- `Flask-WTF` — Form handling with CSRF protection
- `Flask-Migrate` — Database schema migrations
- `deep-translator` — Multi-language translation
- `geopy` — Geocoding utilities
- `gunicorn` — Production WSGI server

---

## 👨‍💻 Author

Built by [khvs09](https://github.com/khvs09)

---

## 📄 License

This project is for educational purposes.

