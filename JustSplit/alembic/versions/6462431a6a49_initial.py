"""initial

Revision ID: 6462431a6a49
Revises: 
Create Date: 2023-11-11 18:39:21.998522

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6462431a6a49'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(length=10), nullable=True),
    sa.Column('profile_image', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('dob', sa.String(length=12), nullable=True),
    sa.Column('friends', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('Group', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('current_currency', sa.String(length=50), nullable=True),
    sa.Column('all_currency_used', postgresql.ARRAY(sa.String(length=50)), nullable=True),
    sa.Column('device_ids', postgresql.ARRAY(sa.String(length=256)), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number'),
    sa.UniqueConstraint('user_name')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
