from sqlalchemy import Boolean, Table, Column, Float, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    
    def __repr__(self):
        return f"<{type(self).__name__}(id={self.id})>"
    
class Supply(BaseModel):
    __tablename__ = 'supplies'
    
    product_id = Column(ForeignKey('product.id'), nullable=False)
    provider_id = Column(ForeignKey('provider.id'), nullable=False)
    bought_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    product_suplies = relationship('Product', back_populates='supplies_product')
    provider_suplies = relationship('Provider', back_populates='supplies_providers')

    
class Product(BaseModel):
    __tablename__ = 'product'
    
    name = Column(String, nullable=False)
    recieve_date = Column(DateTime, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    sales_products = relationship('Sale', back_populates='products_sales')
    supplies_product = relationship('Supply', back_populates='product_suplies')
    
class Provider(BaseModel):
    __tablename__ = 'provider'
    
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    contactee = Column(String, nullable=False)
    
    supplies_providers = relationship('Supply', back_populates='provider_suplies')
    
class Sale(BaseModel):
    __tablename__ = 'sale'

    sale_date = Column(DateTime, nullable=False)
    sale_quantity = Column(Integer, nullable=False)
    retail_price = Column(Float, nullable=False)
    product_code = Column(Integer, ForeignKey('product.id'), nullable=False)
    
    products_sales = relationship('Product', back_populates='sales_products') 
