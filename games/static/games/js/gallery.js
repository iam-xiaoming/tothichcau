const imageUrls = [];
const videoUrls = [];

fetch(`/api/game/${pk}/media/review/`)
    .then(response => response.json())
    .then(data => {
        const imageReviews = data.game_image_reviews || [];
        const videoReviews = data.game_video_reviews || [];

        imageReviews.forEach(img => {
            if (img.image) {
                imageUrls.push(img.image);
            }
        });

        videoReviews.forEach(vid => {
            if (vid.video) {
                videoUrls.push(vid.video);
            }
        });

        console.log('Images:', imageUrls);
        console.log('Videos:', videoUrls);

        createGalleryItems();
    })
    .catch(error => console.error('Error:', error));

let currentIndex = 0;
let items = [];

function updateMedia(src) {
    const container = document.getElementById('galleryContainer');
    container.innerHTML = '';

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
        element.style.objectFit = 'contain';
        element.style.background = '#000'
    } else if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext)) {
        element = document.createElement('img');
        element.src = src;
        element.alt = 'Gallery Image';
        element.style.width = '100%';
        element.style.height = '100%';
        element.style.objectFit = 'contain';
    } else {
        element = document.createElement('iframe');
        element.src = src;
        element.frameBorder = '0';
        element.allowFullscreen = true;
        element.style.width = '100%';
        element.style.height = '100%';
    }

    container.appendChild(element);
}

function getItemWidth() {
    const gallery = document.querySelector('.gallery-items');
    const firstItem = items[0];
    if (!firstItem) return 0;

    const itemWidth = firstItem.offsetWidth;
    const styles = window.getComputedStyle(gallery);
    const gap = parseInt(styles.gap || styles.columnGap || 0);
    return itemWidth + gap;
}

function scrollToIndex() {
    const gallery = document.querySelector('.gallery-items');
    const itemWidth = getItemWidth();
    const scrollX = currentIndex * itemWidth;
    gallery.scrollTo({
        left: scrollX,
        behavior: 'smooth'
    });

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

    updateButtonStates();
}

function updateButtonStates() {
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    const maxIndex = items.length - 1;
    prevBtn.disabled = currentIndex <= 0;
    nextBtn.disabled = currentIndex >= maxIndex;
}

function createGalleryItems() {
    const galleryItemsContainer = document.querySelector('.gallery-items');
    const allItems = [...videoUrls, ...imageUrls];

    allItems.forEach((item, index) => {
        const isVideo = item.match(/\.(mp4|webm|ogg)$/i);
        const isImage = item.match(/\.(jpg|jpeg|png|gif|webp)$/i);
        const button = document.createElement('button');
        button.classList.add('gallery-item');
        button.setAttribute('set-bg', item);

        if (isVideo) {
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
            button.style.backgroundImage = `url(${item})`;
            button.style.backgroundSize = 'cover';
            button.style.backgroundPosition = 'center';
            button.style.backgroundRepeat = 'no-repeat';
        }

        galleryItemsContainer.appendChild(button);
    });

    items = document.querySelectorAll('.gallery-item');

    items.forEach((item, index) => {
        item.addEventListener('click', () => {
            currentIndex = index;
            scrollToIndex();
            openGallery();
        });
    });

    currentIndex = 0
    scrollToIndex();
}

function openGallery() {
    const modal = document.getElementById('galleryModal');
    modal.classList.remove('hide');
    modal.style.display = 'flex';
    document.body.classList.add('no-scroll');
    requestAnimationFrame(() => {
        modal.classList.add('show');
    });

    const selectedItem = items[currentIndex];
    if (selectedItem) {
        const src = selectedItem.getAttribute('set-bg');
        updateMedia(src);
    }
}

function closeGallery() {
    const modal = document.getElementById('galleryModal');
    modal.classList.remove('show');
    modal.classList.add('hide');
    
    const videoElement = document.querySelector('#galleryContainer video');
    if (videoElement) {
        videoElement.pause();
        videoElement.currentTime = 0;
    }

    modal.addEventListener('animationend', function handler() {
        modal.style.display = 'none';
        modal.classList.remove('hide');
        modal.removeEventListener('animationend', handler);
    });
}


document.addEventListener("DOMContentLoaded", function () {

    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');

    prevBtn.addEventListener('click', function () {
        if (currentIndex > 0) {
            currentIndex--;
            scrollToIndex();
        }
    });

    nextBtn.addEventListener('click', function () {
        if (currentIndex < items.length - 1) {
            currentIndex++;
            scrollToIndex();
        }
    });

    window.addEventListener('resize', scrollToIndex);
});
