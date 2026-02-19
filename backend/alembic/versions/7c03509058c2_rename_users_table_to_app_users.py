"""Rename users table to app_users

Revision ID: 7c03509058c2
Revises: 9ac5dc145130
Create Date: 2026-02-19 12:46:55.699845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c03509058c2'
down_revision = '9ac5dc145130'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table('users', 'app_users')


def downgrade() -> None:
    op.rename_table('app_users', 'users')
