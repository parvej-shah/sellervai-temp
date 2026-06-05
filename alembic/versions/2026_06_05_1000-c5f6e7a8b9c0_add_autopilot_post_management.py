"""add_autopilot_post_management

Revision ID: c5f6e7a8b9c0
Revises: ad5ac1984739
Create Date: 2026-06-05 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c5f6e7a8b9c0'
down_revision = 'ad5ac1984739'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add autopilot_enabled column to stores
    op.add_column('stores', sa.Column('autopilot_enabled', sa.Boolean(), nullable=False, server_default=sa.false()))

    # Create page_posts table
    op.create_table('page_posts',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('store_id', sa.UUID(), nullable=False),
        sa.Column('page_id', sa.String(length=255), nullable=False),
        sa.Column('post_id', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('image_url', sa.String(length=500), nullable=True),
        sa.Column('image_text', sa.Text(), nullable=True),
        sa.Column('knowledge', sa.Text(), nullable=True),
        sa.Column('knowledge_updated', sa.Boolean(), nullable=False),
        sa.Column('autopilot_paused', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('post_id')
    )
    op.create_index(op.f('ix_page_posts_post_id'), 'page_posts', ['post_id'], unique=False)

    # Create post_comments table
    op.create_table('post_comments',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('post_id', sa.String(length=255), nullable=False),
        sa.Column('store_id', sa.UUID(), nullable=False),
        sa.Column('comment_id', sa.String(length=255), nullable=False),
        sa.Column('sender_id', sa.String(length=255), nullable=False),
        sa.Column('sender_name', sa.String(length=255), nullable=True),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('replied', sa.Boolean(), nullable=False),
        sa.Column('reply_text', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['page_posts.post_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('comment_id')
    )
    op.create_index(op.f('ix_post_comments_comment_id'), 'post_comments', ['comment_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_post_comments_comment_id'), table_name='post_comments')
    op.drop_table('post_comments')
    op.drop_index(op.f('ix_page_posts_post_id'), table_name='page_posts')
    op.drop_table('page_posts')
    op.drop_column('stores', 'autopilot_enabled')
