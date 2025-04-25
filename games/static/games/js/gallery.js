// Helper to get CSRF token from cookies
const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            const [key, value] = cookie.trim().split('=');
            if (key === name) {
                cookieValue = decodeURIComponent(value);
            }
        });
    }
    return cookieValue;
};

// Function to update the cart button state
const updateCartButton = (btn, gameId) => {
    fetch(`/api/cart/contains/?game_id=${gameId}`)
        .then(res => res.json())
        .then(data => {
            btn.classList.remove('loading');
            if (data.in_cart) {
                btn.classList.add('disabled');
                btn.querySelector('span').textContent = 'In Cart';
            } else if (data.in_library) {
                btn.classList.add('disabled');
                btn.querySelector('span').textContent = 'In Library';
            } else {
                btn.querySelector('span').textContent = 'Add to Cart';
            }
        })
        .catch(err => {
            console.error(`Error checking cart status for game ${gameId}:`, err);
        });
};

// Function to add an item to the cart
const addToCart = (gameId, btn) => {
    fetch("{% url 'add_to_cart' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: new URLSearchParams({
            'game_id': gameId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.already_in_cart || data.success) {
            btn.classList.add('disabled');
            btn.querySelector('span').textContent = 'In Cart';
        }
        if (data.success) {
            updateCartCount(); // Update cart count
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
};

// Add event listeners to buttons on page load
document.querySelectorAll('.watch-btn').forEach(btn => {
    const gameId = btn.getAttribute('data-game-id');
    
    // Initial status check for each game
    updateCartButton(btn, gameId);

    // Add click event listener to add to cart
    btn.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent default link behavior
        addToCart(gameId, btn);
    });
});

// Function to update gallery media (image/video)
const updateMedia = (src) => {
    const container = document.getElementById('galleryContainer');
    container.innerHTML = ''; // Clear previous content

    const defaultSrc = "{% static 'homepage/img/ac.png' %}";
    src = src || defaultSrc;
    const ext = src.split('.').pop().toLowerCase();
    let element;

    if (['mp4', 'webm', 'ogg'].includes(ext)) {
        element = document.createElement('video');
        element.src = src;
        element.controls = true;
        element.autoplay = true;
        element.loop = true;
        element.style.width = '100%';
        element.style.height = '100%';
        element.style.objectFit = 'cover';
    } else if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext)) {
        element = document.createElement('img');
        element.src = src;
        element.alt = 'Gallery Image';
        element.style.width = '100%';
        element.style.height = '100%';
        element.style.objectFit = 'cover';
    } else {
        element = document.createElement('iframe');
        element.src = src;
        element.frameBorder = '0';
        element.allowFullscreen = true;
        element.style.width = '100%';
        element.style.height = '100%';
    }

    container.appendChild(element);
};

// Function to open gallery modal
const openGallery = () => {
    const modal = document.getElementById('galleryModal');
    modal.classList.remove('hide');
    modal.style.display = 'flex';
    requestAnimationFrame(() => {
        modal.classList.add('show');
    });

    const galleryItems = document.querySelectorAll('.gallery-item');
    const selectedItem = galleryItems[currentIndex];
    if (selectedItem) {
        const src = selectedItem.getAttribute('set-bg');
        updateMedia(src);
    }
};

// Function to close gallery modal
const closeGallery = () => {
    const modal = document.getElementById('galleryModal');
    modal.classList.remove('show');
    modal.classList.add('hide');
    modal.addEventListener('animationend', function handler() {
        modal.style.display = 'none';
        modal.classList.remove('hide');
        modal.removeEventListener('animationend', handler);
    });
};

