document.addEventListener('DOMContentLoaded', function() {

    const currentUrl = window.location.href;

    // Hàm mở popup
    function openSharePopup(url) {
        window.open(url, 'share-window', 'width=600,height=400');
    }

    // Facebook
    document.querySelector('.share-button.facebook').addEventListener('click', function (e) {
        e.preventDefault();
        const url = 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(currentUrl);
        openSharePopup(url);
    });

    // Twitter
    document.querySelector('.share-button.twitter').addEventListener('click', function (e) {
        e.preventDefault();
        const text = document.title;
        const url = 'https://twitter.com/intent/tweet?url=' + encodeURIComponent(currentUrl) + '&text=' + encodeURIComponent(text);
        openSharePopup(url);
    });

    // Reddit
    document.querySelector('.share-button.reddit').addEventListener('click', function (e) {
        e.preventDefault();
        const url = 'https://www.reddit.com/submit?url=' + encodeURIComponent(currentUrl);
        openSharePopup(url);
    });

    // LinkedIn
    document.querySelector('.share-button.linkedin').addEventListener('click', function (e) {
        e.preventDefault();
        const title = document.title;
        const url = 'https://www.linkedin.com/shareArticle?mini=true&url=' + encodeURIComponent(currentUrl) + '&title=' + encodeURIComponent(title);
        openSharePopup(url);
    });


    // Copy Link Functionality
    const copyLinkBtn = document.getElementById('copy-link');
    const copyLinkBtnBottom = document.getElementById('copy-link-bottom');
    
    function copyCurrentUrl() {
        const url = window.location.href;
        navigator.clipboard.writeText(url).then(() => {
            // Show tooltip or notification
            showCopyNotification(this);
        }).catch(err => {
            console.error('Could not copy text: ', err);
        });
    }
    
    function showCopyNotification(button) {
        // Create tooltip element
        const tooltip = document.createElement('div');
        tooltip.className = 'copy-tooltip';
        tooltip.textContent = 'Link copied!';
        tooltip.style.position = 'absolute';
        tooltip.style.backgroundColor = 'var(--neon-primary)';
        tooltip.style.color = 'var(--primary-bg)';
        tooltip.style.padding = '5px 10px';
        tooltip.style.borderRadius = '4px';
        tooltip.style.fontSize = '0.8rem';
        tooltip.style.zIndex = '100';
        tooltip.style.opacity = '0';
        tooltip.style.transition = 'opacity 0.3s ease';
        
        // Position the tooltip
        document.body.appendChild(tooltip);
        const buttonRect = button.getBoundingClientRect();
        tooltip.style.top = (buttonRect.top - tooltip.offsetHeight - 10) + 'px';
        tooltip.style.left = (buttonRect.left + buttonRect.width/2 - tooltip.offsetWidth/2) + 'px';
        
        // Show and hide the tooltip
        setTimeout(() => {
            tooltip.style.opacity = '1';
        }, 10);
        
        setTimeout(() => {
            tooltip.style.opacity = '0';
            setTimeout(() => {
                document.body.removeChild(tooltip);
            }, 300);
        }, 2000);
    }
    
    if (copyLinkBtn) {
        copyLinkBtn.addEventListener('click', function(e) {
            e.preventDefault();
            copyCurrentUrl.call(this);
        });
    }
    
    if (copyLinkBtnBottom) {
        copyLinkBtnBottom.addEventListener('click', function(e) {
            e.preventDefault();
            copyCurrentUrl.call(this);
        });
    }
    
    // Comment Like Functionality
    const likeButtons = document.querySelectorAll('.comment-like');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();


            const likeCount = this.querySelector('span');
            const currentLikes = parseInt(likeCount.textContent);


            let action = null;
            const comment_pk = this.getAttribute('comment-pk')

            if (this.classList.contains('liked')) {
                action = 'unlike'
            } else {
                action = 'liked';
            }

            fetch('/post/comment/reaction/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    action: action,
                    comment_pk: comment_pk
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log(data.message);
                } else {
                    console.log(data.error);
                }
            });
                        
            // Toggle like state
            if (this.classList.contains('liked')) {
                this.classList.remove('liked');
                likeCount.textContent = currentLikes - 1;
                
            } else {
                this.classList.add('liked');
                likeCount.textContent = currentLikes + 1;
                
                // Add animation effect
                const heart = document.createElement('i');
                heart.className = 'fas fa-heart heart-animation';
                heart.style.position = 'absolute';
                heart.style.color = '#ff3366';
                heart.style.fontSize = '1.5rem';
                heart.style.opacity = '0';
                heart.style.transition = 'all 0.5s ease';
                
                this.style.position = 'relative';
                this.appendChild(heart);
                
                setTimeout(() => {
                    heart.style.transform = 'translateY(-20px)';
                    heart.style.opacity = '1';
                }, 10);
                
                setTimeout(() => {
                    heart.style.opacity = '0';
                    setTimeout(() => {
                        this.removeChild(heart);
                    }, 500);
                }, 800);
            }
        });
    });


    const likePostButton = document.getElementById('like-post-bottom');

    likePostButton.addEventListener('click', function(e) {
        e.preventDefault();

        let action = null;
        if (this.classList.contains('post_liked')) {
            action = 'unlike'
        } else {
            action = 'liked';
        }

        fetch('/post/reaction/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                action: action,
                post_pk: post_pk
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log(data.message);
            } else {
                console.log(data.error);
            }
        });
        
        
        if (this.classList.contains('post_liked')) {
            this.classList.remove('post_liked');
        } else {
            this.classList.add('post_liked');
            
            // animation
            const heart = document.createElement('i');
            heart.className = 'fas fa-heart heart-animation';
            heart.style.position = 'absolute';
            heart.style.color = '#ff3366';
            heart.style.fontSize = '1.5rem';
            heart.style.opacity = '0';
            heart.style.transition = 'all 0.5s ease';
            
            this.style.position = 'relative';
            this.appendChild(heart);
            
            setTimeout(() => {
                heart.style.transform = 'translateY(-20px)';
                heart.style.opacity = '1';
            }, 10);
            
            setTimeout(() => {
                heart.style.opacity = '0';
                setTimeout(() => {
                    this.removeChild(heart);
                }, 500);
            }, 800);
        }
    });
    
    // Highlight code blocks (if any)
    const codeBlocks = document.querySelectorAll('pre code');
    let hljs; // Declare hljs
    if (codeBlocks.length) {
        // Check if hljs is available globally
        if (typeof window.hljs !== 'undefined') {
            hljs = window.hljs;
        } else {
            // If not, attempt to import it (assuming it's available as a module)
            try {
                hljs = require('highlight.js');
            } catch (error) {
                console.warn('highlight.js not found. Code highlighting will be disabled.');
                hljs = null; // Ensure hljs is null if import fails
            }
        }

        if (hljs) {
            codeBlocks.forEach(block => {
                hljs.highlightBlock(block);
            });
        }
    }
    
    // Add animation to elements when they come into view
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.blog-detail-content h2, .blog-detail-image, blockquote, .sidebar-section');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.2;
            
            if (elementPosition < screenPosition) {
                element.classList.add('animated');
            }
        });
    };
    
    // Set initial state for animated elements
    const elementsToAnimate = document.querySelectorAll('.blog-detail-content h2, .blog-detail-image, blockquote, .sidebar-section');
    elementsToAnimate.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
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
    
    // Reading progress indicator
    const progressBar = document.createElement('div');
    progressBar.className = 'reading-progress';
    progressBar.style.position = 'fixed';
    progressBar.style.top = '0';
    progressBar.style.left = '0';
    progressBar.style.height = '3px';
    progressBar.style.background = 'var(--gradient-primary)';
    progressBar.style.width = '0%';
    progressBar.style.zIndex = '1001';
    progressBar.style.transition = 'width 0.1s ease';
    progressBar.style.boxShadow = '0 0 10px var(--neon-primary)';
    
    document.body.appendChild(progressBar);
    
    function updateReadingProgress() {
        const totalHeight = document.body.scrollHeight - window.innerHeight;
        const progress = (window.scrollY / totalHeight) * 100;
        progressBar.style.width = `${progress}%`;
    }
    
    window.addEventListener('scroll', updateReadingProgress);
});