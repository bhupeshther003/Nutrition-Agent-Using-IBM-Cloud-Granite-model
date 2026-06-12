// ============================================================================
// NutriBot - JavaScript Functions
// ============================================================================

// Global variables
let conversationHistory = [];
let familyMembers = [];

// ============================================================================
// Initialization
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    loadFamilyProfiles();
});

function initializeApp() {
    // Dark mode toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    const savedTheme = localStorage.getItem('theme');
    
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        darkModeToggle.innerHTML = '<i class="bi bi-sun-fill"></i>';
    }
    
    darkModeToggle.addEventListener('click', toggleDarkMode);
    
    // Chat functionality
    document.getElementById('sendBtn').addEventListener('click', sendMessage);
    document.getElementById('chatInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // BMI Calculator
    document.getElementById('calculateBmiBtn').addEventListener('click', calculateBMI);
    
    // Meal Plan Generator
    document.getElementById('generateMealPlanBtn').addEventListener('click', generateMealPlan);
    
    // Food Analysis
    document.getElementById('analyzeBtn').addEventListener('click', analyzeFood);
    
    // Family Profile
    document.getElementById('addMemberBtn').addEventListener('click', addFamilyMember);
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Update active nav link on scroll
    window.addEventListener('scroll', updateActiveNavLink);
}

// ============================================================================
// Dark Mode
// ============================================================================

function toggleDarkMode() {
    const body = document.body;
    const darkModeToggle = document.getElementById('darkModeToggle');
    
    body.classList.toggle('dark-mode');
    
    if (body.classList.contains('dark-mode')) {
        darkModeToggle.innerHTML = '<i class="bi bi-sun-fill"></i>';
        localStorage.setItem('theme', 'dark');
    } else {
        darkModeToggle.innerHTML = '<i class="bi bi-moon-stars-fill"></i>';
        localStorage.setItem('theme', 'light');
    }
}

// ============================================================================
// Chat Functionality
// ============================================================================

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessageToChat('user', message);
    input.value = '';
    
    // Add to conversation history
    conversationHistory.push({
        role: 'user',
        content: message
    });
    
    // Show loading
    showLoading();
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                history: conversationHistory
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            addMessageToChat('bot', `Error: ${data.error}`);
        } else {
            addMessageToChat('bot', data.response);
            conversationHistory.push({
                role: 'assistant',
                content: data.response
            });
        }
    } catch (error) {
        addMessageToChat('bot', `Error: ${error.message}. Please check your API configuration.`);
    } finally {
        hideLoading();
    }
}

function addMessageToChat(role, content) {
    const chatMessages = document.getElementById('chatMessages');
    
    // Remove welcome message if it exists
    const welcomeMessage = chatMessages.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = role === 'user' ? '<i class="bi bi-person-fill"></i>' : '<i class="bi bi-robot"></i>';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML = formatMessage(content);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatMessage(content) {
    // Convert markdown-style formatting to HTML
    let formatted = content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
    
    // Convert numbered lists
    formatted = formatted.replace(/(\d+\.\s.*?)(<br>|$)/g, '<li>$1</li>');
    if (formatted.includes('<li>')) {
        formatted = '<ol>' + formatted + '</ol>';
    }
    
    // Convert bullet points
    formatted = formatted.replace(/[-•]\s(.*?)(<br>|$)/g, '<li>$1</li>');
    if (formatted.includes('<li>') && !formatted.includes('<ol>')) {
        formatted = '<ul>' + formatted + '</ul>';
    }
    
    return formatted;
}

// ============================================================================
// BMI Calculator
// ============================================================================

async function calculateBMI() {
    const weight = parseFloat(document.getElementById('bmiWeight').value);
    const height = parseFloat(document.getElementById('bmiHeight').value);
    
    if (!weight || !height || weight <= 0 || height <= 0) {
        showAlert('Please enter valid weight and height values', 'warning');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/calculate-bmi', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ weight, height })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showAlert(data.error, 'danger');
        } else {
            displayBMIResult(data);
        }
    } catch (error) {
        showAlert(`Error: ${error.message}`, 'danger');
    } finally {
        hideLoading();
    }
}

function displayBMIResult(data) {
    const resultDiv = document.getElementById('bmiResult');
    
    resultDiv.innerHTML = `
        <div class="bmi-result-card alert alert-${data.color}">
            <h4>Your BMI Result</h4>
            <div class="bmi-value">${data.bmi}</div>
            <div class="bmi-category badge bg-${data.color}">${data.category}</div>
            <p class="mt-3 mb-0">${data.recommendation}</p>
        </div>
    `;
}

// ============================================================================
// Meal Plan Generator
// ============================================================================

async function generateMealPlan() {
    const profile = {
        age: document.getElementById('mealAge').value,
        weight: document.getElementById('mealWeight').value,
        height: document.getElementById('mealHeight').value,
        activity: document.getElementById('activityLevel').value
    };
    
    const preferences = {
        diet_type: document.getElementById('dietType').value,
        goal: document.getElementById('goal').value,
        cuisine: document.getElementById('cuisine').value
    };
    
    if (!profile.age || !profile.weight || !profile.height) {
        showAlert('Please fill in all profile fields', 'warning');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/generate-meal-plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ profile, preferences })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showAlert(data.error, 'danger');
        } else {
            displayMealPlan(data.meal_plan);
        }
    } catch (error) {
        showAlert(`Error: ${error.message}`, 'danger');
    } finally {
        hideLoading();
    }
}

