from datetime import datetime
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    recieve_date: datetime
    price: float
    quantity: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    # sales_products: int
    # supplies_product: list[Supply] = []
    
    class Config:
        orm_mode = True

class ProviderBase(BaseModel):
    name: str
    address: str
    phone: str
    contactee: str

class ProviderCreate(ProviderBase):

    pass

class Provider(ProviderBase):
    id: int
    # supplies_providers: list[Supply] = []
    
    class Config:
        orm_mode = True

class SupplyBase(BaseModel):
    product_id: int
    provider_id: int
    bought_price: float
    quantity: int


class SupplyCreate(SupplyBase):
    pass

class Supply(SupplyBase):
    id: int
    class Config:
        orm_mode = True
        
class SaleBase(BaseModel):
    sale_date: datetime
    sale_quantity: int
    retail_price: float
    product_code: int

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    # products_sales: list[Product] = []

    class Config:
        orm_mode = True

