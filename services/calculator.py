import logging

logger = logging.getLogger(__name__)

def calculate_bmi(weight_kg: float, height_cm: float) -> tuple[float, str]:
    """
    Calculate Body Mass Index (BMI) and return classification.
    Formula: BMI = Weight_kg / (Height_m ^ 2)
    """
    try:
        height_m = height_cm / 100.0
        if height_m <= 0:
            raise ValueError("Height must be greater than 0")
        if weight_kg <= 0:
            raise ValueError("Weight must be greater than 0")
            
        bmi = weight_kg / (height_m ** 2)
        bmi = round(bmi, 2)
        
        if bmi < 18.5:
            classification = "Gầy"
        elif 18.5 <= bmi < 25.0:
            classification = "Bình thường"
        elif 25.0 <= bmi < 30.0:
            classification = "Thừa cân"
        else:
            classification = "Béo phì"
            
        return bmi, classification
    except Exception as e:
        logger.error(f"Error in calculate_bmi: {str(e)}")
        raise

def calculate_bmr(weight_kg: float, height_cm: float, age_years: int, gender: str) -> float:
    """
    Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation.
    Nam: 10*W + 6.25*H - 5*A + 5
    Nữ: 10*W + 6.25*H - 5*A - 161
    """
    try:
        if gender.lower() in ['nam', 'male', 'm']:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age_years + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age_years - 161
        return round(bmr, 2)
    except Exception as e:
        logger.error(f"Error in calculate_bmr: {str(e)}")
        raise

def calculate_tdee(bmr: float, activity_level: str) -> float:
    """
    Calculate Total Daily Energy Expenditure (TDEE).
    Activity levels:
    - 'sedentary' (Ít vận động): 1.2
    - 'lightly_active' (Vận động nhẹ): 1.375
    - 'moderately_active' (Vận động vừa): 1.55
    - 'very_active' (Vận động nhiều): 1.725
    - 'extra_active' (Vận động cực kỳ nhiều): 1.9
    """
    try:
        activity_factors = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725,
            'extra_active': 1.9
        }
        
        factor = activity_factors.get(activity_level.lower(), 1.2)
        tdee = bmr * factor
        return round(tdee, 2)
    except Exception as e:
        logger.error(f"Error in calculate_tdee: {str(e)}")
        raise
