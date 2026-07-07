import re
import os
import logging
import unicodedata
import requests
from app.services.calculator import calculate_bmi, calculate_bmr, calculate_tdee
from app.services.recommender import recommend_menu

logger = logging.getLogger(__name__)


def normalize_text(text: str) -> str:
    """Normalize Vietnamese text so matching is robust to accents and punctuation."""
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def contains_keyword(text: str, keyword: str) -> bool:
    """Check whether a normalized keyword appears as a distinct word or phrase."""
    normalized_text = normalize_text(text)
    normalized_keyword = normalize_text(keyword)
    if not normalized_keyword:
        return False
    return re.search(rf"(^|\s){re.escape(normalized_keyword)}($|\s)", normalized_text) is not None


# Basic keywords for rule-based matching
NUTRITION_ANSWERS = {
    "chao": "Xin chào! Mình là Trợ lý Dinh dưỡng UTH. Bạn có thể chia sẻ thông tin thể trạng (chiều cao, cân nặng, tuổi, giới tính, mức vận động, ngân sách ăn uống) để mình tính BMI, TDEE và gợi ý thực đơn thích hợp nhé! (Ví dụ: 'Tôi cao 170cm, nặng 60kg, 20 tuổi, nam, ngân sách 70k')",
    "hello": "Xin chào! Mình là Trợ lý Dinh dưỡng UTH. Bạn có thể chia sẻ thông tin thể trạng (chiều cao, cân nặng, tuổi, giới tính, mức vận động, ngân sách ăn uống) để mình tính BMI, TDEE và gợi ý thực đơn thích hợp nhé! (Ví dụ: 'Tôi cao 170cm, nặng 60kg, 20 tuổi, nam, ngân sách 70k')",
    "hi": "Xin chào! Mình là Trợ lý Dinh dưỡng UTH. Bạn có thể chia sẻ thông tin thể trạng (chiều cao, cân nặng, tuổi, giới tính, mức vận động, ngân sách ăn uống) để mình tính BMI, TDEE và gợi ý thực đơn thích hợp nhé! (Ví dụ: 'Tôi cao 170cm, nặng 60kg, 20 tuổi, nam, ngân sách 70k')",
    "protein": "Protein (Chất đạm) là chất dinh dưỡng thiết yếu giúp xây dựng cơ bắp, sửa chữa tế bào và tăng cường hệ miễn dịch. Với sinh viên UTH, các nguồn protein giá rẻ, chất lượng gồm: trứng gà luộc (5k/quả), ức gà (30k/phần), đậu hũ (5k/miếng), sữa đậu nành UTH (6k/ly), cá nục kho cà chua (22k/phần). Bạn nên ăn khoảng 1.2g - 1.8g protein trên mỗi kg trọng lượng cơ thể.",
    "dam": "Protein (Chất đạm) là chất dinh dưỡng thiết yếu giúp xây dựng cơ bắp, sửa chữa tế bào và tăng cường hệ miễn dịch. Với sinh viên UTH, các nguồn protein giá rẻ, chất lượng gồm: trứng gà luộc (5k/quả), ức gà (30k/phần), đậu hũ (5k/miếng), sữa đậu nành UTH (6k/ly), cá nục kho cà chua (22k/phần). Bạn nên ăn khoảng 1.2g - 1.8g protein trên mỗi kg trọng lượng cơ thể.",
    "carb": "Carb (Tinh bột/Đường) cung cấp năng lượng chính cho não bộ hoạt động và cơ thể học tập cả ngày. Bạn nên ưu tiên tinh bột phức (hấp thu chậm, giàu chất xơ) như: khoai lang luộc (6k/củ), yến mạch (18k/phần), ngô luộc (8k/bắp). Hạn chế tinh bột nhanh từ nước ngọt, trà sữa nhiều đường để tránh buồn ngủ trong giờ học nhé!",
    "tinh bot": "Carb (Tinh bột/Đường) cung cấp năng lượng chính cho não bộ hoạt động và cơ thể học tập cả ngày. Bạn nên ưu tiên tinh bột phức (hấp thu chậm, giàu chất xơ) như: khoai lang luộc (6k/củ), yến mạch (18k/phần), ngô luộc (8k/bắp). Hạn chế tinh bột nhanh từ nước ngọt, trà sữa nhiều đường để tránh buồn ngủ trong giờ học nhé!",
    "fat": "Fat (Chất béo) cần thiết cho việc hấp thụ vitamin (A, D, E, K) và điều hòa hormone. Nên bổ sung chất béo tốt từ hạt điều, đậu phộng rang (10k-20k/gói), mỡ cá (cá hú, cá lóc, cá điêu hồng). Hạn chế chất béo bão hòa từ đồ chiên dầu mỡ đun đi đun lại ở các quán cơm bụi vỉa hè nhé!",
    "chat beo": "Fat (Chất béo) cần thiết cho việc hấp thụ vitamin (A, D, E, K) và điều hòa hormone. Nên bổ sung chất béo tốt từ hạt điều, đậu phộng rang (10k-20k/gói), mỡ cá (cá hú, cá lóc, cá điêu hồng). Hạn chế chất béo bão hòa từ đồ chiên dầu mỡ đun đi đun lại ở các quán cơm bụi vỉa hè nhé!",
    "fiber": "Chất xơ rất quan trọng cho tiêu hóa, giúp no lâu và ổn định đường huyết. Sinh viên nên bổ sung rau muống luộc, rau ngót, bí đỏ, cà chua hoặc bông cải xanh từ các bữa cơm tiệm (yêu cầu xin thêm rau), hoặc ăn chuối chín (3k/quả), trái cây tô (25k/phần).",
    "xo": "Chất xơ rất quan trọng cho tiêu hóa, giúp no lâu và ổn định đường huyết. Sinh viên nên bổ sung rau muống luộc, rau ngót, bí đỏ, cà chua hoặc bông cải xanh từ các bữa cơm tiệm (yêu cầu xin thêm rau), hoặc ăn chuối chín (3k/quả), trái cây tô (25k/phần).",
    "vitamin": "Vitamins và khoáng chất có trong rau củ, quả tươi giúp tăng sức đề kháng, tránh ốm vặt khi mùa thi đến. Hãy bổ sung nước cam vắt (15k), chanh dây (12k), sinh tố đu đủ (15k) hoặc đơn giản là ăn nhiều rau xanh trong bữa trưa/tối.",
    "nuoc": "Uống đủ nước giúp thanh lọc cơ thể, giảm mệt mỏi và tập trung học tập. Công thức: Cân nặng (kg) x 0.04 = Số lít nước cần uống mỗi ngày (ví dụ 50kg cần khoảng 2 lít nước). Hãy mang theo bình nước cá nhân khi lên giảng đường UTH nhé!",
    "luong nuoc": "Uống đủ nước giúp thanh lọc cơ thể, giảm mệt mỏi và tập trung học tập. Công thức: Cân nặng (kg) x 0.04 = Số lít nước cần uống mỗi ngày (ví dụ 50kg cần khoảng 2 lít nước). Hãy mang theo bình nước cá nhân khi lên giảng đường UTH nhé!",
    "uong bao nhieu nuoc": "Uống đủ nước giúp thanh lọc cơ thể, giảm mệt mỏi và tập trung học tập. Công thức: Cân nặng (kg) x 0.04 = Số lít nước cần uống mỗi ngày (ví dụ 50kg cần khoảng 2 lít nước). Hãy mang theo bình nước cá nhân khi lên giảng đường UTH nhé!",
    "bmi": "BMI (Body Mass Index) là Chỉ số khối cơ thể. Công thức = Cân nặng (kg) / [Chiều cao (m) * Chiều cao (m)]. Phân loại: Gầy (<18.5), Bình thường (18.5-24.9), Thừa cân (25-29.9), Béo phì (>=30). Bạn muốn mình tính BMI giúp không? Hãy nhắn chiều cao và cân nặng nhé!",
    "tdee": "TDEE (Total Daily Energy Expenditure) là tổng năng lượng cơ thể tiêu hao trong một ngày, bao gồm cả các hoạt động thể chất và tiêu hóa. TDEE quyết định việc bạn cần ăn bao nhiêu calo để tăng, giảm hoặc duy trì cân nặng.",
    "goi y mon an": "Mình có thể gợi ý thực đơn ăn uống phù hợp với BMI, TDEE và ngân sách của bạn. Hãy gửi chiều cao, cân nặng, tuổi, giới tính và ngân sách mỗi ngày để mình đề xuất 4 bữa hợp lý nhé!",
    "thuc don": "Mình có thể gợi ý thực đơn ăn uống phù hợp với BMI, TDEE và ngân sách của bạn. Hãy gửi chiều cao, cân nặng, tuổi, giới tính và ngân sách mỗi ngày để mình đề xuất 4 bữa hợp lý nhé!",
    "de xuat mon an": "Mình có thể gợi ý thực đơn ăn uống phù hợp với BMI, TDEE và ngân sách của bạn. Hãy gửi chiều cao, cân nặng, tuổi, giới tính và ngân sách mỗi ngày để mình đề xuất 4 bữa hợp lý nhé!",
    "uth": "Chào người bạn UTH! Trường Đại học Giao thông vận tải TP.HCM nổi tiếng với tinh thần năng động. Học tập tại UTH đòi hỏi nhiều năng lượng, hãy để mình đồng hành giúp bạn ăn uống khoa học, tiết kiệm và khỏe mạnh nhé!",
    "cam on": "Không có gì nè! Chúc bạn học tập thật tốt tại UTH và luôn giữ gìn sức khỏe dinh dưỡng nhé!",
    "thanks": "Không có gì nè! Chúc bạn học tập thật tốt tại UTH và luôn giữ gìn sức khỏe dinh dưỡng nhé!"
}

