document.addEventListener('DOMContentLoaded', function() {
    // Image Upload Functionality
    const imageUploadArea = document.getElementById('image-upload-area');
    const imageInput = document.getElementById('post-featured-image');
    const imagePreview = document.getElementById('image-preview');
    
    imageUploadArea.addEventListener('click', function() {
        imageInput.click();
    });
    
    imageUploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        imageUploadArea.style.borderColor = var('--neon-primary');
        imageUploadArea.style.backgroundColor = 'rgba(0, 242, 255, 0.1)';
    });
    
    imageUploadArea.addEventListener('dragleave', function() {
        imageUploadArea.style.borderColor = 'rgba(255, 255, 255, 0.2)';
        imageUploadArea.style.backgroundColor = 'transparent';
    });
    
    imageUploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        imageUploadArea.style.borderColor = 'rgba(255, 255, 255, 0.2)';
        imageUploadArea.style.backgroundColor = 'transparent';
        
        if (e.dataTransfer.files.length) {
            imageInput.files = e.dataTransfer.files;
            displayImagePreview(e.dataTransfer.files[0]);
        }
    });
    
    imageInput.addEventListener('change', function() {
        if (this.files.length) {
            displayImagePreview(this.files[0]);
        }
    });
    
    function displayImagePreview(file) {
        if (!file.type.match('image.*')) {
            alert('Please select an image file');
            return;
        }
        
        const reader = new FileReader();
        
        reader.onload = function(e) {
            imageUploadArea.style.display = 'none';
            imagePreview.style.display = 'block';
            imagePreview.innerHTML = `
                <img src="${e.target.result}" alt="Featured Image">
                <div class="remove-image" id="remove-image">
                    <i class="fas fa-times"></i>
                </div>
            `;
            
            document.getElementById('remove-image').addEventListener('click', function() {
                imageInput.value = '';
                imagePreview.style.display = 'none';
                imagePreview.innerHTML = '';
                imageUploadArea.style.display = 'block';
            });
        };
        
        reader.readAsDataURL(file);
    }
    
    // Additional Images Functionality
    const additionalImageUpload = document.getElementById('additional-image-upload');
    const additionalImagesInput = document.getElementById('additional-images');
    const additionalImagesPreview = document.getElementById('additional-images-preview');
    
    additionalImageUpload.addEventListener('click', function() {
        additionalImagesInput.click();
    });
    
    additionalImagesInput.addEventListener('change', function() {
        if (this.files.length) {
            displayAdditionalImages(this.files);
        }
    });
    
    function displayAdditionalImages(files) {
        for (let i = 0; i < files.length; i++) {
            if (!files[i].type.match('image.*')) {
                continue;
            }
            
            const reader = new FileReader();
            const imageIndex = Date.now() + i; // Unique ID for each image
            
            reader.onload = function(e) {
                const imageItem = document.createElement('div');
                imageItem.className = 'additional-image-item';
                imageItem.dataset.index = imageIndex;
                
                imageItem.innerHTML = `
                    <img src="${e.target.result}" alt="Additional Image">
                    <div class="remove-additional-image" data-index="${imageIndex}">
                        <i class="fas fa-times"></i>
                    </div>
                `;
                
                additionalImagesPreview.appendChild(imageItem);
                
                document.querySelector(`.remove-additional-image[data-index="${imageIndex}"]`).addEventListener('click', function() {
                    document.querySelector(`.additional-image-item[data-index="${this.dataset.index}"]`).remove();
                });
            };
            
            reader.readAsDataURL(files[i]);
        }
    }
    
    // Rich Text Editor Functionality
    const toolbarButtons = document.querySelectorAll('.toolbar-btn');
    const editor = document.getElementById('editor');
    const hiddenContent = document.getElementById('post-content');
    
    toolbarButtons.forEach(button => {
        button.addEventListener('click', function() {
            const command = this.dataset.command;
            
            if (command === 'h2' || command === 'h3' || command === 'p') {
                document.execCommand('formatBlock', false, command);
            } else if (command === 'createLink') {
                const url = prompt('Enter the link URL:');
                if (url) document.execCommand(command, false, url);
            } else if (command === 'insertImage') {
                const url = prompt('Enter the image URL:');
                if (url) document.execCommand(command, false, url);
            } else if (command === 'code') {
                document.execCommand('insertHTML', false, '<pre><code>' + getSelectionText() + '</code></pre>');
            } else if (command === 'blockquote') {
                document.execCommand('formatBlock', false, 'blockquote');
            } else {
                document.execCommand(command, false, null);
            }
            
            // Update hidden content field
            updateHiddenContent();
        });
    });
    
    function getSelectionText() {
        let text = '';
        if (window.getSelection) {
            text = window.getSelection().toString();
        }
        return text || '';
    }
    
    editor.addEventListener('input', updateHiddenContent);
    
    function updateHiddenContent() {
        hiddenContent.value = editor.innerHTML;
    }
    
    // Character Counter for Excerpt
    const excerptField = document.getElementById('post-excerpt');
    const excerptCounter = document.getElementById('excerpt-counter');
    
    excerptField.addEventListener('input', function() {
        const count = this.value.length;
        excerptCounter.textContent = count;
        
        if (count > 180) {
            excerptCounter.style.color = '#ff9800';
        } else {
            excerptCounter.style.color = 'var(--secondary-text)';
        }
    });
    
    // Preview Functionality
    const previewButton = document.getElementById('preview-post');
    const previewModal = document.getElementById('preview-modal');
    const closePreview = document.getElementById('close-preview');
    const editPost = document.getElementById('edit-post');
    const confirmPublish = document.getElementById('confirm-publish');
    
    previewButton.addEventListener('click', function() {
        // Get form values
        const title = document.getElementById('post-title').value || 'Your Post Title';
        const category = document.getElementById('post-category');
        const categoryText = category.options[category.selectedIndex]?.text || 'Category';
        const categoryValue = category.value || 'pc';
        const content = editor.innerHTML || '<p>Your post content will appear here...</p>';
        const featuredImage = imagePreview.querySelector('img')?.src || '/placeholder.svg?height=400&width=800';
        const tags = document.getElementById('post-tags').value;
        
        // Update preview
        document.getElementById('preview-title').textContent = title;
        document.getElementById('preview-category').textContent = categoryText;
        document.getElementById('preview-category').className = `preview-category ${categoryValue}`;
        document.getElementById('preview-content').innerHTML = content;
        document.getElementById('preview-featured-image').innerHTML = `<img src="${featuredImage}" alt="${title}">`;
        
        // Update tags
        const tagsContainer = document.getElementById('preview-tags');
        tagsContainer.innerHTML = '';
        
        if (tags) {
            const tagArray = tags.split(',').map(tag => tag.trim());
            tagArray.forEach(tag => {
                if (tag) {
                    const tagSpan = document.createElement('span');
                    tagSpan.className = 'preview-tag';
                    tagSpan.textContent = tag.startsWith('#') ? tag : `#${tag}`;
                    tagsContainer.appendChild(tagSpan);
                }
            });
        } else {
            const tagSpan = document.createElement('span');
            tagSpan.className = 'preview-tag';
            tagSpan.textContent = '#Gaming';
            tagsContainer.appendChild(tagSpan);
        }
        
        // Show modal
        previewModal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    });
    
    closePreview.addEventListener('click', closePreviewModal);
    editPost.addEventListener('click', closePreviewModal);
    
    function closePreviewModal() {
        previewModal.style.display = 'none';
        document.body.style.overflow = '';
    }
    
    function validateForm() {
        const title = document.getElementById('post-title').value;
        const category = document.getElementById('post-category').value;
        const excerpt = document.getElementById('post-excerpt').value;
        const content = hiddenContent.value;
        
        if (!title) {
            alert('Please enter a post title');
            return false;
        }
        
        if (!category) {
            alert('Please select a category');
            return false;
        }
        
        if (!excerpt) {
            alert('Please enter a short excerpt');
            return false;
        }
        
        if (!content || content === '<p></p>' || content === '<br>') {
            alert('Please enter some content for your post');
            return false;
        }
        
        return true;
    }
});