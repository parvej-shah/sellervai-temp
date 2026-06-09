"""add_google_id_to_users

Revision ID: 05c8b29ad6bf
Revises: 6289d864192c
Create Date: 2026-06-09 22:20:36.320542

Changes:
  - users.google_id  — new nullable unique column (Google OAuth sub)
  - users.hashed_password — allow NULL (Google-only accounts have no password)
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '05c8b29ad6bf'
down_revision = '6289d864192c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add google_id column with unique index
    op.add_column('users', sa.Column('google_id', sa.String(length=255), nullable=True))
    op.create_index(op.f('ix_users_google_id'), 'users', ['google_id'], unique=True)

    # Allow hashed_password to be NULL (Google-only accounts have no password)
    op.alter_column('users', 'hashed_password',
                    existing_type=sa.VARCHAR(length=255),
                    nullable=True)


def downgrade() -> None:
    op.alter_column('users', 'hashed_password',
                    existing_type=sa.VARCHAR(length=255),
                    nullable=False)
    op.drop_index(op.f('ix_users_google_id'), table_name='users')
    op.drop_column('users', 'google_id')
