"""add_product_coupon_order_memory_models

Revision ID: ad5ac1984739
Revises: 833641117afe
Create Date: 2026-06-03 17:28:53.787638

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ad5ac1984739'
down_revision = '833641117afe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('coupons',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('store_id', sa.UUID(), nullable=False),
    sa.Column('code', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('discount_amount', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('discount_percent', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('min_order_amount', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('max_uses', sa.Integer(), nullable=True),
    sa.Column('used_count', sa.Integer(), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_coupons_code'), 'coupons', ['code'], unique=False)
    op.create_table('products',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('store_id', sa.UUID(), nullable=False),
    sa.Column('product_code', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('image', sa.String(length=500), nullable=True),
    sa.Column('available_count', sa.Integer(), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('discount', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_product_code'), 'products', ['product_code'], unique=False)
    op.create_table('conversation_memory',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('conversation_id', sa.UUID(), nullable=False),
    sa.Column('memory', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('conversation_id')
    )
    op.create_table('orders',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('store_id', sa.UUID(), nullable=False),
    sa.Column('order_number', sa.String(length=50), nullable=False),
    sa.Column('customer_name', sa.String(length=255), nullable=False),
    sa.Column('customer_phone', sa.String(length=20), nullable=False),
    sa.Column('customer_phone_2', sa.String(length=20), nullable=True),
    sa.Column('delivery_address', sa.Text(), nullable=False),
    sa.Column('product_code', sa.String(length=100), nullable=False),
    sa.Column('product_name', sa.String(length=255), nullable=False),
    sa.Column('product_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('coupon_code', sa.String(length=100), nullable=True),
    sa.Column('discount_applied', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('total_amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('extra_info', sa.JSON(), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'CONFIRMED', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED', name='orderstatus'), nullable=False),
    sa.Column('platform', sa.String(length=50), nullable=True),
    sa.Column('sender_id', sa.String(length=255), nullable=True),
    sa.Column('conversation_id', sa.UUID(), nullable=True),
    sa.Column('order_date', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_number')
    )
    op.drop_table('langchain_pg_embedding')
    op.drop_table('langchain_pg_collection')
    op.add_column('stores', sa.Column('orders_enabled', sa.Boolean(), nullable=False, server_default=sa.true()))

    # Create the enum type first
    op.execute("CREATE TYPE responselanguage AS ENUM ('ADAPTIVE', 'BANGLA', 'ENGLISH')")

    op.execute("UPDATE stores SET language = 'ENGLISH' WHERE language IS NULL OR language NOT IN ('ADAPTIVE', 'BANGLA', 'ENGLISH')")
    op.execute("ALTER TABLE stores ALTER COLUMN language TYPE responselanguage USING language::responselanguage")
    op.alter_column('stores', 'language', nullable=False)
    op.drop_column('stores', 'products_items')


def downgrade() -> None:
    op.add_column('stores', sa.Column('products_items', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False))

    # Convert enum back to varchar first
    op.execute("ALTER TABLE stores ALTER COLUMN language TYPE VARCHAR(50) USING language::text")
    op.alter_column('stores', 'language', nullable=True)

    # Drop the enum type
    op.execute("DROP TYPE IF EXISTS responselanguage")

    op.drop_column('stores', 'orders_enabled')
    op.create_table('langchain_pg_collection',
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('cmetadata', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('uuid', sa.UUID(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('uuid', name='langchain_pg_collection_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('langchain_pg_embedding',
    sa.Column('collection_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('embedding', sa.NullType(), autoincrement=False, nullable=True),
    sa.Column('document', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('cmetadata', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('custom_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('uuid', sa.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['collection_id'], ['langchain_pg_collection.uuid'], name='langchain_pg_embedding_collection_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid', name='langchain_pg_embedding_pkey')
    )
    op.drop_table('orders')
    op.drop_table('conversation_memory')
    op.drop_index(op.f('ix_products_product_code'), table_name='products')
    op.drop_table('products')
    op.drop_index(op.f('ix_coupons_code'), table_name='coupons')
    op.drop_table('coupons')