def extract_parameters(message: str, current_state: dict) -> dict:
    """Extract height, weight, age, gender, activity level, budget from text using regex."""
    state = current_state.copy()
    message = normalize_text(message)
    
    # 1. Height (e.g. 170cm, cao 1.7m, cao 170, 170)
    height_match = re.search(r'(?:cao|chiều cao)?\s*(1[4-9]\d|20\d)\s*(?:cm|centimet)?', message)
    if not height_match:
        height_match = re.search(r'(?:cao|chiều cao)?\s*(1\.[5-9]\d?)\s*(?:m|met|mét)?', message)
        if height_match:
            state['height'] = float(height_match.group(1)) * 100.0
    else:
        state['height'] = float(height_match.group(1))
        
    # 2. Weight (e.g. nặng 60kg, 60 kg, 60kg)
    weight_match = re.search(r'(?:nặng|cân nặng)?\s*([3-9]\d|1[0-4]\d)\s*(?:kg|ký|kí|kilogam)', message)
    if not weight_match:
        weight_match = re.search(r'nặng\s*([3-9]\d|1[0-4]\d)', message)
    if weight_match:
        state['weight'] = float(weight_match.group(1))
        
    # 3. Age (e.g. 18 tuổi, 18t, 18tuoi)
    age_match = re.search(r'(\d{2})\s*(?:tuổi|tuoi|t\b)', message)
    if age_match:
        state['age'] = int(age_match.group(1))
        
    # 4. Gender (nam/nữ/male/female)
    if 'nam' in message or 'male' in message:
        state['gender'] = 'nam'
    elif 'nữ' in message or 'nu' in message or 'female' in message:
        state['gender'] = 'nữ'
        
    # 5. Activity level
    if 'ít vận động' in message or 'tĩnh tại' in message or 'ngồi nhiều' in message:
        state['activity'] = 'sedentary'
    elif 'vận động nhẹ' in message or 'đi bộ nhẹ' in message or 'tập nhẹ' in message:
        state['activity'] = 'lightly_active'
    elif 'vận động vừa' in message or 'tập thể thao' in message or 'thể thao vừa' in message:
        state['activity'] = 'moderately_active'
    elif 'vận động nhiều' in message or 'tập nặng' in message or 'chạy bộ nhiều' in message:
        state['activity'] = 'very_active'
    elif 'vận động cực nhiều' in message or 'extra active' in message:
        state['activity'] = 'extra_active'
        
    # 6. Budget (e.g. 50k, 50.000đ, ngân sách 70k, 70000đ)
    budget_match = re.search(r'(?:ngân sách|tiền|chi phí)?\s*(\d+)\s*(?:k\b|ngàn|nghin|đ|vnd|đồng)', message)
    if budget_match:
        val = int(budget_match.group(1))
        if val < 1000:
            state['budget'] = val * 1000.0
        else:
            state['budget'] = float(val)
    else:
        money_match = re.search(r'\b(\d{2,3})000\b', message)
        if money_match:
            state['budget'] = float(money_match.group(0))
            
    return state

