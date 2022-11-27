"""empty message

Revision ID: a_data
Revises: a16875ac9988
Create Date: 2022-11-24 07:56:30.441224

"""
from alembic import op
from sqlalchemy.orm import Session
from datetime import datetime

from src.models import Product, Provider, Sale, Supply


# revision identifiers, used by Alembic.
revision = 'a_data'
down_revision = 'a16875ac9988'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)
    
    prod_a = Product(name='printer',
                     recieve_date=datetime(2020, 10, 5, 18, 00),
                     price=10000.00,
                     quantity=40)
    prod_b = Product(name='disk',
                     recieve_date=datetime(2020, 10, 5, 18, 1),
                     price=5600.00,
                     quantity=20)
    
    session.add_all([prod_a,prod_b])
    session.flush()
    
    prov_a = Provider(name='mihal palych',
                      address='lenina 73',
                      phone = '88005553535',
                      contactee='mihal palych')

    prov_b = Provider(name='terentyev',
                      address='pushkina 228',
                      phone = '88005553535',
                      contactee='terentyev')
    
    session.add_all([prov_a, prov_b])
    session.flush()
    
    sale_a = Sale(sale_date=datetime(2020, 10, 6, 10, 25),
                  sale_quantity=1,
                  retail_price=12500.00,
                  product_code = prod_a.id)
    
    sale_b = Sale(sale_date=datetime(2020, 10, 6, 11, 40),
                sale_quantity=1,
                retail_price=12500.00,
                product_code = prod_a.id)
    
    sale_c = Sale(sale_date=datetime(2020, 10, 6, 11, 57),
                sale_quantity=2,
                retail_price=6000.00,
                product_code = prod_b.id)
    
    session.add_all([sale_a, sale_b, sale_c])
    session.flush()
    
    supl_a = Supply(product_id=prod_a.id,
                    provider_id=prov_a.id,
                    bought_price=10000,
                    quantity=40)
    supl_b = Supply(product_id=prod_b.id,
                    provider_id=prov_b.id,
                    bought_price=5600,
                    quantity=20)
    
    session.add_all([supl_a, supl_b,])
    session.commit()
    
def downgrade() -> None:
    pass
