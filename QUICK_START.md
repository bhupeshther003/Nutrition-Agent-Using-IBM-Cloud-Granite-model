# ⚡ Quick Start Guide - NutriBot

Get your NutriBot application running in 5 minutes!

---

## 🎯 Prerequisites

✅ Python 3.8+ installed  
✅ IBM Cloud account with Watsonx.ai access  
✅ IBM Cloud API Key  
✅ Watsonx.ai Project ID  

---

## 🚀 Installation Steps

### Step 1: Install Dependencies (2 minutes)

```bash
pip install -r requirements.txt
```

**Wait for installation to complete...**

---

### Step 2: Configure Environment (1 minute)

1. **Open the `.env` file** in your text editor

2. **Add your credentials:**

```env
IBM_CLOUD_API_KEY=your_actual_api_key_here
IBM_WATSONX_PROJECT_ID=your_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

3. **Generate a secret key** (optional but recommended):

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste it as `FLASK_SECRET_KEY`

---

### Step 3: Test Configuration (1 minute)

```bash
python test_app.py
```

**Expected output:**
```
[OK] IBM_CLOUD_API_KEY: ...
[OK] IBM_WATSONX_PROJECT_ID: ...
[OK] IBM_WATSONX_URL: ...
[OK] Flask imported successfully
[OK] ibm-watsonx-ai imported successfully
[SUCCESS] ALL TESTS PASSED!
```

---

### Step 4: Run the Application (30 seconds)

```bash
python app.py
```

**You should see:**
```
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
```

---

### Step 5: Open in Browser (10 seconds)

Open your browser and go to:

```
http://localhost:5000
```

🎉 **You're ready to use NutriBot!**

---

## 🎮 Try These Features

### 1. Chat with NutriBot
- Scroll to "Chat with NutriBot" section
- Type: "What's a healthy breakfast for weight loss?"
- Press Enter or click Send

### 2. Calculate Your BMI
- Scroll to "BMI Calculator"
- Enter your weight (kg) and height (cm)
- Click "Calculate BMI"

### 3. Generate Meal Plan
- Go to "Personalized Meal Plan"
- Fill in your profile details
- Click "Generate Meal Plan"

### 4. Analyze Food
- Go to "Nutrition Dashboard"
- Enter food items (e.g., "2 roti, 1 bowl dal, 1 cup rice")
- Click "Analyze Nutrition"

### 5. Add Family Members
- Scroll to "Family Profiles"
- Fill in member details
- Click "Add Member"

### 6. Toggle Dark Mode
- Click the moon/sun icon in the navigation bar
- Theme will switch and persist

---

## 🐛 Troubleshooting

### Problem: "No module named 'ibm_watsonx_ai'"

**Solution:**
```bash
pip install -r requirements.txt
```

---

### Problem: "Failed to initialize AI model"

**Solution:**
1. Check your `.env` file has correct credentials
2. Verify API key is valid (no extra spaces)
3. Confirm Project ID is correct
4. Check internet connection

---

### Problem: "Port 5000 already in use"

**Solution:**

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
lsof -i :5000
kill -9 <PID>
```

Or change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use port 5001
```

---

### Problem: Application starts but features don't work

**Solution:**
1. Open browser console (F12)
2. Check for JavaScript errors
3. Verify all files are in correct locations:
   - `templates/index.html`
   - `static/style.css`
   - `static/script.js`

---

## 📝 Quick Commands Reference

| Command | Purpose |
|---------|---------|
| `pip install -r requirements.txt` | Install dependencies |
| `python test_app.py` | Test configuration |
| `python app.py` | Start application |
| `Ctrl+C` | Stop application |
| `python -c "import secrets; print(secrets.token_hex(32))"` | Generate secret key |

---

## 🔑 Getting IBM Credentials

### Get API Key:
1. Go to [IBM Cloud](https://cloud.ibm.com/)
2. Login to your account
3. Click profile icon → **API keys**
4. Click **Create**
5. Copy and save your API key

### Get Project ID:
1. Go to [watsonx.ai](https://dataplatform.cloud.ibm.com/wx/home)
2. Open your project
3. Click **Manage** tab
4. Copy **Project ID**

---

## 💡 Tips

1. **Keep your API key secure** - Never share or commit to Git
2. **Use dark mode** - Easier on the eyes for long sessions
3. **Save meal plans** - Copy and paste to a document
4. **Try different cuisines** - Explore North Indian, South Indian options
5. **Add family members** - Track nutrition for everyone

---

## 📚 More Information

- **Full Documentation:** See `README.md`
- **Setup Guide:** See `SETUP_GUIDE.md`
- **Deployment:** See `DEPLOYMENT.md`
- **Fixes Applied:** See `FIXES_APPLIED.md`

---

## ✅ Success Checklist

Before using the application, ensure:

- [x] Dependencies installed
- [x] `.env` configured with valid credentials
- [x] Test script passes all tests
- [x] Application starts without errors
- [x] Browser opens to http://localhost:5000
- [x] Chat feature responds to messages

---

## 🎉 You're All Set!

Your NutriBot application is ready to provide personalized nutrition guidance!

**Enjoy your journey to better health! 🍎💪**

---

## 🆘 Need Help?

1. Run the test script: `python test_app.py`
2. Check the terminal for error messages
3. Review the troubleshooting section above
4. Verify your IBM Cloud credentials
5. Check IBM Cloud service status

---

*Last Updated: June 12, 2026*
*Version: 1.0.0*