// Function to create gallery items and set event listeners
const createGalleryItems = () => {
    const videoUrls = [
        'homepage/static/homepage/video/hero.mp4',
        'homepage/static/homepage/video/hero2.mp4'
    ];

    const imageUrls = [
        'https://letsenhance.io/static/73136da51c245e80edc6ccfe44888a99/1015f/MainBefore.jpg',
        'https://letsenhance.io/static/73136da51c245e80edc6ccfe44888a99/1015f/MainBefore.jpg',
        'https://letsenhance.io/static/73136da51c245e80edc6ccfe44888a99/1015f/MainBefore.jpg',
    ];

    const galleryItemsContainer = document.querySelector('.gallery-items');
    const allItems = [...videoUrls, ...imageUrls];

    allItems.forEach((item, index) => {
        const isVideo = item.match(/\.(mp4|webm|ogg)$/i);
        const isImage = item.match(/\.(jpg|jpeg|png|gif|webp)$/i);
        const button = document.createElement('button');
        button.classList.add('gallery-item');
        button.setAttribute('set-bg', item);
        
        if (isVideo) {
            button.textContent = `Video ${index + 1}`;
            const video = document.createElement('video');
            video.src = item;
            video.muted = true;
            video.preload = 'auto';
            video.crossOrigin = 'anonymous';
            video.addEventListener('loadeddata', () => {
                video.currentTime = 1;
            });
            video.addEventListener('seeked', () => {
                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                const thumbnail = canvas.toDataURL('image/jpeg');
                button.style.backgroundImage = `url(${thumbnail})`;
                button.style.backgroundSize = 'cover';
                button.style.backgroundPosition = 'center';
                video.remove();
            });
        } else if (isImage) {
            button.textContent = `Image ${index + 1}`;
            button.style.backgroundImage = `url(${item})`;
            button.style.backgroundSize = 'cover';
            button.style.backgroundPosition = 'center';
            button.style.backgroundRepeat = 'no-repeat';
        }

        galleryItemsContainer.appendChild(button);
    });

    galleryItemsContainer.addEventListener('click', (e) => {
        const clickedItem = e.target;
        if (clickedItem.classList.contains('gallery-item')) {
            const src = clickedItem.getAttribute('set-bg');
            updateMedia(src); 
        }
    });
};


// Initialize gallery items on DOMContentLoaded
document.addEventListener('DOMContentLoaded', createGalleryItems);



let currentIndex = 0;

document.addEventListener("DOMContentLoaded", function () {
    const gallery = document.querySelector('.gallery-items');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    const items = document.querySelectorAll('.gallery-item');

    let currentIndex = 0;

    function getItemWidth() {
        const firstItem = items[0];
        if (!firstItem) return 0;

        const itemWidth = firstItem.offsetWidth;
        const styles = window.getComputedStyle(gallery);
        const gap = parseInt(styles.gap || styles.columnGap || 0);
        return itemWidth + gap;
    }

    function scrollToIndex() {
        const itemWidth = getItemWidth();
        const scrollX = currentIndex * itemWidth;
        gallery.scrollTo({
            left: scrollX,
            behavior: 'smooth'
        });

        updateButtonStates();

        items.forEach((item, index) => {
            if (index === currentIndex) {
                item.classList.add('active-border');
            } else {
                item.classList.remove('active-border');
            }
        });

        const modal = document.getElementById('galleryModal');
        if (modal && modal.classList.contains('show')) {
            const selectedItem = items[currentIndex];
            if (selectedItem) {
                const src = selectedItem.getAttribute('set-bg');
                updateMedia(src);
            }
        }
    }

    function updateButtonStates() {
        const maxIndex = items.length - 1;
        prevBtn.disabled = currentIndex <= 0;
        nextBtn.disabled = currentIndex >= maxIndex;
    }

    nextBtn.addEventListener('click', function () {
        if (currentIndex < items.length - 1) {
            currentIndex++;
            scrollToIndex();
        }
    });

    prevBtn.addEventListener('click', function () {
        if (currentIndex > 0) {
            currentIndex--;
            scrollToIndex();
        }
    });

    window.addEventListener('resize', scrollToIndex);

    scrollToIndex();
});

