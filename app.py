from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import os
import json
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai import Credentials

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# ============================================================================
# AGENT INSTRUCTIONS - CUSTOMIZE YOUR NUTRITION AGENT HERE
# ============================================================================
AGENT_INSTRUCTIONS = """
You are NutriBot, an expert AI Nutrition Agent specializing in personalized nutrition guidance.

## Your Role & Tone:
- Be friendly, supportive, and encouraging
- Use a warm, conversational tone while maintaining professionalism
- Show empathy and understanding towards users' dietary challenges
- Be culturally sensitive, especially regarding Indian cuisine and dietary practices

## Specializations:
- Personalized nutrition planning based on age, weight, height, activity level
- Calorie counting and macronutrient analysis
- Indian cuisine expertise (North Indian, South Indian, regional specialties)
- Vegetarian, vegan, and non-vegetarian diet planning
- Family nutrition and meal planning for multiple members
- Weight management (loss, gain, maintenance)
- Sports nutrition and fitness diets
- Medical dietary considerations (diabetes, hypertension, PCOS, etc.)

## Indian Food Preferences:
- Prioritize traditional Indian meals: dal, roti, rice, sabzi, curry
- Include regional favorites: dosa, idli, paratha, biryani, khichdi
- Suggest healthy Indian snacks: roasted chana, makhana, fruits
- Recommend Indian superfoods: turmeric, ghee, millets, lentils
- Provide portion sizes in Indian measurements (katori, roti count)
- Consider Indian meal timing: breakfast, lunch, evening snacks, dinner

## Safety Rules & Limitations:
- NEVER provide medical diagnosis or treatment advice
- ALWAYS recommend consulting healthcare professionals for medical conditions
- Do NOT suggest extreme diets or rapid weight loss methods
- AVOID recommending supplements without professional consultation
- NEVER encourage eating disorders or unhealthy relationships with food
- Respect religious and cultural dietary restrictions (vegetarian, Jain, halal, etc.)
- If asked about serious medical conditions, advise seeing a doctor/dietitian

## Response Format:
- Provide clear, actionable nutrition advice
- Include specific meal suggestions with approximate calories
- Break down macronutrients (protein, carbs, fats) when relevant
- Offer practical tips for Indian households
- Use bullet points and structured formatting for clarity
- Include portion sizes and serving suggestions

## When Creating Meal Plans:
- Consider Indian meal patterns and timing
- Balance traditional foods with nutritional needs
- Suggest affordable, locally available ingredients
- Provide vegetarian alternatives for all meals
- Include hydration recommendations (water, buttermilk, coconut water)
- Add healthy Indian cooking methods (steaming, grilling, tadka)

Remember: Your goal is to empower users with knowledge and practical nutrition guidance while respecting Indian culture, dietary preferences, and safety guidelines.
"""

# ============================================================================
# IBM Watsonx.ai Configuration
# ============================================================================

def get_watsonx_model():
    """Initialize and return IBM Watsonx.ai model"""
    try:
        credentials = Credentials(
            url=os.getenv('IBM_CLOUD_URL', 'https://au-syd.ml.cloud.ibm.com'),
            api_key=os.getenv('IBM_CLOUD_API_KEY')
        )
        
        project_id = os.getenv('IBM_WATSONX_PROJECT_ID')
        
        model = ModelInference(
            model_id='ibm/granite-guardian-3-8b​​',
            params={
                GenParams.DECODING_METHOD: "greedy",
                GenParams.MAX_NEW_TOKENS: 900,
                GenParams.MIN_NEW_TOKENS: 50,
                GenParams.TEMPERATURE: 0.7,
                GenParams.TOP_K: 50,
                GenParams.TOP_P: 1
            },
            credentials=credentials,
            project_id=project_id
        )
        
        return model
    except Exception as e:
        print(f"Error initializing Watsonx model: {str(e)}")
        return None

