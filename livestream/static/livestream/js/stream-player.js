/**
 * Gaming Stream Player - Complete Stream Management System
 * Handles video streaming, chat, and UI interactions
 */

// Global Configuration
const CONFIG = {
    MAX_RECONNECT_ATTEMPTS: 5,
    STREAM_CHECK_INTERVAL: 10000, // 10 seconds
    CHAT_RECONNECT_DELAY: 3000,
    MAX_CHAT_MESSAGES: 100,
    RETRY_DELAY_BASE: 5000
};

// Main Stream Player Class
class StreamPlayer {
    constructor() {
        this.hls = null;
        this.reconnectAttempts = 0;
        this.streamCheckInterval = null;
        this.viewerCount = 0;
        this.streamStartTime = null;
        this.streamTimerInterval = null;
        
        this.video = document.getElementById('video');
        this.streamId = window.STREAM_CONFIG.streamId;
        this.playbackUrl = window.STREAM_CONFIG.playbackUrl;
        
        this.init();
    }

    init() {
        console.log('Initializing Stream Player...');
        this.initializeStream();
        this.startStreamMonitoring();
        this.setupEventListeners();
    }

    initializeStream() {
        if (!this.playbackUrl) {
            this.showError('No playback URL available');
            return;
        }

        console.log('Loading stream:', this.playbackUrl);

        if (Hls.isSupported()) {
            this.setupHLS();
        } else if (this.video.canPlayType('application/vnd.apple.mpegurl')) {
            this.setupNativeHLS();
        } else {
            this.showError('Your browser does not support HLS streaming');
        }
    }

    setupHLS() {
        if (this.hls) {
            this.hls.destroy();
        }

        this.hls = new Hls({
            enableWorker: true,
            lowLatencyMode: true,
            backBufferLength: 90,
            maxBufferLength: 30,
            maxMaxBufferLength: 60
        });

        this.hls.loadSource(this.playbackUrl);
        this.hls.attachMedia(this.video);

        // HLS Event Listeners
        this.hls.on(Hls.Events.MANIFEST_PARSED, () => {
            console.log('Stream manifest loaded successfully');
            this.hideOverlay();
            this.updateStreamStatus(true);
            this.reconnectAttempts = 0;
        });

        this.hls.on(Hls.Events.ERROR, (event, data) => {
            console.error('HLS Error:', data);
            if (data.fatal) {
                this.handleStreamError(data);
            }
        });

        this.hls.on(Hls.Events.FRAG_LOADED, () => {
            this.updateStreamStatus(true);
        });

        this.hls.on(Hls.Events.BUFFER_APPENDED, () => {
            this.hideOverlay();
        });
    }

    setupNativeHLS() {
        this.video.src = this.playbackUrl;
        
        this.video.addEventListener('loadedmetadata', () => {
            console.log('Native HLS loaded');
            this.hideOverlay();
            this.updateStreamStatus(true);
        });
        
        this.video.addEventListener('error', (e) => {
            this.handleStreamError({ type: 'MEDIA_ERROR', details: e });
        });
    }

