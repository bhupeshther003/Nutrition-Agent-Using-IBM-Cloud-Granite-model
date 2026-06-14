// Global variables
let currentJobId = null;
let selectedFiles = [];

// DOM Elements
const jobForm = document.getElementById('job-form');
const uploadSection = document.getElementById('upload-section');
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const fileList = document.getElementById('file-list');
const uploadBtn = document.getElementById('upload-btn');
const processBtn = document.getElementById('process-btn');
const processingSection = document.getElementById('processing-section');
const resultsSection = document.getElementById('results-section');
const loadingOverlay = document.getElementById('loading-overlay');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
});

function initializeEventListeners() {
    // Job form submission
    jobForm.addEventListener('submit', handleJobSubmit);

    // Upload area interactions
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('drop', handleDrop);
    fileInput.addEventListener('change', handleFileSelect);

    // Button clicks
    uploadBtn.addEventListener('click', handleUpload);
    processBtn.addEventListener('click', handleProcess);
    
    const downloadBtn = document.getElementById('download-report-btn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', handleDownloadReport);
    }
}

// Job Form Handling
async function handleJobSubmit(e) {
    e.preventDefault();
    
    const formData = {
        title: document.getElementById('job-title').value,
        description: document.getElementById('job-description').value,
        required_skills: document.getElementById('required-skills').value.split(',').map(s => s.trim()),
        required_experience: document.getElementById('required-experience').value,
        required_education: document.getElementById('required-education').value
    };

    showLoading();

    try {
        const response = await fetch('/api/jobs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.success) {
            currentJobId = data.job_id;
            showNotification('Job created successfully!', 'success');
            
            // Show upload section
            document.getElementById('job-section').style.display = 'none';
            uploadSection.style.display = 'block';
            uploadSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            showNotification('Failed to create job: ' + data.error, 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

// File Upload Handling
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--primary-color)';
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--border-color)';
    
    const files = Array.from(e.dataTransfer.files);
    addFiles(files);
}

function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    addFiles(files);
}

function addFiles(files) {
    const validFiles = files.filter(file => {
        const ext = file.name.split('.').pop().toLowerCase();
        return ['pdf', 'docx'].includes(ext);
    });

    selectedFiles = [...selectedFiles, ...validFiles];
    updateFileList();
    uploadBtn.disabled = selectedFiles.length === 0;
}

