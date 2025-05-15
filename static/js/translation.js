// Function to translate text
async function translateText(text, targetLang) {
    try {
        console.log('Starting translation...');
        console.log('Target language:', targetLang);
        console.log('Text length:', text.length);
        console.log('Text sample:', text.substring(0, 100) + '...');

        // Get CSRF token from meta tag
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        console.log('CSRF Token found:', !!csrfToken);
        if (!csrfToken) {
            throw new Error('CSRF token not found');
        }

        console.log('Sending translation request...');
        const response = await fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                texts: [text],
                target_lang: targetLang
            })
        });

        console.log('Response status:', response.status);
        console.log('Response headers:', Object.fromEntries(response.headers.entries()));
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error response:', errorData);
            throw new Error(errorData.error || `Translation request failed: ${response.status}`);
        }

        const data = await response.json();
        console.log('Server response:', data);

        if (data.error) {
            throw new Error(data.error);
        }

        if (!data.translations || !data.translations[0]) {
            throw new Error('No translation received from server');
        }

        return data.translations[0];
    } catch (error) {
        console.error('Translation error:', error);
        console.error('Error stack:', error.stack);
        throw error;
    }
}

// Function to translate multiple elements
async function translateElements(elements, targetLang) {
    try {
        console.log('Starting translation of multiple elements...');
        
        // Get CSRF token from meta tag
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        if (!csrfToken) {
            throw new Error('CSRF token not found');
        }

        // Collect all texts to translate
        const texts = elements.map(element => element.innerHTML);
        console.log(`Collected ${texts.length} texts to translate`);

        console.log('Sending translation request...');
        const response = await fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                texts: texts,
                target_lang: targetLang
            })
        });

        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Translation request failed: ${response.status}`);
        }

        const data = await response.json();
        console.log('Server response:', data);

        if (data.error) {
            throw new Error(data.error);
        }

        if (!data.translations || data.translations.length !== elements.length) {
            throw new Error('Invalid number of translations received');
        }

        // Update elements with translations
        elements.forEach((element, index) => {
            element.innerHTML = data.translations[index];
        });

        return true;
    } catch (error) {
        console.error('Translation error:', error);
        throw error;
    }
}

// Function to create and show translation dropdown
function createTranslationDropdown() {
    const languages = {
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
    };

    const dropdown = document.createElement('div');
    dropdown.className = 'translation-dropdown';
    dropdown.innerHTML = `
        <button class="btn btn-outline-primary" id="translateBtn" type="button">
            <i class="fas fa-language"></i> Translate
        </button>
        <div class="dropdown-content" id="languageDropdown">
            ${Object.entries(languages).map(([code, name]) => `
                <a href="#" data-lang="${code}">${name}</a>
            `).join('')}
        </div>
    `;

    // Add event listeners
    const translateBtn = dropdown.querySelector('#translateBtn');
    const languageDropdown = dropdown.querySelector('#languageDropdown');

    // Toggle dropdown
    translateBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        languageDropdown.classList.toggle('show');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!dropdown.contains(e.target)) {
            languageDropdown.classList.remove('show');
        }
    });

    // Handle language selection
    languageDropdown.addEventListener('click', async (e) => {
        e.preventDefault();
        const langCode = e.target.dataset.lang;
        if (!langCode) return;

        console.log('Selected language:', langCode);

        // Show loading state only for article text
        const loadingHTML = '<div class="translation-loading"><i class="fas fa-spinner fa-spin"></i> Translating...</div>';
        articleText.innerHTML = loadingHTML;
        translateBtn.disabled = true;

        try {
            // Get the original text
            const originalText = articleText.getAttribute('data-original-text') || articleText.innerHTML;
            
            // Store original text if not already stored
            if (!articleText.getAttribute('data-original-text')) {
                articleText.setAttribute('data-original-text', originalText);
            }

            // Translate only the article text
            const translatedText = await translateText(originalText, langCode);
            articleText.innerHTML = translatedText;
            
            // Update button text to show current language
            const languageName = e.target.textContent;
            translateBtn.innerHTML = `<i class="fas fa-language"></i> ${languageName}`;
            console.log('Translation completed successfully');
        } catch (error) {
            console.error('Translation failed:', error);
            // Restore original text
            articleText.innerHTML = articleText.getAttribute('data-original-text');
            alert(`Translation failed: ${error.message}`);
        } finally {
            translateBtn.disabled = false;
            languageDropdown.classList.remove('show');
        }
    });

    return dropdown;
}

// Initialize translation feature when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing translation feature...');
    
    // Create and add translation dropdown
    const articleHeader = document.querySelector('.article-header');
    if (!articleHeader) {
        console.error('Article header not found');
        return;
    }

    const dropdown = createTranslationDropdown();
    articleHeader.appendChild(dropdown);
    
    const translateBtn = document.getElementById('translateBtn');
    const languageDropdown = document.getElementById('languageDropdown');
    const articleText = document.querySelector('.article-text');
    const mainHeading = document.querySelector('.article-header h1');
    
    if (!translateBtn || !languageDropdown || !articleText || !mainHeading) {
        console.error('Required elements not found:', {
            translateBtn: !!translateBtn,
            languageDropdown: !!languageDropdown,
            articleText: !!articleText,
            mainHeading: !!mainHeading
        });
        return;
    }

    console.log('Found all required elements');

    // Store original texts
    const originalTexts = {
        mainHeading: mainHeading.innerHTML,
        article: articleText.innerHTML,
        location: document.querySelector('.location-details')?.innerHTML || '',
        comments: Array.from(document.querySelectorAll('.comment-body')).map(comment => comment.innerHTML),
        headings: Array.from(document.querySelectorAll('.article-header h1, .section-heading h3, .location-details h3')).map(heading => heading.innerHTML)
    };

    console.log('Original texts found:', {
        mainHeading: !!originalTexts.mainHeading,
        article: !!originalTexts.article,
        location: !!originalTexts.location,
        commentsCount: originalTexts.comments.length,
        headingsCount: originalTexts.headings.length
    });

    // Store original texts as data attributes
    mainHeading.setAttribute('data-original-text', originalTexts.mainHeading);
    articleText.setAttribute('data-original-text', originalTexts.article);
    if (document.querySelector('.location-details')) {
        document.querySelector('.location-details').setAttribute('data-original-text', originalTexts.location);
    }
    document.querySelectorAll('.comment-body').forEach((comment, index) => {
        comment.setAttribute('data-original-text', originalTexts.comments[index]);
    });
    document.querySelectorAll('.article-header h1, .section-heading h3, .location-details h3').forEach((heading, index) => {
        heading.setAttribute('data-original-text', originalTexts.headings[index]);
    });

    // Toggle dropdown
    translateBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        languageDropdown.classList.toggle('show');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!languageDropdown.contains(e.target) && e.target !== translateBtn) {
            languageDropdown.classList.remove('show');
        }
    });

    // Handle language selection
    languageDropdown.addEventListener('click', async (e) => {
        e.preventDefault();
        const langCode = e.target.dataset.lang;
        if (!langCode) return;

        console.log('Selected language:', langCode);

        // Show loading state only for article text
        const loadingHTML = '<div class="translation-loading"><i class="fas fa-spinner fa-spin"></i> Translating...</div>';
        articleText.innerHTML = loadingHTML;
        translateBtn.disabled = true;

        try {
            // Get the original text
            const originalText = articleText.getAttribute('data-original-text') || articleText.innerHTML;
            
            // Store original text if not already stored
            if (!articleText.getAttribute('data-original-text')) {
                articleText.setAttribute('data-original-text', originalText);
            }

            // Translate only the article text
            const translatedText = await translateText(originalText, langCode);
            articleText.innerHTML = translatedText;
            
            // Update button text to show current language
            const languageName = e.target.textContent;
            translateBtn.innerHTML = `<i class="fas fa-language"></i> ${languageName}`;
            console.log('Translation completed successfully');
        } catch (error) {
            console.error('Translation failed:', error);
            // Restore original text
            articleText.innerHTML = articleText.getAttribute('data-original-text');
            alert(`Translation failed: ${error.message}`);
        } finally {
            translateBtn.disabled = false;
            languageDropdown.classList.remove('show');
        }
    });
}); 