    setupEventListeners() {
        // Video Events
        this.video.addEventListener('play', () => {
            this.updateStreamStatus(true);
        });

        this.video.addEventListener('waiting', () => {
            this.showOverlay('Buffering...');
        });

        this.video.addEventListener('playing', () => {
            this.hideOverlay();
        });

        this.video.addEventListener('ended', () => {
            this.updateStreamStatus(false);
        });

        // Window Events
        window.addEventListener('beforeunload', () => {
            this.cleanup();
        });

        window.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                // Page hidden - reduce resource usage
                if (this.hls) {
                    this.hls.config.maxBufferLength = 10;
                }
            } else {
                // Page visible - restore normal buffering
                if (this.hls) {
                    this.hls.config.maxBufferLength = 30;
                }
            }
        });
    }

    startStreamMonitoring() {
        this.streamCheckInterval = setInterval(() => {
            this.checkStreamStatus();
        }, CONFIG.STREAM_CHECK_INTERVAL);
    }

    async checkStreamStatus() {
        try {
            const response = await fetch(`/api/stream/${this.streamId}/status/`);
            const data = await response.json();
            
            if (data.is_live && !this.video.src && !this.hls) {
                console.log('Stream came online, reinitializing...');
                this.initializeStream();
            } else if (!data.is_live && (this.video.src || this.hls)) {
                console.log('Stream went offline');
                this.updateStreamStatus(false);
            }
            
            this.viewerCount = data.viewer_count || 0;
            this.updateViewerCount();
            
        } catch (error) {
            console.error('Error checking stream status:', error);
        }
    }

    updateStreamStatus(isLive) {
        const liveBadge = document.getElementById('liveBadge');
        
        if (isLive) {
            liveBadge.textContent = '🔴 LIVE';
            liveBadge.className = 'live-badge live';
            
            if (!this.streamStartTime) {
                this.streamStartTime = Date.now();
                this.startStreamTimer();
            }
        } else {
            liveBadge.textContent = '⚫ OFFLINE';
            liveBadge.className = 'live-badge offline';
            this.showError('Stream is offline');
            this.streamStartTime = null;
            
            if (this.streamTimerInterval) {
                clearInterval(this.streamTimerInterval);
                this.streamTimerInterval = null;
            }
        }
    }

    startStreamTimer() {
        if (this.streamTimerInterval) {
            clearInterval(this.streamTimerInterval);
        }
        
        this.streamTimerInterval = setInterval(() => {
            if (this.streamStartTime) {
                const elapsed = Date.now() - this.streamStartTime;
                const hours = Math.floor(elapsed / 3600000);
                const minutes = Math.floor((elapsed % 3600000) / 60000);
                const seconds = Math.floor((elapsed % 60000) / 1000);
                
                const timeString = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                document.getElementById('streamTime').textContent = timeString;
            }
        }, 1000);
    }

    updateViewerCount() {
        const viewerElement = document.getElementById('viewerCount');
        const count = this.viewerCount;
        let displayText;
        
        if (count >= 1000000) {
            displayText = `${(count / 1000000).toFixed(1)}M viewers`;
        } else if (count >= 1000) {
            displayText = `${(count / 1000).toFixed(1)}K viewers`;
        } else {
            displayText = `${count} viewers`;
        }
        
        viewerElement.textContent = displayText;
    }

    handleStreamError(data) {
        console.error('Stream error occurred:', data);
        
        let errorMessage = 'Stream connection failed';
        
        if (data && data.details) {
            switch (data.details) {
                case 'manifestLoadError':
                    errorMessage = 'Failed to load stream manifest';
                    break;
                case 'levelLoadError':
                    errorMessage = 'Failed to load stream quality';
                    break;
                case 'fragLoadError':
                    errorMessage = 'Failed to load stream fragment';
                    break;
                default:
                    errorMessage = 'Stream playback error';
            }
        }
        
        this.showError(errorMessage);
        this.updateStreamStatus(false);
        
        // Auto-retry with exponential backoff
        if (this.reconnectAttempts < CONFIG.MAX_RECONNECT_ATTEMPTS) {
            this.reconnectAttempts++;
            const delay = CONFIG.RETRY_DELAY_BASE * Math.pow(2, this.reconnectAttempts - 1);
            
            console.log(`Retrying connection in ${delay}ms (attempt ${this.reconnectAttempts})`);
            setTimeout(() => {
                this.retryConnection();
            }, delay);
        } else {
            console.log('Max reconnection attempts reached');
            Utils.showToast('Maximum reconnection attempts reached', 'error');
        }
    }

    retryConnection() {
        console.log('Retrying stream connection...');
        this.hideError();
        this.showOverlay('Reconnecting...');
        
        if (this.hls) {
            this.hls.destroy();
            this.hls = null;
        }
        
        setTimeout(() => {
            this.initializeStream();
        }, 2000);
    }

    // UI Control Methods
    showOverlay(message = 'Connecting to stream...') {
        const overlay = document.getElementById('videoOverlay');
        const spinner = overlay.querySelector('.loading-spinner p');
        spinner.textContent = message;
        overlay.style.display = 'flex';
    }

    hideOverlay() {
        document.getElementById('videoOverlay').style.display = 'none';
    }

    showError(message) {
        const errorDiv = document.getElementById('videoError');
        const errorText = errorDiv.querySelector('p');
        errorText.textContent = message;
        errorDiv.style.display = 'flex';
        this.hideOverlay();
    }

    hideError() {
        document.getElementById('videoError').style.display = 'none';
    }

    toggleStreamInfo() {
        const details = document.getElementById('streamDetails');
        const isVisible = details.style.display !== 'none';
        details.style.display = isVisible ? 'none' : 'block';
    }

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            this.video.requestFullscreen().catch(err => {
                console.error('Error attempting to enable fullscreen:', err);
                Utils.showToast('Fullscreen not supported', 'warning');
            });
        } else {
            document.exitFullscreen();
        }
    }

    cleanup() {
        console.log('Cleaning up Stream Player...');
        
        if (this.hls) {
            this.hls.destroy();
            this.hls = null;
        }
        
        if (this.streamCheckInterval) {
            clearInterval(this.streamCheckInterval);
            this.streamCheckInterval = null;
        }
        
        if (this.streamTimerInterval) {
            clearInterval(this.streamTimerInterval);
            this.streamTimerInterval = null;
        }
    }
}

// Chat Manager Class
class ChatManager {
    constructor() {
        this.socket = null;
        this.reconnectAttempts = 0;
        this.maxMessages = CONFIG.MAX_CHAT_MESSAGES;
        
        this.chatBox = document.getElementById('chatBox');
        this.messageInput = document.getElementById('messageInput');
        this.streamId = window.STREAM_CONFIG.streamId;
        
        this.init();
    }

    init() {
        console.log('Initializing Chat Manager...');
        this.initializeChat();
    }

