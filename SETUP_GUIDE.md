# 🚀 Quick Setup Guide - NutriBot

This is a step-by-step guide to get your NutriBot application up and running in minutes.

## 📋 Prerequisites Checklist

Before you begin, make sure you have:

- [ ] Python 3.8 or higher installed
- [ ] pip package manager
- [ ] IBM Cloud account (free tier available)
- [ ] Text editor or IDE (VS Code recommended)
- [ ] Internet connection

---

## 🎯 Step 1: Get IBM Watsonx.ai Credentials

### 1.1 Create IBM Cloud Account

1. Go to [IBM Cloud](https://cloud.ibm.com/)
2. Click **"Create an account"** (or login if you have one)
3. Complete the registration process
4. Verify your email address

### 1.2 Access Watsonx.ai

1. Login to IBM Cloud
2. Search for **"watsonx.ai"** in the catalog
3. Click on **"watsonx.ai"** service
4. Click **"Launch watsonx.ai"**

### 1.3 Create a Project

1. In watsonx.ai, click **"Projects"**
2. Click **"New project"**
3. Choose **"Create an empty project"**
4. Give it a name (e.g., "NutriBot Project")
5. Click **"Create"**
6. **Copy your Project ID** from the project settings (you'll need this!)

### 1.4 Generate API Key

1. Click on your profile icon (top right)
2. Go to **"Profile and settings"**
3. Select **"API keys"** from the left menu
4. Click **"Create"** button
5. Give it a name (e.g., "NutriBot API Key")
6. Click **"Create"**
7. **Copy and save your API key securely** (you won't see it again!)

---

## 💻 Step 2: Setup the Application

### 2.1 Download/Clone the Project

If you have the project files, navigate to the project directory:
```bash
cd path/to/nutribot-app
```

### 2.2 Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` in your terminal prompt.

### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

Wait for all packages to install (this may take a few minutes).

### 2.4 Configure Environment Variables

1. **Copy the example file:**
   
   **Windows:**
   ```bash
   copy .env.example .env
   ```
   
   **Mac/Linux:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file:**
   
   Open `.env` in your text editor and replace the placeholders:
   
   ```env
   # Replace with your actual IBM Cloud API Key
   IBM_CLOUD_API_KEY=paste_your_api_key_here
   
   # Replace with your Watsonx.ai Project ID
   IBM_WATSONX_PROJECT_ID=paste_your_project_id_here
   
   # Keep this as is (or change region if needed)
   IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
   
   # Generate a random secret key (see below)
   FLASK_SECRET_KEY=your_secret_key_here
   
   # Keep as development for local testing
   FLASK_ENV=development
   ```

3. **Generate a Secret Key:**
   
   Run this command to generate a secure secret key:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   
   Copy the output and paste it as your `FLASK_SECRET_KEY` value.

---

## 🎬 Step 3: Run the Application

### 3.1 Start the Server

```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
```

### 3.2 Open in Browser

1. Open your web browser
2. Go to: `http://localhost:5000`
3. You should see the NutriBot homepage!

---

## ✅ Step 4: Test the Application

### 4.1 Test Chat Feature

1. Scroll to the **"Chat with NutriBot"** section
2. Type a question like: "What's a healthy breakfast for weight loss?"
3. Click **Send** or press **Enter**
4. Wait for the AI response (may take a few seconds)

### 4.2 Test BMI Calculator

1. Scroll to **"BMI Calculator"** section
2. Enter your weight (e.g., 70 kg)
3. Enter your height (e.g., 170 cm)
4. Click **"Calculate BMI"**
5. View your results!

### 4.3 Test Meal Plan Generator

1. Go to **"Personalized Meal Plan"** section
2. Fill in your profile details
3. Select your preferences
4. Click **"Generate Meal Plan"**
5. View your personalized meal plan!

### 4.4 Test Dark Mode

1. Click the moon icon in the navigation bar
2. The theme should switch to dark mode
3. Click again to switch back

---

## 🎨 Step 5: Customize the Agent (Optional)

### 5.1 Edit Agent Instructions

1. Open `app.py` in your text editor
2. Find the `AGENT_INSTRUCTIONS` section (around line 30)
3. Customize the agent's behavior:

```python
AGENT_INSTRUCTIONS = """
You are NutriBot, an expert AI Nutrition Agent...

## Your Role & Tone:
- Change the personality here
- Make it more formal or casual
- Add specific expertise areas

## Indian Food Preferences:
- Focus on specific regional cuisines
- Add dietary restrictions
- Customize meal suggestions
"""
```

4. Save the file
5. Restart the application (Ctrl+C, then `python app.py`)

### 5.2 Customize UI Colors

1. Open `static/style.css`
2. Find the `:root` section at the top
3. Change color variables:

```css
:root {
    --primary-color: #4f46e5;  /* Change this */
    --secondary-color: #10b981; /* And this */
    /* ... */
}
```

4. Save and refresh your browser

---

## 🐛 Troubleshooting

### Problem: "Import flask could not be resolved"

**Solution:**
```bash
# Make sure virtual environment is activated
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: "Failed to initialize AI model"

**Solution:**
1. Check your `.env` file has correct credentials
2. Verify API key is valid (no extra spaces)
3. Confirm Project ID is correct
4. Check internet connection
5. Verify Watsonx.ai service is active in IBM Cloud

### Problem: "Connection timeout"

**Solution:**
1. Check your internet connection
2. Try a different network
3. Check IBM Cloud service status
4. Verify firewall isn't blocking the connection

### Problem: Application won't start

**Solution:**
```bash
# Check Python version
python --version  # Should be 3.8+

# Check if port 5000 is available
# Windows: netstat -ano | findstr :5000
# Mac/Linux: lsof -i :5000

# Try a different port
python app.py  # Then edit app.py to change port
```

### Problem: Static files not loading

**Solution:**
1. Verify folder structure:
   ```
   nutribot-app/
   ├── static/
   │   ├── style.css
   │   └── script.js
   └── templates/
       └── index.html
   ```
2. Clear browser cache (Ctrl+Shift+Delete)
3. Hard refresh (Ctrl+F5)

---

## 📱 Using the Application

### Chat Interface
- Ask nutrition questions in natural language
- Get personalized advice based on Indian cuisine
- Receive calorie and macronutrient information
- Get meal suggestions and recipes

### Nutrition Dashboard
- Enter food items to analyze
- View calorie breakdown
- Track daily nutrition intake
- Get nutritional insights

### Meal Plan Generator
- Fill in your profile (age, weight, height)
- Select activity level and goals
- Choose diet type and cuisine preference
- Get a complete day's meal plan

### BMI Calculator
- Enter weight and height
- Get instant BMI calculation
- View health category
- Receive recommendations

### Family Profiles
- Add multiple family members
- Track nutrition for each person
- Set individual dietary preferences
- Manage family health together

---

## 🔒 Security Best Practices

1. **Never share your `.env` file**
2. **Don't commit `.env` to Git**
3. **Keep API keys secure**
4. **Use strong secret keys**
5. **Update dependencies regularly**

---

## 📚 Next Steps

### Learn More
- Read the full [README.md](README.md) for detailed features
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Explore IBM Watsonx.ai documentation

### Customize Further
- Modify agent instructions for specific use cases
- Add new features to the application
- Integrate with other services
- Create custom meal plan templates

### Deploy to Production
- Follow the deployment guide
- Choose a hosting platform (Heroku, AWS, IBM Cloud)
- Set up monitoring and logging
- Configure domain and SSL

---

## 🆘 Getting Help

### Resources
- **IBM Watsonx.ai Docs:** https://www.ibm.com/docs/en/watsonx-as-a-service
- **Flask Documentation:** https://flask.palletsprojects.com/
- **Bootstrap Docs:** https://getbootstrap.com/docs/

### Common Questions

**Q: Is this free to use?**
A: IBM Cloud offers a free tier for Watsonx.ai. Check current pricing on IBM Cloud.

**Q: Can I use this commercially?**
A: Check IBM Watsonx.ai terms of service and licensing.

**Q: How do I add more features?**
A: Edit `app.py` for backend, `templates/index.html` for UI, and `static/script.js` for frontend logic.

**Q: Can I change the AI model?**
A: Yes! Edit the `model_id` in `app.py` to use different Granite models.

**Q: How do I backup my data?**
A: Currently uses session storage. For production, implement a database.

---

## 🎉 Congratulations!

You've successfully set up NutriBot! Start exploring the features and getting personalized nutrition advice.

**Enjoy your journey to better health! 🍎💪**

---

## 📝 Quick Reference

### Start Application
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Run application
python app.py
```

### Stop Application
```
Press Ctrl+C in the terminal
```

### Update Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Generate New Secret Key
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

**Need more help? Check the troubleshooting section or review the full documentation!**