def get_rule_response(message: str, state: dict) -> tuple[str, dict]:
    """Process message using rules and context state."""
    normalized = normalize_text(message)
    updated_state = extract_parameters(message, state)

    # Handle knowledge questions before profile-based recommendation flow.
    knowledge_keywords = [
        "protein", "chat dam", "carb", "tinh bot", "fat", "chat beo", "fiber", "chat xo",
        "vitamin", "vitamin va khoang chat", "nuoc", "uong bao nhieu nuoc", "bmi", "tdee",
        "can uong", "uong du nuoc", "protein la gi", "cong thuc", "luong nuoc"
    ]
    if any(contains_keyword(normalized, keyword) for keyword in knowledge_keywords):
        for kw, ans in NUTRITION_ANSWERS.items():
            if contains_keyword(normalized, kw):
                return ans, updated_state

    gained_new = False
    for k, v in updated_state.items():
        if state.get(k) != v:
            gained_new = True
            
    missing = []
    if 'height' not in updated_state:
        missing.append("chiều cao (cm)")
    if 'weight' not in updated_state:
        missing.append("cân nặng (kg)")
    if 'age' not in updated_state:
        missing.append("tuổi")
    if 'gender' not in updated_state:
        missing.append("giới tính (nam/nữ)")
    if 'budget' not in updated_state:
        missing.append("ngân sách ăn/ngày (đ)")
        
    if not missing:
        h = updated_state['height']
        w = updated_state['weight']
        a = updated_state['age']
        g = updated_state['gender']
        act = updated_state.get('activity', 'sedentary')
        b = updated_state['budget']
        
        bmi, bmi_class = calculate_bmi(w, h)
        bmr = calculate_bmr(w, h, a, g)
        tdee = calculate_tdee(bmr, act)
        
        if bmi_class == "Gầy":
            target_cal = tdee + 400
            goal_text = "tăng cân an toàn (thặng dư calo)"
        elif bmi_class == "Thừa cân" or bmi_class == "Béo phì":
            target_cal = max(1200.0, tdee - 400)
            goal_text = "giảm cân lành mạnh (thâm hụt calo)"
        else:
            target_cal = tdee
            goal_text = "duy trì cân nặng khỏe mạnh"
            
        rec = recommend_menu(target_cal, b)
        
        resp = f"### 📊 Kết Quả Phân Tích Dinh Dưỡng\n"
        resp += f"- **BMI của bạn**: {bmi} (Thể trạng: **{bmi_class}**)\n"
        resp += f"- **Chỉ số BMR (Năng lượng nền)**: {bmr:,.0f} kcal\n"
        resp += f"- **TDEE (Năng lượng tiêu hao mỗi ngày)**: {tdee:,.0f} kcal\n"
        resp += f"- **Mục tiêu năng lượng khuyên dùng**: **{target_cal:,.0f} kcal** để hỗ trợ **{goal_text}**.\n\n"
        
        if rec.get("success") and rec.get("menu"):
            if "warning" in rec:
                resp += f"⚠️ *{rec['warning']}*\n\n"
            resp += f"### 🍽️ Thực Đơn Đề Xuất (Tổng chi phí: {rec['metrics']['total_cost']:,.0f}đ)\n"
            
            meals = ["Bữa Sáng", "Bữa Trưa", "Bữa Tối", "Bữa Phụ"]
            for idx, item in enumerate(rec["menu"]):
                meal_name = meals[idx]
                resp += f"- **{meal_name}**: *{item['name']}*\n"
                resp += f"  - Giá: {item['price']:,.0f}đ | Năng lượng: {item['calories']:.0f} kcal\n"
                resp += f"  - Protein: {item['protein']}g | Carb: {item['carb']}g | Fat: {item['fat']}g\n"
                
            resp += f"\n**Tổng dinh dưỡng ngày**:\n"
            resp += f"- Calories: {rec['metrics']['total_calories']:.0f} kcal / {target_cal:,.0f} kcal\n"
            resp += f"- Protein: {rec['metrics']['total_protein']}g | Carb: {rec['metrics']['total_carb']}g | Fat: {rec['metrics']['total_fat']}g\n\n"
            resp += f"💡 *Lời khuyên*: Bạn hãy giữ thói quen uống đủ nước (~{w*0.04:.1f} lít/ngày) và kết hợp đi bộ/tập thể dục nhẹ 30 phút mỗi ngày nhé!"
        else:
            resp += f"❌ Không thể tìm thấy thực đơn phù hợp trong tầm giá {b:,.0f}đ. Vui lòng thử tăng ngân sách ăn uống mỗi ngày nhé!"
            
        return resp, updated_state
        
    if gained_new and missing:
        received = []
        if 'height' in updated_state: received.append(f"Chiều cao: {updated_state['height']}cm")
        if 'weight' in updated_state: received.append(f"Cân nặng: {updated_state['weight']}kg")
        if 'age' in updated_state: received.append(f"Tuổi: {updated_state['age']}")
        if 'gender' in updated_state: received.append(f"Giới tính: {updated_state['gender']}")
        if 'budget' in updated_state: received.append(f"Ngân sách: {updated_state['budget']:,.0f}đ")
        
        nudge = f"Đã ghi nhận thông tin của bạn ({', '.join(received)}).\n\nĐể hệ thống gợi ý thực đơn hoàn chỉnh nhất, xin vui lòng cung cấp thêm các thông tin còn thiếu sau:\n"
        for m in missing:
            nudge += f"- **{m}**\n"
        nudge += "\n*Ví dụ: Bạn nhắn tiếp 'nặng 65kg, giới tính nam, ngân sách 80k'*"
        return nudge, updated_state
        
    for kw, ans in NUTRITION_ANSWERS.items():
        if contains_keyword(normalized, kw):
            return ans, updated_state
            
    fallback = (
        "Xin chào! Mình là Trợ lý Dinh dưỡng UTH. Mình có thể giúp bạn:\n"
        "1. Tính chỉ số BMI, TDEE và khuyên dùng thực đơn dựa trên chiều cao, cân nặng, tuổi, giới tính và ngân sách.\n"
        "2. Giải đáp kiến thức về Protein, Carbs, Chất béo, Nước uống.\n\n"
        "👉 *Bạn hãy nhắn tin theo mẫu: 'Mình cao 168cm, nặng 55kg, 20 tuổi, nữ, ngân sách 60k' để mình phân tích nhé!*"
    )
    return fallback, updated_state

