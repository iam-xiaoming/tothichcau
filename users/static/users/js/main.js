document.addEventListener('DOMContentLoaded', function () {
    // 1. Tab switching
    const tabItems = document.querySelectorAll('.tab-item');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabItems.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active from all
            tabItems.forEach(t => t.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            // Activate clicked tab
            tab.classList.add('active');
            const tabId = tab.getAttribute('data-tab').toLowerCase();
            const activePane = document.getElementById(tabId);
            if (activePane) activePane.classList.add('active');
        });
    });

    // 2. Copy game key
    document.querySelectorAll('.copy-key').forEach(btn => {
        btn.addEventListener('click', () => {
            const key = btn.getAttribute('data-key');
            navigator.clipboard.writeText(key).then(() => {
                alert('Copied: ' + key);
            });
        });
    });

    // 3. Preview uploaded profile image
    const imageInput = document.getElementById('profile-image-upload');
    if (imageInput) {
        imageInput.addEventListener('change', function () {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const img = document.querySelector('.profile-picture-upload img');
                    if (img) {
                        img.src = e.target.result;
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }
});
