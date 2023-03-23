from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy import CheckConstraint


from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    pizzas = relationship('Pizza', secondary='restaurant_pizzas', back_populates='restaurants')
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'created_at': self.created_at,
        }

class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    toppings = Column(String(255), nullable=True)  
    ingredients = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    restaurants = relationship('Restaurant', secondary='restaurant_pizzas', back_populates='pizzas')




class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    pizza_id = Column(Integer, ForeignKey('pizzas.id'), nullable=False)
    price = Column(Float, nullable=False)

    __table_args__ = (
        CheckConstraint('price >= 1 AND price <= 30', name='price_check'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'pizza_id': self.pizza_id,
            'price': self.price,
        }