def get_chatbot_response(message: str, state: dict) -> tuple[str, dict]:
    """Core entry point for chatbot, calling Gemini AI if API key is configured."""
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    
    state = extract_parameters(message, state)
    
    if not gemini_key and not openai_key:
        return get_rule_response(message, state)
        
    if gemini_key:
        try:
            sys_instruction = (
                "Bạn là chatbot dinh dưỡng học đường thông thái dành cho sinh viên trường UTH (Đại học GTVT TP.HCM). "
                "Hãy giao tiếp thân thiện, ngắn gọn, lịch sự, xưng hô 'Mình' - 'Bạn'. "
                "Bạn có quyền truy cập vào thông tin thể chất hiện tại của người dùng (nếu có):\n"
                f"- Chiều cao: {state.get('height', 'chưa có')} cm\n"
                f"- Cân nặng: {state.get('weight', 'chưa có')} kg\n"
                f"- Tuổi: {state.get('age', 'chưa có')} tuổi\n"
                f"- Giới tính: {state.get('gender', 'chưa có')}\n"
                f"- Ngân sách ăn: {state.get('budget', 'chưa có')} VND/ngày\n"
                f"- Mức vận động: {state.get('activity', 'sedentary')}\n\n"
                "Hãy trả lời người dùng ngắn gọn bằng tiếng Việt. Nếu người dùng cung cấp thông tin chiều cao, cân nặng, tuổi, giới tính, ngân sách, "
                "bạn hãy tính toán BMI, TDEE và gợi ý một số món ăn Việt Nam bình dân phù hợp (như cơm tấm, phở, bún riêu, trứng luộc, sữa đậu nành, chuối...). "
                "Luôn định dạng câu trả lời đẹp mắt bằng Markdown, dùng emoji và các thẻ bullet points rõ ràng."
            )
            
            headers = {"Content-Type": "application/json"}
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": f"System context:\n{sys_instruction}\n\nUser message: {message}"}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 800
                }
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                res_data = response.json()
                text_response = res_data['candidates'][0]['content']['parts'][0]['text']
                return text_response, state
        except Exception as e:
            logger.error(f"Gemini API call failed: {str(e)}")
            
    if openai_key:
        try:
            model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_key}"
            }
            url = "https://api.openai.com/v1/chat/completions"
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Bạn là chatbot dinh dưỡng dành cho sinh viên trường UTH. Hãy giao tiếp bằng tiếng Việt, "
                            "thân thiện, ngắn gọn và hữu ích. Dưới đây là thông tin thể chất người dùng được lưu trữ:\n"
                            f"Chiều cao: {state.get('height', 'chưa')}cm, Cân nặng: {state.get('weight', 'chưa')}kg, "
                            f"Tuổi: {state.get('age', 'chưa')}, Giới tính: {state.get('gender', 'chưa')}, "
                            f"Ngân sách: {state.get('budget', 'chưa')}đ. Hãy dùng thông tin này để tư vấn nếu thích hợp."
                        )
                    },
                    {"role": "user", "content": message}
                ],
                "temperature": 0.7,
                "max_tokens": 800
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                res_data = response.json()
                text_response = res_data['choices'][0]['message']['content']
                return text_response, state
        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            
    return get_rule_response(message, state)
