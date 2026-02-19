"""empty message

Revision ID: 87b583e30186
Revises: 001_initial_english, bf5ee2336f5d
Create Date: 2026-02-19 11:33:48.647678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87b583e30186'
down_revision = ('001_initial_english', 'bf5ee2336f5d')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
