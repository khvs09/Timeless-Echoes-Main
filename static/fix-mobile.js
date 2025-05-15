// Mobile card fix script
(function() {
    // Only run on mobile
    if (window.innerWidth <= 768) {
        console.log("Applying mobile article card fixes");
        
        // Find all article cards
        const articleCards = document.querySelectorAll('.article-card');
        if (articleCards.length > 0) {
            console.log("Found " + articleCards.length + " cards to fix");
            
            // Apply fixes to each card
            articleCards.forEach(function(card) {
                // Force horizontal layout
                card.setAttribute('style', 'display: flex !important; flex-direction: row !important; height: 130px !important; overflow: hidden !important; margin-bottom: 10px !important;');
                
                // Fix image wrapper
                const imageWrapper = card.querySelector('.article-image-wrapper');
                if (imageWrapper) {
                    imageWrapper.setAttribute('style', 'width: 40% !important; min-width: 120px; height: 130px !important; position: relative; overflow: hidden;');
                    
                    // Fix image
                    const img = imageWrapper.querySelector('img');
                    if (img) {
                        img.setAttribute('style', 'width: 100% !important; height: 100% !important; object-fit: cover !important;');
                    }
                    
                    // Fix location badge
                    const location = imageWrapper.querySelector('.article-location');
                    if (location) {
                        location.setAttribute('style', 'position: absolute; bottom: 0; left: 0; width: 100%; background: linear-gradient(to top, rgba(0,0,0,0.7), transparent); padding: 20px 8px 6px; color: white; font-size: 12px;');
                    }
                }
                
                // Fix content
                const content = card.querySelector('.article-content');
                if (content) {
                    content.setAttribute('style', 'width: 60% !important; padding: 10px 15px !important; display: flex !important; flex-direction: column !important; justify-content: space-between !important;');
                    
                    // Fix title
                    const title = content.querySelector('h3');
                    if (title) {
                        title.setAttribute('style', 'font-size: 16px !important; line-height: 1.3; margin: 0 0 5px 0 !important; max-height: 42px; overflow: hidden;');
                    }
                    
                    // Hide excerpt
                    const excerpt = content.querySelector('.article-excerpt');
                    if (excerpt) {
                        excerpt.setAttribute('style', 'display: none !important;');
                    }
                    
                    // Fix read more link
                    const readMore = content.querySelector('.read-more');
                    if (readMore) {
                        readMore.setAttribute('style', 'font-size: 14px; color: #FF7F50; font-weight: 500; margin-top: auto;');
                    }
                }
            });
        }
    }
})(); 