from app import db, login_manager
from datetime import datetime 
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pic = db.Column(db.String(100), nullable=False, default='default.jpg')  # profile pic
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  

    # rest of your columns here

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_pic}')"
    
class Product(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)  # Store image file path
    stock = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Product {self.name}>'


reviews = db.relationship('Review', back_populates='product', cascade='all, delete-orphan')

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # if you have users
    rating = db.Column(db.Integer, nullable=False)  
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

