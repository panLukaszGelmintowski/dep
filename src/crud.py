from sqlalchemy.orm import Session
from src import models, schemas

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name,
                                recieve_date=product.recieve_date,
                                price=product.price,
                                quantity=product.quantity)
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product_price(db:Session, product: schemas.Product, new_price:float):# pragma: no cover
    db_product = get_product_by_id(db=db, product_id=product.id)
    db_product.price = new_price
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product_amount(db:Session, product_id:int, product_amount:float):
    db_product = get_product_by_id(db=db, product_id=product_id)
    if db_product:
        db_product.quantity += product_amount
        if db_product.quantity >= 0:
            db.commit()
    return db_product

def get_product_by_id(db: Session, product_id:int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_name(db: Session, product_name:str):
    return db.query(models.Product).filter(models.Product.name == product_name).first()

def create_provider(db:Session, provider:schemas.ProviderCreate):
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

def create_sale(db: Session, sale: schemas.SaleCreate):
    db_sale = models.Sale(sale_date=sale.sale_date,
                          sale_quantity=sale.sale_quantity,
                          retail_price=sale.retail_price,
                          product_code=sale.product_code)
    db_product = get_product_by_id(db=db, product_id=sale.product_code)
    if sale.sale_quantity <= db_product.quantity:
        update_product_amount(db=db, 
                              product_id=sale.product_code,
                              product_amount=-sale.sale_quantity)
        db.add(db_sale)
        db.commit()
        db.refresh(db_sale)
    return db_sale

def get_sale_by_product_code(db: Session, product_code: int):
    return db.query(models.Sale).filter(models.Sale.product_code == models.Product.id).filter(models.Product.id == product_code).all()

def create_supply(db:Session, supply:schemas.SupplyCreate):
    db_supply = models.Supply(product_id=supply.product_id,
                              provider_id=supply.provider_id,
                              bought_price=supply.bought_price,
                              quantity=supply.quantity)
    update_product_amount(db=db, 
                          product_id=supply.product_id,
                          product_amount=+supply.quantity)
    db.add(db_supply)
    db.commit()
    db.refresh(db_supply)
    return db_supply

def get_supply_by_provider(db:Session, provider_id:int):
    return db.query(models.Supply).filter(models.Supply.provider_id == provider_id).all()
