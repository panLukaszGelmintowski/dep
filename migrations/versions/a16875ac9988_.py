"""empty message

Revision ID: a16875ac9988
Revises: 
Create Date: 2022-11-24 07:56:20.441224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a16875ac9988'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('recieve_date', sa.DateTime(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_id'), 'product', ['id'], unique=False)
    op.create_table('provider',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('contactee', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provider_id'), 'provider', ['id'], unique=False)
    op.create_table('sale',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sale_date', sa.DateTime(), nullable=False),
    sa.Column('sale_quantity', sa.Integer(), nullable=False),
    sa.Column('retail_price', sa.Float(), nullable=False),
    sa.Column('product_code', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_code'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sale_id'), 'sale', ['id'], unique=False)
    op.create_table('supplies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.Column('bought_price', sa.Float(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['provider_id'], ['provider.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_supplies_id'), 'supplies', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_supplies_id'), table_name='supplies')
    op.drop_table('supplies')
    op.drop_index(op.f('ix_sale_id'), table_name='sale')
    op.drop_table('sale')
    op.drop_index(op.f('ix_provider_id'), table_name='provider')
    op.drop_table('provider')
    op.drop_index(op.f('ix_product_id'), table_name='product')
    op.drop_table('product')
    # ### end Alembic commands ###