    initializeChat() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/chat/${this.streamId}/`;
        
        console.log('Connecting to chat:', wsUrl);
        
        this.socket = new WebSocket(wsUrl);

        this.socket.onopen = (e) => {
            console.log('Chat connected successfully');
            Utils.showToast('Connected to chat', 'success');
            this.reconnectAttempts = 0;
        };

        this.socket.onmessage = (e) => {
            try {
                const data = JSON.parse(e.data);
                this.addChatMessage(data);
            } catch (error) {
                console.error('Error parsing chat message:', error);
            }
        };

        this.socket.onclose = (e) => {
            console.log('Chat disconnected:', e.code, e.reason);
            
            if (e.code !== 1000) { // Not a normal closure
                Utils.showToast('Chat disconnected', 'warning');
                this.attemptReconnect();
            }
        };

        this.socket.onerror = (e) => {
            console.error('Chat connection error:', e);
            Utils.showToast('Chat connection error', 'error');
        };
    }

    attemptReconnect() {
        if (this.reconnectAttempts < CONFIG.MAX_RECONNECT_ATTEMPTS) {
            this.reconnectAttempts++;
            const delay = CONFIG.CHAT_RECONNECT_DELAY * this.reconnectAttempts;
            
            console.log(`Attempting to reconnect chat in ${delay}ms (attempt ${this.reconnectAttempts})`);
            
            setTimeout(() => {
                this.initializeChat();
            }, delay);
        } else {
            console.log('Max chat reconnection attempts reached');
            Utils.showToast('Chat connection failed', 'error');
        }
    }

    addChatMessage(data) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message';
        
        const timestamp = new Date().toLocaleTimeString([], {
            hour: '2-digit', 
            minute: '2-digit'
        });
        
        // Sanitize message content
        const sanitizedMessage = this.sanitizeMessage(data.message);
        const sanitizedUsername = this.sanitizeMessage(data.username);
        
        messageDiv.innerHTML = `
            <span class="message-time">${timestamp}</span>
            <span class="message-username">${sanitizedUsername}:</span>
            <span class="message-text">${sanitizedMessage}</span>
        `;
        
        this.chatBox.appendChild(messageDiv);
        this.chatBox.scrollTop = this.chatBox.scrollHeight;
        
        // Remove old messages if too many
        while (this.chatBox.children.length > this.maxMessages) {
            this.chatBox.removeChild(this.chatBox.firstChild);
        }
        
        // Add entrance animation
        requestAnimationFrame(() => {
            messageDiv.style.opacity = '0';
            messageDiv.style.transform = 'translateX(-10px)';
            
            requestAnimationFrame(() => {
                messageDiv.style.transition = 'all 0.3s ease';
                messageDiv.style.opacity = '1';
                messageDiv.style.transform = 'translateX(0)';
            });
        });
    }

    sanitizeMessage(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message) {
            return;
        }
        
        if (message.length > 200) {
            Utils.showToast('Message too long (max 200 characters)', 'warning');
            return;
        }
        
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            Utils.showToast('Chat not connected', 'error');
            return;
        }
        
        try {
            this.socket.send(JSON.stringify({
                'message': message,
                'username': 'Anonymous' // Replace with actual username from session
            }));
            
            this.messageInput.value = '';
        } catch (error) {
            console.error('Error sending message:', error);
            Utils.showToast('Failed to send message', 'error');
        }
    }

    handleKeyPress(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            this.sendMessage();
        }
    }

    toggleChat() {
        const chatContainer = document.getElementById('chatContainer');
        const isVisible = chatContainer.style.display !== 'none';
        chatContainer.style.display = isVisible ? 'none' : 'flex';
    }

    cleanup() {
        console.log('Cleaning up Chat Manager...');
        
        if (this.socket) {
            this.socket.close(1000, 'Page unload');
            this.socket = null;
        }
    }
}

// Utility Functions
class Utils {
    static async copyToClipboard(elementId) {
        const element = document.getElementById(elementId);
        const text = element.textContent;
        
        try {
            await navigator.clipboard.writeText(text);
            this.showToast('Copied to clipboard!', 'success');
        } catch (error) {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.opacity = '0';
            document.body.appendChild(textArea);
            textArea.select();
            
            try {
                document.execCommand('copy');
                this.showToast('Copied to clipboard!', 'success');
            } catch (fallbackError) {
                this.showToast('Failed to copy to clipboard', 'error');
            }
            
            document.body.removeChild(textArea);
        }
    }

    static showToast(message, type = 'info') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        container.appendChild(toast);
        
        // Trigger animation
        requestAnimationFrame(() => {
            toast.classList.add('show');
        });
        
        // Remove after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                if (container.contains(toast)) {
                    container.removeChild(toast);
                }
            }, 300);
        }, 3000);
    }

    static formatNumber(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }

    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Global instances
let streamPlayer;
let chatManager;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing application...');
    
    try {
        streamPlayer = new StreamPlayer();
        chatManager = new ChatManager();
        
        console.log('Application initialized successfully');
        Utils.showToast('Stream player ready', 'success');
        
    } catch (error) {
        console.error('Error initializing application:', error);
        Utils.showToast('Failed to initialize player', 'error');
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    if (streamPlayer) {
        streamPlayer.cleanup();
    }
    if (chatManager) {
        chatManager.cleanup();
    }
});

// Export for global access
window.StreamPlayer = streamPlayer;
window.ChatManager = chatManager;
window.Utils = Utils;

// Declare Hls globally