from sqlalchemy import ARRAY, JSON, Boolean, Enum, MetaData, Table, Column ,Integer, String, ForeignKey
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from src.database import Base

metadata = MetaData()


restaurant = Table(
    'restaurant', 
    metadata, 
    Column('restaurant_id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('phone_number', String, nullable=True),
    Column('email', String, nullable=False)
)

food = Table(
    'food',
    metadata,
    Column('food_id', Integer, primary_key=True),
    Column('category_name', JSON, nullable=False),
    Column('food_name', JSON, nullable=False),
    Column('dish_picture_url', String, nullable=True),
    Column('ingredients', JSON, nullable=False),
    Column('allergens', Integer, ForeignKey('allergen.allergen_id')), # is it possible to enter more than one value here?
    Column('size', Integer, nullable=False),
    Column('price', Integer, nullable=False),
    Column('currency', Enum('USD', 'EUR', 'CZK', name='currency_enum'), nullable=False),
    Column('restaurant_id', Integer, ForeignKey("restaurant.restaurant_id"))
)

allergen = Table(
    'allergen',
    metadata,
    Column('allergen_id', Integer, primary_key=True),
    Column('allergen_name', JSON, nullable=False)
)

user_history = Table(
    'user_history',
    metadata,
    Column('id_user', Integer, ForeignKey("user.id")),
    Column('id_food', Integer, ForeignKey("food.food_id")),
    Column('rating', Enum('good', 'not good',  name='rating_enum'))
)

user = Table(
    'user', 
    metadata, 
    Column('id', Integer, primary_key=True),
    Column('user_name', String, nullable=False),
    Column('email', String, nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),    
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False , nullable=False),
)

class User(SQLAlchemyBaseUserTable[int], Base):
        id: int = Column('id', Integer, primary_key=True)
        user_name: str = Column('user_name', String, nullable=False)
        email: str = Column(String(length=320), unique=True, index=True, nullable=False)
        hashed_password: str = Column(String(length=1024), nullable=False)
        is_active: bool = Column(Boolean, default=True, nullable=False)
        is_superuser: bool = Column(Boolean, default=False, nullable=False)
        is_verified: bool = Column(Boolean, default=False , nullable=False)


user_preferences = Table(
    'user_preferences', 
    metadata, 
    Column('id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('preferred_ingredients', Enum('tomato', 'beef', name = 'ingredients_enum')), # Enum?
    Column('allergens', ARRAY(String)) # Enum?
)