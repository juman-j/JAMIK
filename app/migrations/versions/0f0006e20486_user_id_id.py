"""user_id -> id

Revision ID: 0f0006e20486
Revises: 
Create Date: 2023-06-07 21:02:19.379995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f0006e20486'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('allergen',
    sa.Column('allergen_id', sa.Integer(), nullable=False),
    sa.Column('allergen_name', sa.JSON(), nullable=False),
    sa.PrimaryKeyConstraint('allergen_id')
    )
    op.create_table('restaurant',
    sa.Column('restaurant_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('restaurant_id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('food',
    sa.Column('food_id', sa.Integer(), nullable=False),
    sa.Column('category_name', sa.JSON(), nullable=False),
    sa.Column('food_name', sa.JSON(), nullable=False),
    sa.Column('dish_picture_url', sa.String(), nullable=True),
    sa.Column('ingredients', sa.JSON(), nullable=False),
    sa.Column('allergens', sa.Integer(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('currency', sa.Enum('USD', 'EUR', 'CZK', name='currency_enum'), nullable=False),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['allergens'], ['allergen.allergen_id'], ),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.restaurant_id'], ),
    sa.PrimaryKeyConstraint('food_id')
    )
    op.create_table('user_preferences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('preferred_ingredients', sa.Enum('tomato', 'beef', name='ingredients_enum'), nullable=True),
    sa.Column('allergens', sa.ARRAY(sa.String()), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_history',
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.Column('id_food', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Enum('good', 'not good', name='rating_enum'), nullable=True),
    sa.ForeignKeyConstraint(['id_food'], ['food.food_id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_history')
    op.drop_table('user_preferences')
    op.drop_table('food')
    op.drop_table('user')
    op.drop_table('restaurant')
    op.drop_table('allergen')
    # ### end Alembic commands ###
