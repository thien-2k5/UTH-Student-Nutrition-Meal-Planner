# pyrefly: ignore [missing-import]
import pytest
from app import create_app
from database.db import db
from models.food import Food
from services.calculator import calculate_bmi, calculate_bmr, calculate_tdee
from services.recommender import recommend_menu
from services.chatbot import extract_parameters, get_rule_response

# Define test config
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test_secret_key"

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(TestConfig)
    
    # Create tables and insert sample foods for tests
    with app.app_context():
        db.create_all()
        
        # Add sample foods
        sample_foods = [
            # Sáng
            Food(name="Bánh mì", price=15000, protein=10, fat=8, carb=40, fiber=2, vitamin="B", calories=300, category="Sáng"),
            # Trưa/Tối
            Food(name="Cơm tấm sườn", price=30000, protein=25, fat=15, carb=70, fiber=2, vitamin="B, Sắt", calories=500, category="Trưa/Tối"),
            Food(name="Cơm thịt kho", price=25000, protein=20, fat=18, carb=68, fiber=1.5, vitamin="B", calories=480, category="Trưa/Tối"),
            # Ăn vặt / Nước uống
            Food(name="Sữa đậu nành", price=6000, protein=6, fat=4, carb=12, fiber=1.5, vitamin="E", calories=100, category="Nước uống")
        ]
        db.session.bulk_save_objects(sample_foods)
        db.session.commit()
        
    yield app
    
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

# ================= 1. CALCULATOR TESTS =================

def test_calculate_bmi():
    # Weight 60kg, Height 170cm
    bmi, classification = calculate_bmi(60.0, 170.0)
    assert bmi == 20.76
    assert classification == "Bình thường"
    
    # Weight 45kg, Height 170cm
    bmi_under, class_under = calculate_bmi(45.0, 170.0)
    assert bmi_under < 18.5
    assert class_under == "Gầy"
    
    # Weight 80kg, Height 170cm
    bmi_over, class_over = calculate_bmi(80.0, 170.0)
    assert 25.0 <= bmi_over < 30.0
    assert class_over == "Thừa cân"

def test_calculate_bmr():
    # Male: 10*60 + 6.25*170 - 5*20 + 5 = 600 + 1062.5 - 100 + 5 = 1567.5
    bmr_male = calculate_bmr(60.0, 170.0, 20, "nam")
    assert bmr_male == 1567.5
    
    # Female: 10*60 + 6.25*170 - 5*20 - 161 = 600 + 1062.5 - 100 - 161 = 1401.5
    bmr_female = calculate_bmr(60.0, 170.0, 20, "nữ")
    assert bmr_female == 1401.5

def test_calculate_tdee():
    bmr = 1500.0
    # sedentary factor 1.2
    tdee = calculate_tdee(bmr, "sedentary")
    assert tdee == 1800.0
    
    # moderately active factor 1.55
    tdee_active = calculate_tdee(bmr, "moderately_active")
    assert tdee_active == 2325.0

# ================= 2. RECOMMENDER TESTS =================

def test_recommend_menu(app):
    with app.app_context():
        # Target calories: 1400 kcal, Budget: 80,000 VND
        result = recommend_menu(1400.0, 80000.0)
        assert result["success"] is True
        assert len(result["menu"]) == 4
        assert result["metrics"]["total_cost"] <= 80000.0
        
        # Test low budget fallback
        result_fallback = recommend_menu(1800.0, 10000.0)
        assert result_fallback["success"] is True
        assert "warning" in result_fallback
        assert result_fallback["metrics"]["total_cost"] > 10000.0  # Cheapeast combined is 15k+30k+25k+6k = 76k

# ================= 3. CHATBOT REGEX TESTS =================

def test_extract_parameters():
    state = {}
    msg = "Mình cao 175cm nặng 65kg nặng 21 tuổi nam ngân sách 80k"
    updated = extract_parameters(msg, state)
    
    assert updated.get("height") == 175.0
    assert updated.get("weight") == 65.0
    assert updated.get("age") == 21
    assert updated.get("gender") == "nam"
    assert updated.get("budget") == 80000.0

def test_chatbot_rule_response(app):
    with app.app_context():
        state = {}
        # Asking general nutrient info
        reply, updated_state = get_rule_response("protein là gì?", state)
        assert "Chất đạm" in reply
        
        # Nudging missing params
        reply2, updated_state2 = get_rule_response("mình cao 170cm nặng 60kg", state)
        assert "Đã ghi nhận thông tin" in reply2
        assert updated_state2.get("height") == 170.0
        assert updated_state2.get("weight") == 60.0

# ================= 4. VIEW ROUTING TESTS =================

def test_page_routing(client):
    # Verify index page loads
    res = client.get("/")
    assert res.status_code == 200
    assert b"UTH" in res.data
    
    # Verify other pages load
    assert client.get("/bmi").status_code == 200
    assert client.get("/recommend").status_code == 200
    assert client.get("/chat").status_code == 200
    assert client.get("/knowledge").status_code == 200
    assert client.get("/about").status_code == 200

# ================= 5. API ENDPOINT TESTS =================

def test_api_bmi(client):
    res = client.post("/api/bmi", json={
        "weight": 60,
        "height": 170,
        "age": 20,
        "gender": "nam",
        "activity": "sedentary"
    })
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data["success"] is True
    assert json_data["bmi"] == 20.76

def test_api_recommend(client):
    res = client.post("/api/recommend", json={
        "weight": 60,
        "height": 170,
        "age": 20,
        "gender": "nam",
        "activity": "sedentary",
        "budget": 80000,
        "goal": "maintain"
    })
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data["success"] is True
    assert "metrics" in json_data

def test_api_chat(client):
    res = client.post("/api/chat", json={
        "message": "chào chatbot"
    })
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data["success"] is True
    assert "reply" in json_data

def test_api_foods(client):
    res = client.get("/api/foods?q=B%C3%A1nh+m%C3%AC")
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data["success"] is True
    assert json_data["count"] == 1
    assert json_data["foods"][0]["name"] == "Bánh mì"
