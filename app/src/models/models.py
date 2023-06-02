from sqlalchemy import ARRAY, JSON, Boolean, MetaData, Table, Column ,Integer, String, ForeignKey, Float
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from database import Base

metadata = MetaData()


restaurant = Table(
    'restaurant', 
    metadata, 
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('phone_number', String, nullable=True),
    Column('email', String, nullable=False)
    # Column ("registered_at", TIMESTAMP, default=datetime.utcnow),
    # password
)

branch = Table(
    'branch',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('address', String, nullable=True),
    # Column('opening_hours', String, nullable=True),
    # Column('phone_number', String, nullable=True),
    # Column('email', String, nullable=True),
    Column('id_restaurant', Integer, ForeignKey("restaurant.id"))
)

menu = Table(
    'menu',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('category_name', String, nullable=False),
    Column('dish_name', String, nullable=False),
    Column('dish_picture_url', String, nullable=True),
    Column('ingredients', ARRAY(String), nullable=False),
    Column('allergens', ARRAY(String), nullable=False ), 
    # Column('restrictions', list, nullable=True),
    # Column('flavors', String, nullable=True),
    Column('nutritional_values', JSON, nullable=True), 
    Column('size', Float, nullable=True),
    Column('price', Float, nullable=False), 
    Column('currency', String, nullable=False), 
    Column('id_branch', Integer, ForeignKey("branch.id"))
)

user = Table(
    'user', 
    metadata, 
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String, nullable=False),
    Column('email', String, nullable=False),
    # Column('registered_at', TIMESTAMP, default=datetime.datetime.utcnow()),
    Column('hashed_password', String, nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),    
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False , nullable=False),
)

class User(SQLAlchemyBaseUserTable[int], Base):
        id: int = Column('user_id', Integer, primary_key=True)
        user_name: str = Column('user_name', String, nullable=False)
        email: str = Column(String(length=320), unique=True, index=True, nullable=False)
        # registered_at: Column ("registered_at", TIMESTAMP, default=datetime.datetime.utcnow())
        hashed_password: str = Column(String(length=1024), nullable=False)
        is_active: bool = Column(Boolean, default=True, nullable=False)
        is_superuser: bool = Column(Boolean, default=False, nullable=False)
        is_verified: bool = Column(Boolean, default=False , nullable=False)


user_preferences = Table(
    'user_preferences', 
    metadata, 
    Column('user_id', Integer, ForeignKey('user.user_id'), primary_key=True),
    Column('preferred_cuisine', ARRAY(String)),
    Column('preferred_ingredients', ARRAY(String)),
    Column('disliked_ingredients', ARRAY(String)),
    Column('allergens', ARRAY(String)),
    Column('nutritional_preferences', ARRAY(String))
)