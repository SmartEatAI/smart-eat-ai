"""DEPRECATED - Use new English migrations

Revision ID: bf5ee2336f5d
Revises: 382ed2ed6d7f
Create Date: 2026-02-19 10:05:48.825667

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bf5ee2336f5d'
down_revision = '382ed2ed6d7f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # This migration is deprecated - Spanish table names
    pass


def downgrade() -> None:
    # This migration is deprecated
    pass
