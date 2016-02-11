"""init_models

Revision ID: 4dd5bdfa430
Revises: None
Create Date: 2016-02-11 13:15:36.919774

"""

revision = '4dd5bdfa430'
down_revision = None

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import coaster


def upgrade():
    op.create_table('organization',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('userid', sa.Unicode(length=22), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=250), nullable=False),
    sa.Column('title', sa.Unicode(length=250), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('userid')
    )
    op.create_table('user',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('lastuser_token_scope', sa.Unicode(length=250), nullable=True),
    sa.Column('lastuser_token_type', sa.Unicode(length=250), nullable=True),
    sa.Column('userinfo', coaster.sqlalchemy.JsonDict(), nullable=True),
    sa.Column('email', sa.Unicode(length=80), nullable=True),
    sa.Column('lastuser_token', sa.String(length=22), nullable=True),
    sa.Column('username', sa.Unicode(length=80), nullable=True),
    sa.Column('userid', sa.String(length=22), nullable=False),
    sa.Column('fullname', sa.Unicode(length=80), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('lastuser_token'),
    sa.UniqueConstraint('userid'),
    sa.UniqueConstraint('username')
    )
    op.create_table('inventory',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('description', sa.Unicode(length=2500), nullable=True),
    sa.Column('organization_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=250), nullable=False),
    sa.Column('title', sa.Unicode(length=250), nullable=False),
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('organization_id', 'name')
    )
    op.create_table('category',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('inventory_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.Column('name', sa.Unicode(length=250), nullable=False),
    sa.Column('title', sa.Unicode(length=250), nullable=False),
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventory.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('inventory_id', 'name')
    )
    op.create_table('discount_policy',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('inventory_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.Column('discount_type', sa.Integer(), nullable=False),
    sa.Column('item_quantity_min', sa.Integer(), nullable=False),
    sa.Column('item_quantity_max', sa.Integer(), nullable=True),
    sa.Column('percentage', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=250), nullable=False),
    sa.Column('title', sa.Unicode(length=250), nullable=False),
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.CheckConstraint(u'percentage <= 100', name='percentage_bound_upper'),
    sa.CheckConstraint(u'percentage > 0', name='percentage_bound_lower'),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventory.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('inventory_id', 'name')
    )
    op.create_table('order',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('inventory_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('invoiced_at', sa.DateTime(), nullable=True),
    sa.Column('order_hash', sa.Unicode(length=120), nullable=True),
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventory.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('discount_coupon',
    sa.Column('code', sa.Unicode(length=6), nullable=False),
    sa.Column('discount_policy_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.Column('quantity_available', sa.Integer(), nullable=False),
    sa.Column('quantity_total', sa.Integer(), nullable=False),
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.CheckConstraint(u'quantity_available <= quantity_total', name='quantity_bound'),
    sa.ForeignKeyConstraint(['discount_policy_id'], ['discount_policy.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code', 'discount_policy_id')
    )
    op.create_table('item',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('description', sa.Unicode(length=2500), nullable=False),
    sa.Column('inventory_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.Column('category_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.Column('quantity_available', sa.Integer(), nullable=False),
    sa.Column('quantity_total', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=250), nullable=False),
    sa.Column('title', sa.Unicode(length=250), nullable=False),
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.CheckConstraint(u'quantity_available <= quantity_total', name='quantity_bound'),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventory.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('inventory_id', 'name')
    )
    op.create_table('payment',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('order_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
    sa.Column('pg_payment_id', sa.Unicode(length=80), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_discount_policy',
    sa.Column('item_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.Column('discount_policy_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['discount_policy_id'], ['discount_policy.id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
    sa.PrimaryKeyConstraint('item_id', 'discount_policy_id')
    )
    op.create_table('line_item',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('order_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
    sa.Column('item_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('base_amount', sa.Numeric(), nullable=False),
    sa.Column('discounted_amount', sa.Numeric(), nullable=False),
    sa.Column('final_amount', sa.Numeric(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('price',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('item_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.Column('valid_from', sa.DateTime(), nullable=False),
    sa.Column('valid_upto', sa.DateTime(), nullable=False),
    sa.Column('amount', sa.Numeric(), nullable=False),
    sa.Column('currency', sa.Unicode(length=3), nullable=False),
    sa.Column('name', sa.Unicode(length=250), nullable=False),
    sa.Column('title', sa.Unicode(length=250), nullable=False),
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.CheckConstraint(u'valid_from < valid_upto', name='valid_bound'),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('item_id', 'name')
    )
    op.create_table('transaction',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('order_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
    sa.Column('payment_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
    sa.Column('amount', sa.Numeric(), nullable=False),
    sa.Column('currency', sa.Unicode(length=3), nullable=False),
    sa.Column('transaction_type', sa.Integer(), nullable=False),
    sa.Column('transaction_method', sa.Integer(), nullable=False),
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['payment_id'], ['payment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('transaction')
    op.drop_table('price')
    op.drop_table('line_item')
    op.drop_table('item_discount_policy')
    op.drop_table('payment')
    op.drop_table('item')
    op.drop_table('discount_coupon')
    op.drop_table('order')
    op.drop_table('discount_policy')
    op.drop_table('category')
    op.drop_table('inventory')
    op.drop_table('user')
    op.drop_table('organization')
    ### end Alembic commands ###