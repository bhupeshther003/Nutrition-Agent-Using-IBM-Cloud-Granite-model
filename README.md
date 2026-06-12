# 🍎 NutriBot - AI-Powered Nutrition Agent

An intelligent nutrition guidance web application powered by **IBM Watsonx.ai** and **Granite models**. Get personalized meal plans, calorie analysis, BMI calculations, and family nutrition management with a focus on Indian cuisine.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![IBM Watsonx.ai](https://img.shields.io/badge/IBM-Watsonx.ai-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🤖 AI-Powered Chat Interface
- Real-time nutrition advice using IBM Watsonx.ai Granite models
- Context-aware conversations with chat history
- Specialized in Indian cuisine and dietary practices
- Support for vegetarian, vegan, and non-vegetarian diets

### 📊 Nutrition Dashboard
- Track daily calories, protein, carbs, and fats
- Analyze nutritional content of Indian food items
- Visual statistics with animated cards
- Real-time food analysis

### 🍽️ Personalized Meal Planning
- AI-generated meal plans based on:
  - Age, weight, height, and activity level
  - Diet preferences (Vegetarian, Non-Veg, Vegan, Eggetarian)
  - Goals (Weight loss, maintenance, gain, muscle building)
  - Cuisine preferences (North Indian, South Indian, Mixed, Continental)
- Detailed calorie and macronutrient breakdown
- Practical, affordable Indian meal suggestions

### 📏 BMI Calculator
- Calculate Body Mass Index
- Get category classification (Underweight, Normal, Overweight, Obese)
- Receive personalized health recommendations
- Color-coded results for easy understanding

### 👨‍👩‍👧‍👦 Family Profile Management
- Create profiles for multiple family members
- Track nutrition for entire family
- Individual dietary preferences and goals
- Easy-to-manage member cards

### 🎨 Modern UI/UX
- Responsive design for mobile, tablet, and desktop
- Dark mode support with toggle
- Smooth animations and transitions
- Bootstrap 5 with custom styling
- Gradient backgrounds and modern cards

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- IBM Cloud account with Watsonx.ai access
- IBM Cloud API Key
- Watsonx.ai Project ID

### Installation

1. **Clone or download the project**
   ```bash
   cd nutribot-app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   
   Windows:
   ```bash
   .venv\Scripts\activate
   ```
   
   Linux/Mac:
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   
   Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   ```
   
   Edit `.env` and add your credentials:
   ```env
   IBM_CLOUD_API_KEY=your_actual_api_key_here
   IBM_WATSONX_PROJECT_ID=your_project_id_here
   IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
   FLASK_SECRET_KEY=your_secret_key_here
   FLASK_ENV=development
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open your browser**
   
   Navigate to: `http://localhost:5000`

## 🔑 Getting IBM Watsonx.ai Credentials

### Step 1: Create IBM Cloud Account
1. Go to [IBM Cloud](https://cloud.ibm.com/)
2. Sign up for a free account or log in

### Step 2: Create Watsonx.ai Project
1. Navigate to **IBM Watsonx.ai** service
2. Create a new project
3. Note your **Project ID** from project settings

### Step 3: Generate API Key
1. Go to **Manage** → **Access (IAM)**
2. Select **API keys** from the left menu
3. Click **Create an IBM Cloud API key**
4. Copy and save your API key securely

### Step 4: Configure the Application
Add your credentials to the `.env` file as shown in the installation steps.

## 🎯 Customizing the Agent

The nutrition agent behavior can be easily customized by editing the `AGENT_INSTRUCTIONS` section in `app.py`:

```python
AGENT_INSTRUCTIONS = """
You are NutriBot, an expert AI Nutrition Agent...

## Your Role & Tone:
- Modify the agent's personality and communication style

## Specializations:
- Add or remove areas of expertise

## Indian Food Preferences:
- Customize regional food preferences
- Add specific dietary restrictions

## Safety Rules & Limitations:
- Define what the agent should and shouldn't do

## Response Format:
- Customize how responses are structured
"""
```

### Customization Examples:

**Change Tone:**
```python
## Your Role & Tone:
- Be professional and clinical
- Use technical nutrition terminology
- Provide evidence-based recommendations
```

**Add Specialization:**
```python
## Specializations:
- Keto diet planning
- Intermittent fasting guidance
- Sports nutrition for athletes
- Pregnancy nutrition
```

**Regional Preferences:**
```python
## Indian Food Preferences:
- Focus on South Indian cuisine (dosa, idli, sambar)
- Include Bengali dishes (fish curry, mishti)
- Suggest Gujarati thali options
```

## 📁 Project Structure

```
nutribot-app/
├── app.py                 # Flask backend with Watsonx.ai integration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your actual credentials (not in git)
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── style.css         # Custom CSS styles
│   └── script.js         # JavaScript functionality
└── .venv/                # Virtual environment (created during setup)
```

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0** - Web framework
- **IBM Watsonx.ai** - AI/ML platform
- **IBM Granite Models** - Large language models
- **Python-dotenv** - Environment variable management

### Frontend
- **Bootstrap 5.3.2** - UI framework
- **Bootstrap Icons** - Icon library
- **Google Fonts (Poppins)** - Typography
- **Vanilla JavaScript** - Interactivity
- **CSS3** - Custom styling with animations

### AI Model
- **IBM Granite 13B Chat v2** - Conversational AI model
- Optimized for nutrition and health guidance
- Context-aware responses
- Indian cuisine expertise

## 🌐 Deployment

### Deploy to IBM Cloud

1. **Install IBM Cloud CLI**
   ```bash
   # Download from: https://cloud.ibm.com/docs/cli
   ```

2. **Login to IBM Cloud**
   ```bash
   ibmcloud login
   ```

3. **Create a Cloud Foundry app**
   ```bash
   ibmcloud cf push nutribot-app
   ```

### Deploy to Heroku

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku app**
   ```bash
   heroku create nutribot-app
   ```

3. **Set environment variables**
   ```bash
   heroku config:set IBM_CLOUD_API_KEY=your_key
   heroku config:set IBM_WATSONX_PROJECT_ID=your_project_id
   heroku config:set FLASK_SECRET_KEY=your_secret
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### Deploy to AWS/Azure/GCP

Use the provided `requirements.txt` and configure environment variables in your cloud platform's settings.

## 📱 Features in Detail

### Chat Interface
- **Real-time AI responses** using IBM Watsonx.ai
- **Conversation history** for context-aware answers
- **Markdown formatting** support in responses
- **Smooth animations** for message appearance
- **Auto-scroll** to latest messages

### Nutrition Dashboard
- **Live statistics** for daily intake
- **Food analysis** with detailed breakdown
- **Calorie tracking** with visual indicators
- **Macronutrient display** (Protein, Carbs, Fats)

### Meal Planning
- **Personalized plans** based on user profile
- **Multiple diet types** support
- **Goal-oriented** recommendations
- **Cuisine preferences** (Indian regional foods)
- **Detailed meal breakdown** with calories

### BMI Calculator
- **Instant calculation** with visual feedback
- **Category classification** with color coding
- **Health recommendations** based on BMI
- **Easy-to-understand** results

### Family Profiles
- **Multiple member support**
- **Individual tracking** for each member
- **Dietary preferences** per person
- **Easy management** with add/remove functionality

## 🎨 UI Features

- ✅ **Responsive Design** - Works on all devices
- ✅ **Dark Mode** - Eye-friendly night mode
- ✅ **Smooth Animations** - Professional transitions
- ✅ **Modern Gradients** - Beautiful color schemes
- ✅ **Loading Indicators** - Clear feedback
- ✅ **Toast Notifications** - Non-intrusive alerts
- ✅ **Smooth Scrolling** - Enhanced navigation

## 🔒 Security Best Practices

1. **Never commit `.env` file** to version control
2. **Use strong secret keys** for Flask sessions
3. **Keep API keys secure** and rotate regularly
4. **Use HTTPS** in production
5. **Validate user inputs** on both client and server
6. **Implement rate limiting** for API calls

## 🐛 Troubleshooting

### Issue: "Import flask could not be resolved"
**Solution:** Activate virtual environment and install dependencies
```bash
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Issue: "Failed to initialize AI model"
**Solution:** Check your IBM Cloud credentials in `.env` file
- Verify API key is correct
- Ensure Project ID is valid
- Check Watsonx.ai service is active

### Issue: "Connection timeout"
**Solution:** Check your internet connection and IBM Cloud service status

### Issue: Dark mode not persisting
**Solution:** Clear browser cache and localStorage

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application page |
| `/chat` | POST | Send message to AI agent |
| `/calculate-bmi` | POST | Calculate BMI |
| `/generate-meal-plan` | POST | Generate personalized meal plan |
| `/analyze-food` | POST | Analyze food nutritional content |
| `/family-profile` | POST | Save family member profiles |
| `/get-family-profile` | GET | Retrieve family profiles |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **IBM Watsonx.ai** for providing the AI platform
- **IBM Granite Models** for powerful language understanding
- **Bootstrap** for the UI framework
- **Flask** community for the excellent web framework

## 📧 Support

For issues and questions:
- Check the troubleshooting section
- Review IBM Watsonx.ai documentation
- Open an issue on the project repository

## 🔮 Future Enhancements

- [ ] Recipe suggestions with step-by-step instructions
- [ ] Grocery list generation
- [ ] Integration with fitness trackers
- [ ] Multi-language support
- [ ] Voice input for queries
- [ ] PDF export for meal plans
- [ ] Weekly meal planning calendar
- [ ] Water intake tracking
- [ ] Exercise recommendations
- [ ] Progress tracking with charts

---

**Built with ❤️ using IBM Watsonx.ai and Flask**

*Disclaimer: This application provides general nutrition information and should not replace professional medical advice. Always consult healthcare professionals for medical concerns.*