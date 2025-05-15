import os
import json
from flask import render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
import uuid
import logging
import requests
from deep_translator import GoogleTranslator
from urllib.parse import quote

from app import app, db
from models import User, Article, Comment
from forms import (
    LoginForm, RegistrationForm, ArticleForm, CommentForm, SearchForm,
    ChangePasswordForm, DeleteAccountForm
)
from sqlalchemy import or_

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize translator
translator = GoogleTranslator()

# Available languages for translation
LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'bn': 'Bengali',
    'te': 'Telugu',
    'mr': 'Marathi',
    'ta': 'Tamil',
    'ur': 'Urdu',
    'gu': 'Gujarati',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'pa': 'Punjabi',
    'or': 'Odia',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ru': 'Russian',
    'ar': 'Arabic'
}

# Helper functions
def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'gif']

def save_image(file):
    """Save uploaded image and return relative path"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add a unique identifier to prevent filename collisions
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        # Ensure the upload folder exists
        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        # Save the file
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        # Store only the relative path from static folder
        return f"uploads/{unique_filename}"
    return None

# Helper function to generate search form for all templates
def get_search_form():
    return SearchForm(request.args, csrf_enabled=False) if request.args.get('query') else SearchForm(csrf_enabled=False)

# Home page route
@app.route('/')
def index():
    # Get filter parameters if they exist
    state = request.args.get('state', '')
    district = request.args.get('district', '')
    village = request.args.get('village', '')
    page = request.args.get('page', 1, type=int)
    
    # Apply filters if they exist
    query = Article.query
    if state:
        query = query.filter(Article.state == state)
    if district:
        query = query.filter(Article.district == district)
    if village:
        query = query.filter(Article.village == village)
    
    # Paginate the results
    articles = query.order_by(Article.timestamp.desc()).paginate(page=page, per_page=6)
    
    # Get all distinct states for the filter dropdown
    states = db.session.query(Article.state).distinct().all()
    states = [state[0] for state in states if state[0]]  # Filter out None or empty values
    
    # Get districts if state is selected
    districts = []
    if state:
        districts = db.session.query(Article.district).filter(Article.state == state).distinct().all()
        districts = [district[0] for district in districts if district[0]]  # Filter out None or empty values
    
    # Get villages if district is selected
    villages = []
    if district:
        villages = db.session.query(Article.village).filter(Article.district == district).distinct().all()
        villages = [village[0] for village in villages if village[0]]  # Filter out None or empty values
    
    return render_template('index.html', articles=articles, states=states, 
                          districts=districts, villages=villages,
                          selected_state=state, selected_district=district, 
                          selected_village=village, search_form=get_search_form())

# Search route
@app.route('/search')
def search():
    search_form = get_search_form()
    page = request.args.get('page', 1, type=int)
    
    if search_form.validate():
        query_text = search_form.query.data
        
        # Search in title, description, state, district, and village
        search_results = Article.query.filter(
            or_(
                Article.title.ilike(f'%{query_text}%'),
                Article.description.ilike(f'%{query_text}%'),
                Article.state.ilike(f'%{query_text}%'),
                Article.district.ilike(f'%{query_text}%'),
                Article.village.ilike(f'%{query_text}%')
            )
        ).order_by(Article.timestamp.desc()).paginate(page=page, per_page=6)
        
        return render_template('search_results.html', 
                            search_results=search_results, 
                            query=query_text,
                            search_form=search_form)
    
    return redirect(url_for('index'))

# AJAX Search route for autocomplete and instant results
@app.route('/api/search')
def api_search():
    query_text = request.args.get('query', '')
    if not query_text or len(query_text) < 3:
        return jsonify({"results": []})
    
    # Search in title, description, state, district, and village
    search_results = Article.query.filter(
        or_(
            Article.title.ilike(f'%{query_text}%'),
            Article.description.ilike(f'%{query_text}%'),
            Article.state.ilike(f'%{query_text}%'),
            Article.district.ilike(f'%{query_text}%'),
            Article.village.ilike(f'%{query_text}%')
        )
    ).order_by(Article.timestamp.desc()).limit(5).all()
    
    results = []
    for article in search_results:
        results.append({
            'id': article.id,
            'title': article.title,
            'description': article.description[:100] + '...' if len(article.description) > 100 else article.description,
            'image_path': article.image_path if article.image_path else 'uploads/default.jpg',
            'state': article.state,
            'district': article.district,
            'url': url_for('view_article', article_id=article.id)
        })
    
    return jsonify({"results": results})

# User authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form, search_form=get_search_form())

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, search_form=get_search_form())

# Article routes
@app.route('/article/<int:article_id>')
def view_article(article_id):
    article = Article.query.get_or_404(article_id)
    form = CommentForm()
    # Pass the Comment model to the template
    return render_template('article.html', article=article, form=form, Comment=Comment, search_form=get_search_form())

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_article():
    form = ArticleForm()
    if form.validate_on_submit():
        image_path = None
        if form.image.data:
            image_path = save_image(form.image.data)
        
        # Convert latitude and longitude strings to float if they exist
        latitude = None
        longitude = None
        if form.latitude.data and form.longitude.data:
            try:
                latitude = float(form.latitude.data)
                longitude = float(form.longitude.data)
            except ValueError:
                # If conversion fails, we'll just keep them as None
                pass
        
        article = Article(
            title=form.title.data,
            description=form.description.data,
            image_path=image_path,
            state=form.state.data,
            district=form.district.data,
            village=form.village.data,
            address=form.address.data,
            latitude=latitude,
            longitude=longitude,
            author=current_user
        )
        db.session.add(article)
        db.session.commit()
        flash('Your article has been published!')
        return redirect(url_for('index'))
    return render_template('create_article.html', form=form, search_form=get_search_form())

@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)
    
    # Check if the current user is the author of the article
    if article.user_id != current_user.id:
        flash('You can only edit your own articles.')
        return redirect(url_for('view_article', article_id=article_id))
    
    form = ArticleForm()
    
    if form.validate_on_submit():
        article.title = form.title.data
        article.description = form.description.data
        article.state = form.state.data
        article.district = form.district.data
        article.village = form.village.data
        article.address = form.address.data
        
        # Update latitude and longitude if provided
        if form.latitude.data and form.longitude.data:
            try:
                article.latitude = float(form.latitude.data)
                article.longitude = float(form.longitude.data)
            except ValueError:
                # If conversion fails, we'll keep the existing values
                pass
        
        # Handle image update
        if form.image.data:
            image_path = save_image(form.image.data)
            if image_path:
                # Remove the old image if it exists and it's not the default
                if article.image_path and article.image_path != 'uploads/default.jpg':
                    try:
                        old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], article.image_path.split('/')[-1])
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                    except Exception as e:
                        logger.error(f"Error removing old image: {str(e)}")
                
                article.image_path = image_path
        
        db.session.commit()
        flash('Your article has been updated!')
        return redirect(url_for('view_article', article_id=article_id))
    
    # Pre-populate the form with existing article data
    elif request.method == 'GET':
        form.title.data = article.title
        form.description.data = article.description
        form.state.data = article.state
        form.district.data = article.district
        form.village.data = article.village
        form.address.data = article.address
        if article.latitude and article.longitude:
            form.latitude.data = article.latitude
            form.longitude.data = article.longitude
    
    return render_template('edit_article.html', form=form, article=article, search_form=get_search_form())

@app.route('/article/<int:article_id>/comment', methods=['POST'])
@login_required
def add_comment(article_id):
    article = Article.query.get_or_404(article_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            body=form.body.data,
            author=current_user,
            article=article
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!')
    return redirect(url_for('view_article', article_id=article_id))

@app.route('/article/<int:article_id>/delete', methods=['POST'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    
    # Check if the current user is the author
    if article.user_id != current_user.id:
        flash('You can only delete your own articles.')
        return redirect(url_for('view_article', article_id=article_id))
    
    # Delete image file if exists
    if article.image_path and article.image_path != 'uploads/default.jpg':
        try:
            old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], article.image_path.split('/')[-1])
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
        except Exception as e:
            logger.error(f"Error removing image during article deletion: {str(e)}")
    
    # Delete article (will cascade delete comments)
    db.session.delete(article)
    db.session.commit()
    
    flash('Your article has been deleted.')
    return redirect(url_for('index'))

# API routes for location filters
@app.route('/get_districts')
def get_districts():
    state = request.args.get('state')
    districts = db.session.query(Article.district).filter(Article.state == state).distinct().all()
    districts = [district[0] for district in districts if district[0]]  # Filter out None or empty values
    return jsonify({'districts': districts})

@app.route('/get_villages')
def get_villages():
    district = request.args.get('district')
    villages = db.session.query(Article.village).filter(Article.district == district).distinct().all()
    villages = [village[0] for village in villages if village[0]]  # Filter out None or empty values
    return jsonify({'villages': villages})

@app.route('/profile')
@login_required
def profile():
    user_articles = Article.query.filter_by(user_id=current_user.id).order_by(Article.timestamp.desc()).all()
    return render_template('profile.html', articles=user_articles, search_form=get_search_form())

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    password_form = ChangePasswordForm()
    delete_form = DeleteAccountForm()
    
    if password_form.submit.data and password_form.validate_on_submit():
        # Change password logic
        if not current_user.check_password(password_form.current_password.data):
            flash('Current password is incorrect', 'error')
            return redirect(url_for('settings'))
            
        current_user.set_password(password_form.new_password.data)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('settings'))
        
    if delete_form.submit.data and delete_form.validate_on_submit():
        # Delete account logic
        if not current_user.check_password(delete_form.confirmation.data):
            flash('Password is incorrect', 'error')
            return redirect(url_for('settings'))
            
        # Delete all user content
        articles = Article.query.filter_by(user_id=current_user.id).all()
        for article in articles:
            # Delete associated image files
            if article.image_path and article.image_path != 'uploads/default.jpg':
                try:
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], article.image_path.split('/')[-1])
                    if os.path.exists(image_path):
                        os.remove(image_path)
                except Exception as e:
                    logger.error(f"Error removing image: {str(e)}")
            
            # Note: Comments will be cascade deleted with the Article
        
        user_id = current_user.id
        logout_user()  # Log the user out first
        
        # Then delete the user account
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        
        flash('Your account has been permanently deleted.', 'info')
        return redirect(url_for('index'))
        
    return render_template('settings.html', 
                          password_form=password_form, 
                          delete_form=delete_form,
                          search_form=get_search_form())

@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.json
        logger.info(f"Received translation request: {data}")
        
        if not data or 'texts' not in data or 'target_lang' not in data:
            logger.error("Invalid request parameters")
            return jsonify({'error': 'Invalid request parameters'}), 400
        
        texts = data['texts']
        target_lang = data['target_lang']
        
        # Check if inputs are valid
        if not isinstance(texts, list) or not all(isinstance(text, str) for text in texts):
            logger.error("Invalid texts format")
            return jsonify({'error': 'Texts must be a list of strings'}), 400
        
        if not isinstance(target_lang, str) or len(target_lang) != 2:
            logger.error(f"Invalid target language: {target_lang}")
            return jsonify({'error': 'Target language must be a 2-letter language code'}), 400
        
        # Validate target language code
        if target_lang not in LANGUAGES:
            logger.error(f"Unsupported language code: {target_lang}")
            return jsonify({'error': f'Invalid language code: {target_lang}'}), 400
        
        translations = []
        
        for i, text in enumerate(texts):
            # Skip translation if text is empty
            if not text or text.strip() == '':
                logger.info(f"Skipping empty text at index {i}")
                translations.append('')
                continue
            
            try:
                logger.info(f"Translating text {i}: '{text[:100]}...' to {target_lang}")
                # Create a new translator instance for each translation
                translator = GoogleTranslator(source='auto', target=target_lang)
                translated_text = translator.translate(text)
                if not translated_text:
                    raise Exception("Empty translation received")
                logger.info(f"Translation {i} successful: '{translated_text[:100]}...'")
                translations.append(translated_text)
            except Exception as e:
                logger.error(f"Error translating text {i}: {str(e)}")
                return jsonify({'error': f'Translation failed: {str(e)}'}), 500
        
        response = {'translations': translations}
        logger.info(f"Sending response with {len(translations)} translations")
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return jsonify({'error': 'Translation failed', 'details': str(e)}), 500

@app.route('/api/validate_coordinates', methods=['POST'])
def validate_coordinates():
    """Validate coordinates are within valid ranges"""
    data = request.get_json()
    lat = data.get('latitude')
    lng = data.get('longitude')
    
    if lat is None or lng is None:
        return jsonify({'error': 'Coordinates required'}), 400
    
    try:
        lat = float(lat)
        lng = float(lng)
        
        if -90 <= lat <= 90 and -180 <= lng <= 180:
            return jsonify({'valid': True})
        return jsonify({'valid': False, 'error': 'Coordinates out of range'})
        
    except ValueError:
        return jsonify({'valid': False, 'error': 'Invalid coordinate format'})

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', search_form=get_search_form()), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', search_form=get_search_form()), 500

# Language list route for translation feature
@app.route('/languages')
def get_languages():
    return jsonify(LANGUAGES)