from flask import Blueprint, render_template, request, jsonify, session
from app.database import db
from app.models.food import Food
from app.services.calculator import calculate_bmi, calculate_bmr, calculate_tdee
from app.services.recommender import recommend_menu
from app.services.chatbot import get_chatbot_response
import logging

logger = logging.getLogger(__name__)
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home/Landing Page."""
    return render_template('index.html')

@main_bp.route('/bmi')
def bmi_page():
    """BMI Calculator Page."""
    return render_template('bmi.html')

@main_bp.route('/recommend')
def recommend_page():
    """Meal Recommendation Dashboard Page."""
    return render_template('recommend.html')

@main_bp.route('/chat')
def chat_page():
    """Dedicated Chatbot Page."""
    return render_template('chat.html')

@main_bp.route('/knowledge')
def knowledge_page():
    """Nutritional Knowledge Guide Page."""
    return render_template('knowledge.html')

@main_bp.route('/about')
def about_page():
    """About & Credits Page."""
    return render_template('about.html')

# ================= API ENDPOINTS =================

@main_bp.route('/api/bmi', methods=['POST'])
def api_bmi():
    """Calculate BMI, BMR, and TDEE."""
    try:
        data = request.get_json() or {}
        weight = float(data.get('weight', 0))
        height = float(data.get('height', 0))
        age = int(data.get('age', 0))
        gender = data.get('gender', 'nam')
        activity = data.get('activity', 'sedentary')
        
        if weight <= 0 or height <= 0 or age <= 0:
            return jsonify({'success': False, 'error': 'Thông số chiều cao, cân nặng, tuổi phải lớn hơn 0.'}), 400
            
        bmi, classification = calculate_bmi(weight, height)
        bmr = calculate_bmr(weight, height, age, gender)
        tdee = calculate_tdee(bmr, activity)
        
        # Save in session for chatbot/recommender context
        session['user_metrics'] = {
            'weight': weight,
            'height': height,
            'age': age,
            'gender': gender,
            'activity': activity,
            'bmi': bmi,
            'classification': classification,
            'bmr': bmr,
            'tdee': tdee
        }
        
        return jsonify({
            'success': True,
            'bmi': bmi,
            'classification': classification,
            'bmr': bmr,
            'tdee': tdee
        })
    except ValueError:
        return jsonify({'success': False, 'error': 'Định dạng dữ liệu không hợp lệ.'}), 400
    except Exception as e:
        logger.error(f"Error in api_bmi: {str(e)}")
        return jsonify({'success': False, 'error': 'Lỗi máy chủ nội bộ.'}), 500

@main_bp.route('/api/recommend', methods=['POST'])
def api_recommend():
    """Generate daily meal recommendation based on target calories, budget, and goal."""
    try:
        data = request.get_json() or {}
        weight = float(data.get('weight', 0))
        height = float(data.get('height', 0))
        age = int(data.get('age', 0))
        gender = data.get('gender', 'nam')
        activity = data.get('activity', 'sedentary')
        budget = float(data.get('budget', 50000))
        goal = data.get('goal', 'maintain')  # lose, maintain, gain
        
        if weight <= 0 or height <= 0 or age <= 0:
            return jsonify({'success': False, 'error': 'Thông số chiều cao, cân nặng, tuổi phải lớn hơn 0.'}), 400
            
        # Calculate stats
        bmi, classification = calculate_bmi(weight, height)
        bmr = calculate_bmr(weight, height, age, gender)
        tdee = calculate_tdee(bmr, activity)
        
        # Save in session
        session['user_metrics'] = {
            'weight': weight,
            'height': height,
            'age': age,
            'gender': gender,
            'activity': activity,
            'bmi': bmi,
            'classification': classification,
            'bmr': bmr,
            'tdee': tdee,
            'budget': budget,
            'goal': goal
        }
        
        # Calorie adjustment based on goal
        if goal == 'lose':
            target_calories = max(1200.0, tdee - 400.0)
        elif goal == 'gain':
            target_calories = tdee + 400.0
        else:
            target_calories = tdee
            
        # Generate menu recommendation
        rec_result = recommend_menu(target_calories, budget)
        rec_result['bmi'] = bmi
        rec_result['classification'] = classification
        rec_result['tdee'] = tdee
        rec_result['target_calories'] = target_calories
        
        return jsonify(rec_result)
    except ValueError:
        return jsonify({'success': False, 'error': 'Định dạng dữ liệu không hợp lệ.'}), 400
    except Exception as e:
        logger.error(f"Error in api_recommend: {str(e)}")
        return jsonify({'success': False, 'error': 'Lỗi máy chủ nội bộ.'}), 500

@main_bp.route('/api/chat', methods=['POST'])
def api_chat():
    """Chatbot Endpoint."""
    try:
        data = request.get_json() or {}
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'success': False, 'error': 'Tin nhắn trống.'}), 400
            
        # Retrieve chatbot state from session or initialize
        chatbot_state = session.get('chatbot_state', {})
        
        # Get response and update chatbot state
        reply, updated_state = get_chatbot_response(message, chatbot_state)
        session['chatbot_state'] = updated_state
        
        return jsonify({
            'success': True,
            'reply': reply,
            'state': updated_state
        })
    except Exception as e:
        logger.error(f"Error in api_chat: {str(e)}")
        return jsonify({'success': False, 'error': 'Lỗi chatbot.'}), 500

@main_bp.route('/api/foods', methods=['GET'])
def api_foods():
    """Retrieve, search, and filter food items."""
    try:
        query_str = request.args.get('q', '').strip()
        category = request.args.get('category', '').strip()
        max_price = request.args.get('max_price', type=float)
        max_calories = request.args.get('max_calories', type=float)
        
        # Query DB
        db_query = Food.query
        
        if query_str:
            db_query = db_query.filter(Food.name.like(f"%{query_str}%"))
            
        if category:
            db_query = db_query.filter(Food.category == category)
            
        if max_price is not None:
            db_query = db_query.filter(Food.price <= max_price)
            
        if max_calories is not None:
            db_query = db_query.filter(Food.calories <= max_calories)
            
        foods = db_query.all()
        return jsonify({
            'success': True,
            'count': len(foods),
            'foods': [f.to_dict() for f in foods]
        })
    except Exception as e:
        logger.error(f"Error in api_foods: {str(e)}")
        return jsonify({'success': False, 'error': 'Lỗi lấy dữ liệu món ăn.'}), 500
