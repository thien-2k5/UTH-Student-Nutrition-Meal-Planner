from app.database import db

class Food(db.Model):
    """Food item database model."""
    __tablename__ = 'foods'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)  # VND (Vietnamese Dong)
    protein = db.Column(db.Float, nullable=False)  # grams
    fat = db.Column(db.Float, nullable=False)  # grams
    carb = db.Column(db.Float, nullable=False)  # grams
    fiber = db.Column(db.Float, nullable=False)  # grams
    vitamin = db.Column(db.String(250), nullable=False)  # Comma-separated vitamins
    calories = db.Column(db.Float, nullable=False)  # kcal
    category = db.Column(db.String(50), nullable=False)  # "Sáng", "Trưa/Tối", "Ăn vặt", "Nước uống"
    
    def to_dict(self):
        """Convert model object to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'protein': self.protein,
            'fat': self.fat,
            'carb': self.carb,
            'fiber': self.fiber,
            'vitamin': self.vitamin,
            'calories': self.calories,
            'category': self.category
        }
        
    def __repr__(self):
        return f"<Food {self.name} ({self.category}) - {self.price} VND>"