function displayMealPlan(mealPlan) {
    const resultDiv = document.getElementById('mealPlanResult');
    
    resultDiv.innerHTML = `
        <div class="meal-plan-content">
            <div class="alert alert-success mb-4">
                <i class="bi bi-check-circle-fill me-2"></i>
                Your personalized meal plan has been generated!
            </div>
            <div class="meal-plan-text">
                ${formatMessage(mealPlan)}
            </div>
        </div>
    `;
}

// ============================================================================
// Food Analysis
// ============================================================================

async function analyzeFood() {
    const foodItems = document.getElementById('foodItems').value.trim();
    
    if (!foodItems) {
        showAlert('Please enter food items to analyze', 'warning');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/analyze-food', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ food_items: foodItems })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showAlert(data.error, 'danger');
        } else {
            displayFoodAnalysis(data.analysis);
        }
    } catch (error) {
        showAlert(`Error: ${error.message}`, 'danger');
    } finally {
        hideLoading();
    }
}

function displayFoodAnalysis(analysis) {
    const resultDiv = document.getElementById('analysisResult');
    
    resultDiv.innerHTML = `
        <div class="alert alert-info">
            <h5 class="alert-heading">
                <i class="bi bi-clipboard-data me-2"></i>Nutritional Analysis
            </h5>
            <hr>
            <div class="analysis-content">
                ${formatMessage(analysis)}
            </div>
        </div>
    `;
    
    // Update dashboard stats (mock data for demo)
    updateDashboardStats();
}

function updateDashboardStats() {
    // Mock data - in production, calculate from actual food analysis
    document.getElementById('caloriesCount').textContent = Math.floor(Math.random() * 500 + 1500);
    document.getElementById('proteinCount').textContent = Math.floor(Math.random() * 50 + 50) + 'g';
    document.getElementById('carbsCount').textContent = Math.floor(Math.random() * 100 + 150) + 'g';
    document.getElementById('fatsCount').textContent = Math.floor(Math.random() * 30 + 40) + 'g';
}

// ============================================================================
// Family Profile Management
// ============================================================================

async function addFamilyMember() {
    const member = {
        name: document.getElementById('memberName').value.trim(),
        relation: document.getElementById('memberRelation').value,
        age: document.getElementById('memberAge').value,
        weight: document.getElementById('memberWeight').value,
        height: document.getElementById('memberHeight').value,
        diet: document.getElementById('memberDiet').value
    };
    
    if (!member.name || !member.age || !member.weight || !member.height) {
        showAlert('Please fill in all member details', 'warning');
        return;
    }
    
    familyMembers.push(member);
    
    showLoading();
    
    try {
        const response = await fetch('/family-profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ members: familyMembers })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showAlert(data.error, 'danger');
        } else {
            showAlert('Family member added successfully!', 'success');
            displayFamilyMembers();
            clearMemberForm();
        }
    } catch (error) {
        showAlert(`Error: ${error.message}`, 'danger');
    } finally {
        hideLoading();
    }
}

function displayFamilyMembers() {
    const container = document.getElementById('familyMembers');
    
    if (familyMembers.length === 0) {
        container.innerHTML = `
            <div class="text-center text-muted py-5">
                <i class="bi bi-person-plus-fill display-1 mb-3"></i>
                <p>Add family members to manage their nutrition profiles</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = familyMembers.map((member, index) => `
        <div class="member-card d-flex align-items-center">
            <div class="member-avatar">
                <i class="bi bi-person-fill"></i>
            </div>
            <div class="flex-grow-1">
                <h5 class="mb-1">${member.name}</h5>
                <p class="text-muted mb-1">
                    <span class="badge bg-primary">${member.relation}</span>
                    <span class="ms-2">${member.age} years</span>
                </p>
                <p class="mb-0 small">
                    <i class="bi bi-heart-pulse me-1"></i>${member.weight}kg | 
                    <i class="bi bi-rulers me-1"></i>${member.height}cm | 
                    <i class="bi bi-egg me-1"></i>${member.diet}
                </p>
            </div>
            <button class="btn btn-outline-danger btn-sm" onclick="removeFamilyMember(${index})">
                <i class="bi bi-trash"></i>
            </button>
        </div>
    `).join('');
}

function removeFamilyMember(index) {
    if (confirm('Are you sure you want to remove this family member?')) {
        familyMembers.splice(index, 1);
        displayFamilyMembers();
        
        // Update server
        fetch('/family-profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ members: familyMembers })
        });
    }
}

function clearMemberForm() {
    document.getElementById('memberName').value = '';
    document.getElementById('memberAge').value = '';
    document.getElementById('memberWeight').value = '';
    document.getElementById('memberHeight').value = '';
}

async function loadFamilyProfiles() {
    try {
        const response = await fetch('/get-family-profile');
        const data = await response.json();
        
        if (data.members && data.members.length > 0) {
            familyMembers = data.members;
            displayFamilyMembers();
        }
    } catch (error) {
        console.error('Error loading family profiles:', error);
    }
}

// ============================================================================
// Utility Functions
// ============================================================================

function showLoading() {
    document.getElementById('loadingSpinner').classList.add('active');
}

function hideLoading() {
    document.getElementById('loadingSpinner').classList.remove('active');
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        
        if (window.pageYOffset >= sectionTop - 100) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}

// ============================================================================
// Sample Data for Demo
// ============================================================================

// Add some sample conversation starters
const sampleQuestions = [
    "What's a healthy breakfast for weight loss?",
    "How many calories should I eat daily?",
    "Suggest a vegetarian meal plan",
    "What are the benefits of dal and rice?",
    "How to gain weight healthily?"
];

// You can add click handlers for these if you want quick-start buttons

// Made with Bob