# ============================================================================
# Routes
# ============================================================================

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages with nutrition agent"""
    try:
        data = request.json
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get Watsonx model
        model = get_watsonx_model()
        if not model:
            return jsonify({'error': 'Failed to initialize AI model. Please check your API credentials.'}), 500
        
        # Build conversation context
        context = AGENT_INSTRUCTIONS + "\n\n## Conversation History:\n"
        for msg in conversation_history[-5:]:  # Last 5 messages for context
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            context += f"{role.capitalize()}: {content}\n"
        
        context += f"\nUser: {user_message}\nAssistant:"
        
        # Generate response
        response = model.generate_text(prompt=context)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/calculate-bmi', methods=['POST'])
def calculate_bmi():
    """Calculate BMI and provide recommendations"""
    try:
        data = request.json
        weight = float(data.get('weight', 0))
        height = float(data.get('height', 0))
        
        if weight <= 0 or height <= 0:
            return jsonify({'error': 'Invalid weight or height'}), 400
        
        # Calculate BMI
        height_m = height / 100  # Convert cm to meters
        bmi = weight / (height_m ** 2)
        
        # Determine category
        if bmi < 18.5:
            category = 'Underweight'
            color = 'info'
            recommendation = 'Consider increasing calorie intake with nutritious foods.'
        elif 18.5 <= bmi < 25:
            category = 'Normal'
            color = 'success'
            recommendation = 'Maintain your healthy weight with balanced diet and exercise.'
        elif 25 <= bmi < 30:
            category = 'Overweight'
            color = 'warning'
            recommendation = 'Focus on portion control and regular physical activity.'
        else:
            category = 'Obese'
            color = 'danger'
            recommendation = 'Consult a healthcare professional for personalized guidance.'
        
        return jsonify({
            'bmi': round(bmi, 2),
            'category': category,
            'color': color,
            'recommendation': recommendation,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': f'Calculation error: {str(e)}'}), 500

@app.route('/generate-meal-plan', methods=['POST'])
def generate_meal_plan():
    """Generate personalized meal plan"""
    try:
        data = request.json
        profile = data.get('profile', {})
        preferences = data.get('preferences', {})
        
        # Build prompt for meal plan generation
        prompt = f"""{AGENT_INSTRUCTIONS}

Generate a detailed one-day Indian meal plan for:
- Age: {profile.get('age', 'Not specified')}
- Weight: {profile.get('weight', 'Not specified')} kg
- Height: {profile.get('height', 'Not specified')} cm
- Activity Level: {profile.get('activity', 'Moderate')}
- Diet Type: {preferences.get('diet_type', 'Vegetarian')}
- Goal: {preferences.get('goal', 'Maintain weight')}
- Cuisine Preference: {preferences.get('cuisine', 'North Indian')}

Provide a structured meal plan with:
1. Breakfast (with calories)
2. Mid-morning snack
3. Lunch (with calories)
4. Evening snack
5. Dinner (with calories)
6. Total daily calories
7. Macronutrient breakdown

Make it practical, affordable, and suitable for Indian households.
"""
        
        model = get_watsonx_model()
        if not model:
            return jsonify({'error': 'Failed to initialize AI model'}), 500
        
        meal_plan = model.generate_text(prompt=prompt)
        
        return jsonify({
            'meal_plan': meal_plan,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error generating meal plan: {str(e)}'}), 500

@app.route('/analyze-food', methods=['POST'])
def analyze_food():
    """Analyze nutritional content of food items"""
    try:
        data = request.json
        food_items = data.get('food_items', '')
        
        if not food_items:
            return jsonify({'error': 'No food items provided'}), 400
        
        prompt = f"""{AGENT_INSTRUCTIONS}

Analyze the nutritional content of the following Indian food items:
{food_items}

Provide:
1. Approximate calories for each item
2. Protein, carbs, and fat content
3. Health benefits
4. Portion size recommendations
5. Healthier alternatives if applicable

Be specific and practical for Indian context.
"""
        
        model = get_watsonx_model()
        if not model:
            return jsonify({'error': 'Failed to initialize AI model'}), 500
        
        analysis = model.generate_text(prompt=prompt)
        
        return jsonify({
            'analysis': analysis,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error analyzing food: {str(e)}'}), 500

@app.route('/family-profile', methods=['POST'])
def save_family_profile():
    """Save family member profiles"""
    try:
        data = request.json
        family_members = data.get('members', [])
        
        # Store in session (in production, use database)
        session['family_members'] = family_members
        
        return jsonify({
            'message': 'Family profiles saved successfully',
            'count': len(family_members),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error saving profiles: {str(e)}'}), 500

@app.route('/get-family-profile', methods=['GET'])
def get_family_profile():
    """Retrieve family member profiles"""
    try:
        family_members = session.get('family_members', [])
        
        return jsonify({
            'members': family_members,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error retrieving profiles: {str(e)}'}), 500

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
