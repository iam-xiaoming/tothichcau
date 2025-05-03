// Gaming-style notification JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const notificationBell = document.querySelector('.notification');
    const notificationDropdown = document.querySelector('.notification-dropdown');
    
    // Make sure both elements exist
    if (!notificationBell || !notificationDropdown) return;
    
    // Create a container for positioning if needed
    const parent = notificationBell.parentNode;
    if (!parent.classList.contains('notification-container')) {
      const container = document.createElement('div');
      container.className = 'notification-container';
      parent.insertBefore(container, notificationBell);
      container.appendChild(notificationBell);
      container.appendChild(notificationDropdown);
    }

    function loadNotifications() {
      fetch('/api/notifications/')
        .then(response => response.json())
        .then(data => {
          const body = document.querySelector('.notification-body');
          if (!body) return;
    
          body.innerHTML = '';
    
          data.notifications.forEach(n => {
            const item = document.createElement('div');
            item.className = 'notification-item';
            item.innerHTML = `
              <div class="notification-item-content">
                <h4>${n.title || 'New Notification'}</h4>
                <p>${n.message}</p>
                <span>${n.timestamp}</span>
              </div>`;
            body.appendChild(item);
          });
          
          updateNotificationCount(data.notifications.length);
        })
        .catch(err => console.error('Error loading notifications:', err));
    }

    loadNotifications();
    

    // Toggle dropdown on click
    notificationBell.addEventListener('click', function(e) {
      e.preventDefault(); // Prevent the default anchor behavior
      
      // Toggle active class
      this.classList.toggle('active');
      
      // Add sound effect (optional)
      if (this.classList.contains('active')) {
        playNotificationSound();
      }
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
      if (!notificationBell.contains(e.target) && !notificationDropdown.contains(e.target)) {
        notificationBell.classList.remove('active');
      }
    });
    
    // Optional: Add sound effect function
    function playNotificationSound() {
      // Create an audio element
      const audio = new Audio();
      // Set the source to your notification sound
      audio.src = 'https://assets.mixkit.co/sfx/preview/mixkit-arcade-game-jump-coin-216.mp3';
      audio.volume = 0.5;
      audio.play().catch(e => console.log('Audio play failed:', e));
    }
    
    // Update notification count (example)
    function updateNotificationCount(count) {
      const badge = notificationBell.querySelector('.notification-badge');
      if (badge) {
        badge.textContent = count;
        badge.style.display = 'flex';
      }
    }
    
    // Example: Mark all as read button
    const markAllReadBtn = document.querySelector('.notification-footer button');
    if (markAllReadBtn) {
      markAllReadBtn.addEventListener('click', function() {

        fetch('/api/notifications/mark-read/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
          }
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            loadNotifications();
            updateNotificationCount(0);
          }
        })
        .catch(err => console.error('Mark as read failed:', err));
      });
    }
  });