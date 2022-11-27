from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependecy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/products/', response_model=schemas.Product)
def create_product(product: schemas.Product, db:Session = Depends(get_db)):
    db_product = crud.get_product_by_name(db, product_name=product.name)
    if db_product:
        raise HTTPException(status_code=400, detail='product already exist')
    return crud.create_product(db=db, product=product)

@app.put('/products/', response_model=schemas.Product)
def update_product_price(product: schemas.Product, new_price: float, db:Session=Depends(get_db)):
    db_product = crud.get_product_by_id(db=db, product_id=product.id)
    if db_product is None:
        raise HTTPException(status_code=404, detail='product not found')
    return crud.update_product_price(db=db,product=product,new_price=new_price)
        
@app.get('/products/{product_id}', response_model=schemas.Product)
def get_product_by_id(product_id:int, db:Session=Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail='product not found')
    return db_product

@app.get('/products/', response_model=schemas.Product)
def get_product_by_name(product_name:str, db:Session=Depends(get_db)):
    db_product = crud.get_product_by_name(db, product_name=product_name)
    if db_product is None:
        raise HTTPException(status_code=404, detail='product not found')
    return db_product

@app.post('/provider/', response_model=schemas.Provider)
def create_provider(provider: schemas.ProviderCreate, db:Session = Depends(get_db)):
    db_provider = crud.get_provider_by_name(db, name=provider.name)
    if db_provider:
        raise HTTPException(status_code=400, detail='provider already exist')
    return crud.create_provider(db=db, provider=provider)
    
@app.post('/sale/', response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate,  db:Session=Depends(get_db)):
    db_sale = crud.create_sale(db=db, sale=sale)
    print(db_sale)
    if db_sale.id is None:
        raise HTTPException(status_code=422, detail='there is not enough product')
    return db_sale

@app.get('/sale/products/{product_code}', response_model=list[schemas.Sale])
def get_sale_by_product_code(product_code:int, db:Session=Depends(get_db)):
    db_sale = crud.get_sale_by_product_code(db=db, product_code=product_code)
    db_product = get_product_by_id(db=db, product_id=product_code)
    if db_sale is None:
        raise HTTPException(status_code=404, detail='sales not found')
    if db_product is None:
        raise HTTPException(status_code=404, detail='teee')
    return db_sale

@app.post('/supply/',response_model=schemas.Supply)
def create_supply(supply: schemas.SupplyCreate, db:Session=Depends(get_db)):
    db_supply = crud.create_supply(supply=supply, db=db) 
    if db_supply.id is None:
        raise HTTPException(status_code=422, detail='there is not enough product')
    return db_supply
   
@app.get('/supply/via_{provider_id}', response_model=list[schemas.Supply])
def get_supply_by_provider(provider_id:int, db:Session=Depends(get_db)):
    db_supply = get_supply_by_provider(provider_id=provider_id, db=db)
    if db_supply is None:
        raise HTTPException(status_code=404, detail='supply not found')    
    return db_supply