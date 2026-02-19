"""Initial migration with English models

Revision ID: 001_initial_english
Revises: 
Create Date: 2026-02-19 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial_english'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create user table
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)

    # Create profile table
    op.create_table('profile',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('goal', sa.String(), nullable=True),
        sa.Column('height', sa.Float(), nullable=True),
        sa.Column('weight', sa.Float(), nullable=True),
        sa.Column('body_fat_percentage', sa.Float(), nullable=True),
        sa.Column('calories_target', sa.Integer(), nullable=True),
        sa.Column('protein_target', sa.Integer(), nullable=True),
        sa.Column('carbs_target', sa.Integer(), nullable=True),
        sa.Column('fat_target', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profile_id'), 'profile', ['id'], unique=False)
    op.create_index(op.f('ix_profile_user_id'), 'profile', ['user_id'], unique=True)

    # Create plan table
    op.create_table('plan',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('active', sa.Boolean(), server_default='true', nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plan_id'), 'plan', ['id'], unique=False)
    op.create_index(op.f('ix_plan_user_id'), 'plan', ['user_id'], unique=False)

    # Create recipe table
    op.create_table('recipe',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('calories', sa.Integer(), nullable=True),
        sa.Column('protein', sa.Integer(), nullable=True),
        sa.Column('carbs', sa.Integer(), nullable=True),
        sa.Column('fat', sa.Integer(), nullable=True),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('recipe_url', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recipe_id'), 'recipe', ['id'], unique=False)
    op.create_index(op.f('ix_recipe_name'), 'recipe', ['name'], unique=False)

    # Create taste table
    op.create_table('taste',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_taste_id'), 'taste', ['id'], unique=False)

    # Create restriction table
    op.create_table('restriction',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_restriction_id'), 'restriction', ['id'], unique=False)

    # Create daily_menu table
    op.create_table('daily_menu',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('day_of_week', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['plan_id'], ['plan.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_daily_menu_id'), 'daily_menu', ['id'], unique=False)
    op.create_index(op.f('ix_daily_menu_plan_id'), 'daily_menu', ['plan_id'], unique=False)

    # Create profile_taste table
    op.create_table('profile_taste',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('profile_id', sa.Integer(), nullable=False),
        sa.Column('taste_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['taste_id'], ['taste.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profile_taste_id'), 'profile_taste', ['id'], unique=False)

    # Create profile_restriction table
    op.create_table('profile_restriction',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('profile_id', sa.Integer(), nullable=False),
        sa.Column('restriction_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['restriction_id'], ['restriction.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profile_restriction_id'), 'profile_restriction', ['id'], unique=False)

    # Create profile_eating_style table
    op.create_table('profile_eating_style',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('profile_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profile_eating_style_id'), 'profile_eating_style', ['id'], unique=False)

    # Create recipe_meal_type table
    op.create_table('recipe_meal_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recipe_meal_type_id'), 'recipe_meal_type', ['id'], unique=False)
    op.create_index(op.f('ix_recipe_meal_type_recipe_id'), 'recipe_meal_type', ['recipe_id'], unique=False)

    # Create recipe_diet_type table
    op.create_table('recipe_diet_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recipe_diet_type_id'), 'recipe_diet_type', ['id'], unique=False)
    op.create_index(op.f('ix_recipe_diet_type_recipe_id'), 'recipe_diet_type', ['recipe_id'], unique=False)

    # Create meal_detail table
    op.create_table('meal_detail',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False),
        sa.Column('daily_menu_id', sa.Integer(), nullable=False),
        sa.Column('schedule', sa.Time(), nullable=True),
        sa.Column('status', sa.String(), server_default='pending', nullable=True),
        sa.Column('meal_type', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['daily_menu_id'], ['daily_menu.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], onupdate='CASCADE', ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meal_detail_daily_menu_id'), 'meal_detail', ['daily_menu_id'], unique=False)
    op.create_index(op.f('ix_meal_detail_id'), 'meal_detail', ['id'], unique=False)
    op.create_index(op.f('ix_meal_detail_recipe_id'), 'meal_detail', ['recipe_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('meal_detail')
    op.drop_table('recipe_diet_type')
    op.drop_table('recipe_meal_type')
    op.drop_table('profile_eating_style')
    op.drop_table('profile_restriction')
    op.drop_table('profile_taste')
    op.drop_table('daily_menu')
    op.drop_table('restriction')
    op.drop_table('taste')
    op.drop_table('recipe')
    op.drop_table('plan')
    op.drop_table('profile')
    op.drop_table('user')
