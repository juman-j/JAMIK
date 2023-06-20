from sqlalchemy import Table
from sqlalchemy import ARRAY
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from src.database import Base

metadata = MetaData()


restaurant = Table(
    'restaurant', 
    metadata, 
    Column('restaurant_id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('phone_number', String, nullable=True, unique=True),
    Column('email', String, nullable=False, unique=True)
)

food = Table(
    'food',
    metadata,
    Column('food_id', Integer, autoincrement=True, primary_key=True),
    Column('food_name', JSONB, nullable=False),
    Column('category_name', JSONB, nullable=False),
    Column('dish_picture_url', String, nullable=True),
    Column('ingredients', JSONB, nullable=False),
    Column('diet_restriction', JSONB, nullable=True),
    Column('nutritional_values', JSONB, nullable=True),
    Column('size', JSONB, nullable=False),
    Column('price', Integer, nullable=False),
    Column('currency', String, nullable=False),
    Column('is_active', Boolean, nullable=False),
    Column('restaurant_id', Integer, ForeignKey("restaurant.restaurant_id"))
)

food_allergens = Table(
    'food_allergens',
    metadata,
    Column('food_id', Integer, ForeignKey('food.food_id'), primary_key=True),
    Column('allergen_id', String, ForeignKey('allergen.allergen_id'), primary_key=True)
)

allergen = Table(
    'allergen',
    metadata,
    Column('allergen_id', String, primary_key=True),
    Column('allergen_name', JSONB, nullable=False)
)

user_history = Table(
    'user_history',
    metadata,
    Column('id_user', Integer, ForeignKey("user.id")),
    Column('id_food', Integer, ForeignKey("food.food_id")),
    Column('rating', Integer)
)

user = Table(
    'user', 
    metadata, 
    Column('id', Integer, primary_key=True),
    Column('user_name', String, nullable=False, unique=True),
    Column('email', String, nullable=False, unique=True),
    Column('hashed_password', String, nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),    
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False , nullable=False),
)

class User(SQLAlchemyBaseUserTable[int], Base):
        id: int = Column('id', Integer, primary_key=True)
        user_name: str = Column('user_name', String, nullable=False, unique=True)
        email: str = Column(String(length=320), unique=True, index=True, nullable=False)
        hashed_password: str = Column(String(length=1024), nullable=False)
        is_active: bool = Column(Boolean, default=True, nullable=False)
        is_superuser: bool = Column(Boolean, default=False, nullable=False)
        is_verified: bool = Column(Boolean, default=False , nullable=False)


user_preferences = Table(
    'user_preferences', 
    metadata, 
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('preferred_ingredients', ARRAY(String), nullable=False),
    Column('diet_restriction', ARRAY(String), nullable=True),
    Column('metric_system', String, nullable=False),
    Column('allergens', ARRAY(String), nullable=True)
)