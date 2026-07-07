import random
import logging
from models.food import Food
from database.db import db

logger = logging.getLogger(__name__)

def recommend_menu(target_calories: float, max_budget: float) -> dict:
    """
    Recommend a 1-day meal plan consisting of:
    - Bữa sáng (Breakfast)
    - Bữa trưa (Lunch)
    - Bữa tối (Dinner)
    - Món phụ/Nước uống (Snack/Drink)
    
    Constraints:
    - Total cost <= max_budget
    - Total calories is close to target_calories (within ~15% if possible)
    - Optimize for protein
    """
    try:
        # Fetch all foods categorized
        all_foods = Food.query.all()
        
        breakfasts = [f for f in all_foods if f.category == "Sáng"]
        main_dishes = [f for f in all_foods if f.category == "Trưa/Tối"]
        snacks = [f for f in all_foods if f.category in ["Ăn vặt", "Nước uống"]]
        
        if not breakfasts or len(main_dishes) < 2 or not snacks:
            return {
                "success": False,
                "error": "Dữ liệu món ăn chưa đủ để đề xuất thực đơn.",
                "menu": []
            }
            
        # Try finding a random combination that fits budget and calorie targets
        best_combination = None
        best_score = -999999  # Calorie match & high protein score
        
        attempts = 3000
        for _ in range(attempts):
            b = random.choice(breakfasts)
            # Pick 2 distinct lunch/dinner items
            l = random.choice(main_dishes)
            d = random.choice(main_dishes)
            while d.id == l.id:
                d = random.choice(main_dishes)
                
            s = random.choice(snacks)
            
            total_cost = b.price + l.price + d.price + s.price
            total_cal = b.calories + l.calories + d.calories + s.calories
            total_protein = b.protein + l.protein + d.protein + s.protein
            total_carb = b.carb + l.carb + d.carb + s.carb
            total_fat = b.fat + l.fat + d.fat + s.fat
            total_fiber = b.fiber + l.fiber + d.fiber + s.fiber
            
            # Check hard budget constraint
            if total_cost <= max_budget:
                # Score based on how close calories are to target, and rewarding protein
                cal_diff = abs(total_cal - target_calories)
                
                # Penalty for calorie deviation
                cal_penalty = cal_diff * 1.5
                
                # Reward protein content (each gram of protein adds to the score)
                protein_reward = total_protein * 5.0
                
                # Fiber reward
                fiber_reward = total_fiber * 2.0
                
                score = protein_reward + fiber_reward - cal_penalty
                
                # We want total calories within 20% if budget allows
                cal_deviation_pct = cal_diff / target_calories
                if cal_deviation_pct <= 0.20:
                    score += 200  # Bonus for fitting within calorie range
                    
                if score > best_score:
                    best_score = score
                    best_combination = {
                        "breakfast": b,
                        "lunch": l,
                        "dinner": d,
                        "snack": s,
                        "metrics": {
                            "total_cost": total_cost,
                            "total_calories": total_cal,
                            "total_protein": round(total_protein, 1),
                            "total_fat": round(total_fat, 1),
                            "total_carb": round(total_carb, 1),
                            "total_fiber": round(total_fiber, 1),
                        }
                    }
                    
        # If no combination fits the budget constraint
        if not best_combination:
            logger.warning(f"No meal plan met budget {max_budget} VND. Finding cheapest option...")
            # Relax budget constraint to find cheapest possible healthy menu
            breakfasts_sorted = sorted(breakfasts, key=lambda x: x.price)
            mains_sorted = sorted(main_dishes, key=lambda x: x.price)
            snacks_sorted = sorted(snacks, key=lambda x: x.price)
            
            b = breakfasts_sorted[0]
            l = mains_sorted[0]
            d = mains_sorted[1] if len(mains_sorted) > 1 else mains_sorted[0]
            s = snacks_sorted[0]
            
            total_cost = b.price + l.price + d.price + s.price
            total_cal = b.calories + l.calories + d.calories + s.calories
            total_protein = b.protein + l.protein + d.protein + s.protein
            total_fat = b.fat + l.fat + d.fat + s.fat
            total_carb = b.carb + l.carb + d.carb + s.carb
            total_fiber = b.fiber + l.fiber + d.fiber + s.fiber
            
            return {
                "success": True,
                "warning": f"Ngân sách {max_budget:,.0f}đ quá thấp. Hệ thống đã chọn thực đơn tiết kiệm nhất có thể ({total_cost:,.0f}đ).",
                "menu": [b.to_dict(), l.to_dict(), d.to_dict(), s.to_dict()],
                "breakfast": b.to_dict(),
                "lunch": l.to_dict(),
                "dinner": d.to_dict(),
                "snack": s.to_dict(),
                "metrics": {
                    "total_cost": total_cost,
                    "total_calories": total_cal,
                    "total_protein": round(total_protein, 1),
                    "total_fat": round(total_fat, 1),
                    "total_carb": round(total_carb, 1),
                    "total_fiber": round(total_fiber, 1),
                }
            }
            
        return {
            "success": True,
            "menu": [
                best_combination["breakfast"].to_dict(),
                best_combination["lunch"].to_dict(),
                best_combination["dinner"].to_dict(),
                best_combination["snack"].to_dict()
            ],
            "breakfast": best_combination["breakfast"].to_dict(),
            "lunch": best_combination["lunch"].to_dict(),
            "dinner": best_combination["dinner"].to_dict(),
            "snack": best_combination["snack"].to_dict(),
            "metrics": best_combination["metrics"]
        }
        
    except Exception as e:
        logger.error(f"Error in recommend_menu: {str(e)}")
        return {
            "success": False,
            "error": f"Lỗi hệ thống đề xuất: {str(e)}",
            "menu": []
        }
