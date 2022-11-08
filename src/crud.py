from sqlalchemy.orm import Session
from src import models, schemas

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name,
                                recieve_date=product.recieve_date,
                                bough_price=product.bough_price,
                                quantity=product.quantity)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product_by_id(db: Session, product_id:int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_name(db: Session, name:str):
    return db.query(models.Product).filter(models.Product.name == name).first()

def create_providerr(db:Session, provider:schemas.ProviderCreate):
    db_provider = models.Provider(name=provider.name,
                                  address=provider.address,
                                  phone=provider.phone,
                                  contactee=provider.contactee)
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider

def get_provder(db: Session, product_id:int):
    return db.query(models.Provider).filter(models.Provider.id == product_id).first()

def get_provider_by_name(db: Session, name:str):
    return db.query(models.Provider).filter(models.Provider.name == name).first()

def get_provider_by_phone(db: Session, phone:str):
    return db.query(models.Provider).filter(models.Provider.phone == phone).first()

def get_provider_by_mail(db: Session, address:str):
    return db.query(models.Provider).filter(models.Provider.address == address).first()

def get_provider_by_contactee(db: Session, contactee:str):
    return db.query(models.Provider).filter(models.Provider.contactee == contactee).first()

def create_sale(db: Session, sale: schemas.SaleCreate, product_id:int):
    db_sale = models.Sale(sale_date=sale.sale_date,
                          sale_quantity=sale.sale_quantity,
                          retail_price=sale.retail_price,
                          product_code=product_id)
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_sale_by_product_code(db: Session, product_code: int):
    return db.query(models.Sale).filter(models.Sale.product_code == models.Product.id).filter(models.Product.id == product_code).all()