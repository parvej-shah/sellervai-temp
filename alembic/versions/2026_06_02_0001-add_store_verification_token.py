"""add store verification token

Revision ID: 2026_06_02_0001
Revises: 2d2d941f6b2b
Create Date: 2026-06-02 00:01:00.000000

"""
from alembic import op
import sqlalchemy as sa
import secrets


# revision identifiers, used by Alembic.
revision = '2026_06_02_0001'
down_revision = '2d2d941f6b2b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('stores', sa.Column('verification_token', sa.String(length=255), nullable=True))

    connection = op.get_bind()
    store_rows = connection.execute(sa.text("SELECT id FROM stores WHERE verification_token IS NULL")).fetchall()
    for row in store_rows:
        connection.execute(
            sa.text("UPDATE stores SET verification_token = :token WHERE id = :store_id"),
            {"token": secrets.token_urlsafe(32), "store_id": row.id},
        )

    op.alter_column('stores', 'verification_token', nullable=False)
    op.create_index(op.f('ix_stores_verification_token'), 'stores', ['verification_token'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_stores_verification_token'), table_name='stores')
    op.drop_column('stores', 'verification_token')