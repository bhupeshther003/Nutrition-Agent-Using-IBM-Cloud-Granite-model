// Global state
let isProcessing = false;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    checkHealth();
    loadDocuments();
});

function initializeApp() {
    console.log('Company Policy Assistant initialized');
}

function setupEventListeners() {
    // Upload area click
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary-color)';
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = 'var(--border-color)';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--border-color)';
        const files = e.dataTransfer.files;
        handleFileUpload(files);
    });
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        handleFileUpload(e.target.files);
    });
    
    // Question input
    const questionInput = document.getElementById('questionInput');
    questionInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            askQuestion();
        }
    });
    
    // Auto-resize textarea
    questionInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });
}

async function checkHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        const statusDot = document.getElementById('statusDot');
        const statusText = document.getElementById('statusText');
        
        if (data.watsonx_initialized) {
            statusDot.classList.add('online');
            statusText.textContent = 'System Ready';
        } else {
            statusDot.classList.add('offline');
            statusText.textContent = 'Watsonx Not Configured';
        }
    } catch (error) {
        console.error('Health check failed:', error);
        const statusDot = document.getElementById('statusDot');
        const statusText = document.getElementById('statusText');
        statusDot.classList.add('offline');
        statusText.textContent = 'System Error';
    }
}

async function handleFileUpload(files) {
    const uploadStatus = document.getElementById('uploadStatus');
    
    if (files.length === 0) return;
    
    uploadStatus.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
    uploadStatus.className = 'upload-status';
    
    for (let file of files) {
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                uploadStatus.innerHTML = `<i class="fas fa-check-circle"></i> ${data.message}`;
                uploadStatus.className = 'upload-status success';
                loadDocuments();
            } else {
                uploadStatus.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${data.error}`;
                uploadStatus.className = 'upload-status error';
            }
        } catch (error) {
            uploadStatus.innerHTML = `<i class="fas fa-exclamation-circle"></i> Upload failed: ${error.message}`;
            uploadStatus.className = 'upload-status error';
        }
    }
    
    // Clear file input
    document.getElementById('fileInput').value = '';
    
    // Clear status after 5 seconds
    setTimeout(() => {
        uploadStatus.innerHTML = '';
    }, 5000);
}

async function loadDocuments() {
    const documentList = document.getElementById('documentList');
    
    try {
        const response = await fetch('/api/documents');
        const data = await response.json();
        
        if (data.success && data.documents.length > 0) {
            documentList.innerHTML = data.documents.map(doc => `
                <div class="document-item">
                    <span class="document-name">
                        <i class="fas fa-file-alt"></i> ${doc}
                    </span>
                    <button class="delete-btn" onclick="deleteDocument('${doc}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `).join('');
        } else {
            documentList.innerHTML = '<p class="loading">No documents uploaded yet</p>';
        }
    } catch (error) {
        console.error('Failed to load documents:', error);
        documentList.innerHTML = '<p class="loading">Failed to load documents</p>';
    }
}

async function deleteDocument(documentName) {
    if (!confirm(`Are you sure you want to delete "${documentName}"?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/documents/${encodeURIComponent(documentName)}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            loadDocuments();
        } else {
            alert('Failed to delete document: ' + data.error);
        }
    } catch (error) {
        alert('Failed to delete document: ' + error.message);
    }
}

async function askQuestion() {
    if (isProcessing) return;
    
    const questionInput = document.getElementById('questionInput');
    const question = questionInput.value.trim();
    
    if (!question) return;
    
    isProcessing = true;
    const sendButton = document.getElementById('sendButton');
    sendButton.disabled = true;
    
    // Add user message
    addMessage(question, 'user');
    
    // Clear input
    questionInput.value = '';
    questionInput.style.height = 'auto';
    
    // Show typing indicator
    const typingId = addTypingIndicator();
    
    try {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        if (data.success) {
            addMessage(data.answer, 'assistant', data.sources);
        } else {
            addMessage('Sorry, I encountered an error: ' + data.error, 'assistant');
        }
    } catch (error) {
        removeTypingIndicator(typingId);
        addMessage('Sorry, I encountered an error processing your question.', 'assistant');
        console.error('Error:', error);
    } finally {
        isProcessing = false;
        sendButton.disabled = false;
        questionInput.focus();
    }
}

function addMessage(text, type, sources = []) {
    const chatMessages = document.getElementById('chatMessages');
    
    // Remove welcome message if it exists
    const welcomeMessage = chatMessages.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;
    
    let sourcesHtml = '';
    if (sources && sources.length > 0) {
        sourcesHtml = `
            <div class="message-sources">
                <h4><i class="fas fa-book"></i> Sources:</h4>
                ${sources.map(source => `
                    <div class="source-item">
                        <i class="fas fa-file-alt"></i> ${source.document}
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    messageDiv.innerHTML = `
        <div class="message-content">
            ${escapeHtml(text)}
            ${sourcesHtml}
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    const typingId = 'typing-' + Date.now();
    typingDiv.id = typingId;
    typingDiv.className = 'message message-assistant';
    typingDiv.innerHTML = `
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return typingId;
}

function removeTypingIndicator(typingId) {
    const typingDiv = document.getElementById(typingId);
    if (typingDiv) {
        typingDiv.remove();
    }
}

async function clearHistory() {
    if (!confirm('Are you sure you want to clear the chat history?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/history', {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            const chatMessages = document.getElementById('chatMessages');
            chatMessages.innerHTML = `
                <div class="welcome-message">
                    <i class="fas fa-robot"></i>
                    <h3>Welcome to the Company Policy Assistant!</h3>
                    <p>I can help you with questions about:</p>
                    <ul>
                        <li>HR policies and procedures</li>
                        <li>Leave and attendance policies</li>
                        <li>Travel and expense policies</li>
                        <li>Security and compliance guidelines</li>
                        <li>General company policies</li>
                    </ul>
                    <p>Upload your company policy documents and start asking questions!</p>
                </div>
            `;
        }
    } catch (error) {
        alert('Failed to clear history: ' + error.message);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML.replace(/\n/g, '<br>');
}

// Made with Bob
