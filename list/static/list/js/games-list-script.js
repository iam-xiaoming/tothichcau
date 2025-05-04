document.addEventListener('DOMContentLoaded', function() {
    // Rating Slider
    const ratingSlider = document.getElementById('rating-slider');
    const sliderValue = document.querySelector('.slider-value');
    
    if (ratingSlider) {
        ratingSlider.addEventListener('input', function() {
            sliderValue.textContent = this.value + '+';
        });
    }
    
    // View Toggle
    const viewButtons = document.querySelectorAll('.view-btn');
    const gamesGrid = document.getElementById('games-grid');
    
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const view = this.getAttribute('data-view');
            
            // Remove active class from all buttons
            viewButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Update grid view
            if (view === 'grid') {
                gamesGrid.classList.remove('list-view');
            } else {
                gamesGrid.classList.add('list-view');
            }
        });
    });
    
    // Wishlist Toggle
    const wishlistButtons = document.querySelectorAll('.btn-wishlist');
    
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.classList.toggle('active');
            
            if (this.classList.contains('active')) {
                this.querySelector('i').classList.remove('far');
                this.querySelector('i').classList.add('fas');
                
                // Show notification
                showNotification('Game added to wishlist!');
            } else {
                this.querySelector('i').classList.remove('fas');
                this.querySelector('i').classList.add('far');
                
                // Show notification
                showNotification('Game removed from wishlist!');
            }
        });
    });
    
    function showNotification(message) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        notification.style.position = 'fixed';
        notification.style.bottom = '20px';
        notification.style.right = '20px';
        notification.style.backgroundColor = 'var(--neon-primary)';
        notification.style.color = 'var(--primary-bg)';
        notification.style.padding = '10px 20px';
        notification.style.borderRadius = '5px';
        notification.style.boxShadow = '0 0 10px var(--neon-primary)';
        notification.style.zIndex = '1000';
        notification.style.opacity = '0';
        notification.style.transform = 'translateY(20px)';
        notification.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        
        // Add to body
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateY(0)';
        }, 10);
        
        // Hide and remove notification
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
    
    // Search Functionality
    const searchInput = document.getElementById('game-search');
    const searchButton = document.getElementById('search-btn');
    const gameCards = document.querySelectorAll('.game-card');
    const gamesTotal = document.getElementById('games-total');
    
    function performSearch() {
        const searchTerm = searchInput.value.toLowerCase();
        let visibleCount = 0;
        
        gameCards.forEach(card => {
            const title = card.querySelector('.game-title').textContent.toLowerCase();
            const description = card.querySelector('.game-description').textContent.toLowerCase();
            
            if (title.includes(searchTerm) || description.includes(searchTerm)) {
                card.style.display = '';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        // Update games count
        gamesTotal.textContent = visibleCount;
        
        // Show message if no results
        if (visibleCount === 0) {
            showNoResults();
        } else {
            hideNoResults();
        }
    }
    
    if (searchButton) {
        searchButton.addEventListener('click', performSearch);
    }
    
    if (searchInput) {
        searchInput.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
    
    function showNoResults() {
        // Check if no results message already exists
        if (!document.querySelector('.no-results')) {
            const noResults = document.createElement('div');
            noResults.className = 'no-results';
            noResults.innerHTML = `
                <div style="text-align: center; padding: 50px 20px;">
                    <i class="fas fa-search" style="font-size: 3rem; color: var(--secondary-text); margin-bottom: 20px;"></i>
                    <h3>No games found</h3>
                    <p>Try adjusting your search or filters to find what you're looking for.</p>
                    <button id="reset-search" class="btn-primary" style="margin-top: 20px;">Reset Search</button>
                </div>
            `;
            
            gamesGrid.appendChild(noResults);
            
            // Add event listener to reset button
            document.getElementById('reset-search').addEventListener('click', function() {
                searchInput.value = '';
                performSearch();
            });
        }
    }
    
    function hideNoResults() {
        const noResults = document.querySelector('.no-results');
        if (noResults) {
            noResults.remove();
        }
    }
    
    // Filter Functionality
    const applyFiltersBtn = document.getElementById('apply-filters');
    const resetFiltersBtn = document.getElementById('reset-filters');
    
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', applyFilters);
    }
    
    if (resetFiltersBtn) {
        resetFiltersBtn.addEventListener('click', resetFilters);
    }
    
    function applyFilters() {
        // Get selected platforms
        const selectedPlatforms = Array.from(document.querySelectorAll('.filter-option input[type="checkbox"]:checked'))
            .filter(checkbox => checkbox.closest('.filter-group').querySelector('h4').textContent === 'Platforms')
            .map(checkbox => checkbox.value);
        
        // Get selected genres
        const selectedGenres = Array.from(document.querySelectorAll('.filter-option input[type="checkbox"]:checked'))
            .filter(checkbox => checkbox.closest('.filter-group').querySelector('h4').textContent === 'Genres')
            .map(checkbox => checkbox.value);
        
        // Get minimum rating
        const minRating = parseFloat(ratingSlider.value);
        
        // Get year range
        const yearFrom = parseInt(document.getElementById('year-from').value);
        const yearTo = parseInt(document.getElementById('year-to').value);
        
        let visibleCount = 0;
        
        // Apply filters to each game card
        gameCards.forEach(card => {
            // Get card data
            const cardPlatforms = card.getAttribute('data-platforms').split(' ');
            const cardGenres = card.getAttribute('data-genres').split(' ');
            const cardRating = parseFloat(card.getAttribute('data-rating'));
            const cardYear = parseInt(card.getAttribute('data-year'));
            
            // Check if card matches all filters
            const platformMatch = selectedPlatforms.length === 0 || 
                                 selectedPlatforms.some(platform => cardPlatforms.includes(platform));
            
            const genreMatch = selectedGenres.length === 0 || 
                              selectedGenres.some(genre => cardGenres.includes(genre));
            
            const ratingMatch = cardRating >= minRating;
            
            const yearMatch = cardYear >= yearFrom && cardYear <= yearTo;
            
            // Show or hide card based on filter matches
            if (platformMatch && genreMatch && ratingMatch && yearMatch) {
                card.style.display = '';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        // Update games count
        gamesTotal.textContent = visibleCount;
        
        // Show message if no results
        if (visibleCount === 0) {
            showNoResults();
        } else {
            hideNoResults();
        }
        
        // Show notification
        showNotification('Filters applied!');
    }
    
    function resetFilters() {
        // Reset platform checkboxes
        document.querySelectorAll('.filter-option input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = false;
        });
        
        // Reset rating slider
        ratingSlider.value = 7;
        sliderValue.textContent = '7+';
        
        // Reset year range
        document.getElementById('year-from').value = '2020';
        document.getElementById('year-to').value = '2023';
        
        // Show all game cards
        gameCards.forEach(card => {
            card.style.display = '';
        });
        
        // Update games count
        gamesTotal.textContent = gameCards.length;
        
        // Hide no results message
        hideNoResults();
        
        // Show notification
        showNotification('Filters reset!');
    }
    
    // Sort Functionality
    const sortSelect = document.getElementById('sort-by');
    
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            const sortValue = this.value;
            const gameCardsArray = Array.from(gameCards);
            
            // Sort game cards based on selected option
            gameCardsArray.sort((a, b) => {
                if (sortValue === 'newest') {
                    const dateA = new Date(a.querySelector('.game-release').textContent.replace('Released: ', ''));
                    const dateB = new Date(b.querySelector('.game-release').textContent.replace('Released: ', ''));
                    return dateB - dateA;
                } else if (sortValue === 'rating') {
                    const ratingA = parseFloat(a.getAttribute('data-rating'));
                    const ratingB = parseFloat(b.getAttribute('data-rating'));
                    return ratingB - ratingA;
                } else if (sortValue === 'name-asc') {
                    const titleA = a.querySelector('.game-title').textContent;
                    const titleB = b.querySelector('.game-title').textContent;
                    return titleA.localeCompare(titleB);
                } else if (sortValue === 'name-desc') {
                    const titleA = a.querySelector('.game-title').textContent;
                    const titleB = b.querySelector('.game-title').textContent;
                    return titleB.localeCompare(titleA);
                }
                
                return 0;
            });
            
            // Reorder game cards in the DOM
            gameCardsArray.forEach(card => {
                gamesGrid.appendChild(card);
            });
            
            // Show notification
            showNotification('Games sorted!');
        });
    }
    
    // Genre Filter
    const genreCards = document.querySelectorAll('.genre-card');
    
    genreCards.forEach(card => {
        card.addEventListener('click', function(e) {
            e.preventDefault();
            
            const genre = this.getAttribute('data-genre');
            
            // Reset all genre checkboxes
            document.querySelectorAll('.filter-option input[value]').forEach(checkbox => {
                if (checkbox.value === genre) {
                    checkbox.checked = true;
                } else {
                    checkbox.checked = false;
                }
            });
            
            // Apply filters
            applyFilters();
            
            // Scroll to games grid
            gamesGrid.scrollIntoView({ behavior: 'smooth' });
        });
    });
    
    // Mobile Filter Toggle
    if (window.innerWidth < 992) {
        // Create filter toggle button
        const filterToggle = document.createElement('button');
        filterToggle.className = 'filter-toggle';
        filterToggle.textContent = 'Filters';
        
        // Insert before filter section
        const filterSection = document.querySelector('.filter-section');
        filterSection.parentNode.insertBefore(filterToggle, filterSection);
        
        // Add event listener
        filterToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            filterSection.classList.toggle('active');
        });
    }
    
    // Animation on scroll
    const animateOnScroll = function() {
        const gameCards = document.querySelectorAll('.game-card');
        
        gameCards.forEach((card, index) => {
            const cardPosition = card.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.2;
            
            if (cardPosition < screenPosition) {
                setTimeout(() => {
                    card.classList.add('animated');
                }, index * 100);
            }
        });
    };
    
    // Set initial state for animated elements
    document.querySelectorAll('.game-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });
    
    // Add animated class
    document.querySelectorAll('.animated').forEach(element => {
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    });
    
    // Run animation on scroll
    window.addEventListener('scroll', animateOnScroll);
    
    // Run animation on initial load
    setTimeout(animateOnScroll, 500);
});