"""second_commit

Revision ID: 1d8417d80c6e
Revises: 5fb9a179c502
Create Date: 2023-11-11 18:52:49.175858

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1d8417d80c6e'
down_revision = '5fb9a179c502'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friend_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.Column('friendship_status', sa.Boolean(), nullable=True),
    sa.Column('request_status', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('group_name', sa.String(length=50), nullable=False),
    sa.Column('group_image', sa.String(length=256), nullable=True),
    sa.Column('group_description', sa.String(length=256), nullable=True),
    sa.Column('group_members', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('left_group_member', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('group_balance', sa.Float(), nullable=True),
    sa.Column('group_status', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_login',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('device_id', sa.String(length=100), nullable=False),
    sa.Column('device_name', sa.String(length=100), nullable=True),
    sa.Column('logged_in_status', sa.Boolean(), nullable=True),
    sa.Column('login_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('logout_at', sa.DateTime(), nullable=True),
    sa.Column('location', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('expense',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('expense_tag', sa.String(length=30), nullable=False),
    sa.Column('total_amount', sa.Float(), nullable=True),
    sa.Column('expense_currency', sa.String(length=50), nullable=True),
    sa.Column('expense_description', sa.String(length=256), nullable=True),
    sa.Column('expense_image', sa.String(length=256), nullable=True),
    sa.Column('expense_category', sa.String(length=50), nullable=True),
    sa.Column('expense_comment', sa.String(length=256), nullable=True),
    sa.Column('payer', postgresql.ARRAY(postgresql.JSONB(astext_type=sa.Text())), nullable=True),
    sa.Column('payee', postgresql.ARRAY(postgresql.JSONB(astext_type=sa.Text())), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('expense_snapshot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('expense_id', sa.Integer(), nullable=True),
    sa.Column('expense_snapshots', postgresql.ARRAY(postgresql.JSONB(astext_type=sa.Text())), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['expense_id'], ['expense.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('expense_snapshot')
    op.drop_table('expense')
    op.drop_table('user_login')
    op.drop_table('group')
    op.drop_table('friend_request')
    # ### end Alembic commands ###
