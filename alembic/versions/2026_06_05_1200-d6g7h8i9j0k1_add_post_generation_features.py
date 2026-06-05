"""add_post_generation_features

Revision ID: d6g7h8i9j0k1
Revises: c5f6e7a8b9c0
Create Date: 2026-06-05 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd6g7h8i9j0k1'
down_revision = 'c5f6e7a8b9c0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enums
    op.execute("CREATE TYPE posttype AS ENUM ('product', 'meme', 'quote')")
    op.execute("CREATE TYPE postsource AS ENUM ('webhook', 'generated')")
    
    # Add new columns to page_posts
    op.add_column('page_posts', sa.Column('platform', sa.String(length=50), nullable=False, server_default='facebook'))
    op.add_column('page_posts', sa.Column('post_type', sa.Enum('product', 'meme', 'quote', name='posttype'), nullable=False, server_default='product'))
    op.add_column('page_posts', sa.Column('post_source', sa.Enum('webhook', 'generated', name='postsource'), nullable=False, server_default='webhook'))
    op.add_column('page_posts', sa.Column('product_id', sa.UUID(), nullable=True))
    
    # Remove server defaults after they're set
    op.alter_column('page_posts', 'platform', server_default=None)
    op.alter_column('page_posts', 'post_type', server_default=None)
    op.alter_column('page_posts', 'post_source', server_default=None)


def downgrade() -> None:
    op.drop_column('page_posts', 'product_id')
    op.drop_column('page_posts', 'post_source')
    op.drop_column('page_posts', 'post_type')
    op.drop_column('page_posts', 'platform')
    op.execute("DROP TYPE postsource")
    op.execute("DROP TYPE posttype")