function updateFileList() {
    fileList.innerHTML = '';
    
    selectedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <span>
                <i class="fas fa-file-alt"></i>
                ${file.name} (${formatFileSize(file.size)})
            </span>
            <i class="fas fa-times file-remove" onclick="removeFile(${index})"></i>
        `;
        fileList.appendChild(fileItem);
    });
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    updateFileList();
    uploadBtn.disabled = selectedFiles.length === 0;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

async function handleUpload() {
    if (!currentJobId || selectedFiles.length === 0) return;

    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append('resumes', file);
    });

    showLoading();

    try {
        const response = await fetch(`/api/jobs/${currentJobId}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            showNotification(`${data.uploaded_count} resumes uploaded successfully!`, 'success');
            
            // Show process button
            uploadBtn.style.display = 'none';
            processBtn.style.display = 'inline-flex';
        } else {
            showNotification('Upload failed: ' + data.error, 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

// Processing Handling
async function handleProcess() {
    if (!currentJobId) return;

    // Show processing section
    uploadSection.style.display = 'none';
    processingSection.style.display = 'block';
    processingSection.scrollIntoView({ behavior: 'smooth' });

    // Update counts
    document.getElementById('total-count').textContent = selectedFiles.length;
    document.getElementById('processed-count').textContent = '0';

    try {
        const response = await fetch(`/api/jobs/${currentJobId}/process`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            // Simulate progress (in production, use WebSocket or polling)
            simulateProgress(data.processed_count, data.total_count);
            
            // Wait a bit then show results
            setTimeout(() => {
                loadResults();
            }, 2000);
        } else {
            showNotification('Processing failed: ' + data.error, 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    }
}

function simulateProgress(processed, total) {
    let current = 0;
    const interval = setInterval(() => {
        current++;
        const percentage = (current / total) * 100;
        
        document.getElementById('progress-fill').style.width = percentage + '%';
        document.getElementById('processed-count').textContent = current;

        if (current >= processed) {
            clearInterval(interval);
        }
    }, 500);
}

// Results Handling
async function loadResults() {
    if (!currentJobId) return;

    try {
        const response = await fetch(`/api/jobs/${currentJobId}/results`);
        const data = await response.json();

        if (data.candidates && data.candidates.length > 0) {
            displayResults(data);
            
            // Show results section
            processingSection.style.display = 'none';
            resultsSection.style.display = 'block';
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            showNotification('No results found', 'warning');
        }
    } catch (error) {
        showNotification('Error loading results: ' + error.message, 'error');
    }
}

function displayResults(data) {
    // Update statistics
    document.getElementById('total-candidates').textContent = data.total_candidates;
    document.getElementById('avg-score').textContent = data.average_score.toFixed(1) + '%';
    
    const topScore = Math.max(...data.candidates.map(c => c.match_score));
    document.getElementById('top-score').textContent = topScore.toFixed(1) + '%';
    
    const strongCount = data.candidates.filter(c => c.match_score >= 85).length;
    document.getElementById('strong-candidates').textContent = strongCount;

    // Display candidates
    const candidatesList = document.getElementById('candidates-list');
    candidatesList.innerHTML = '';

    data.candidates.forEach(candidate => {
        const candidateCard = createCandidateCard(candidate);
        candidatesList.appendChild(candidateCard);
    });
}

function createCandidateCard(candidate) {
    const card = document.createElement('div');
    card.className = 'candidate-card';

    const scoreClass = getScoreClass(candidate.match_score);
    
    // Parse JSON strings
    const skills = parseJSON(candidate.skills);
    const matchingSkills = parseJSON(candidate.matching_skills);
    const missingSkills = parseJSON(candidate.missing_skills);

    card.innerHTML = `
        <div class="candidate-header">
            <div class="candidate-name">${candidate.name}</div>
            <div class="candidate-rank">Rank #${candidate.rank}</div>
        </div>
        
        <div class="candidate-score ${scoreClass}">
            ${candidate.match_score.toFixed(1)}% Match
        </div>

        <div class="candidate-details">
            <div class="detail-item">
                <i class="fas fa-envelope"></i>
                <span>${candidate.email || 'N/A'}</span>
            </div>
            <div class="detail-item">
                <i class="fas fa-phone"></i>
                <span>${candidate.phone || 'N/A'}</span>
            </div>
            <div class="detail-item">
                <i class="fas fa-chart-line"></i>
                <span>Skills: ${candidate.skills_score.toFixed(1)}%</span>
            </div>
            <div class="detail-item">
                <i class="fas fa-briefcase"></i>
                <span>Experience: ${candidate.experience_score.toFixed(1)}%</span>
            </div>
        </div>

        <div class="candidate-skills">
            <strong>Matching Skills:</strong>
            <div class="skills-list">
                ${matchingSkills.slice(0, 5).map(skill => 
                    `<span class="skill-tag matched">${skill}</span>`
                ).join('')}
            </div>
        </div>

        ${missingSkills.length > 0 ? `
        <div class="candidate-skills">
            <strong>Missing Skills:</strong>
            <div class="skills-list">
                ${missingSkills.slice(0, 5).map(skill => 
                    `<span class="skill-tag missing">${skill}</span>`
                ).join('')}
            </div>
        </div>
        ` : ''}

        ${candidate.detailed_feedback ? `
        <div class="candidate-feedback">
            <h4><i class="fas fa-comment-dots"></i> AI Assessment</h4>
            <p>${candidate.detailed_feedback}</p>
        </div>
        ` : ''}
    `;

    return card;
}

function getScoreClass(score) {
    if (score >= 85) return 'score-excellent';
    if (score >= 70) return 'score-good';
    if (score >= 50) return 'score-fair';
    return 'score-poor';
}

function parseJSON(jsonString) {
    try {
        return JSON.parse(jsonString || '[]');
    } catch {
        return [];
    }
}

// Report Download
async function handleDownloadReport() {
    if (!currentJobId) return;

    showLoading();

    try {
        const response = await fetch(`/api/jobs/${currentJobId}/report`);
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `screening_report_${currentJobId}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showNotification('Report downloaded successfully!', 'success');
        } else {
            showNotification('Failed to download report', 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

// Utility Functions
function showLoading() {
    loadingOverlay.style.display = 'flex';
}

function hideLoading() {
    loadingOverlay.style.display = 'none';
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#2e7d32' : type === 'error' ? '#c62828' : '#1976d2'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;

    document.body.appendChild(notification);

    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 5000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Made with Bob
