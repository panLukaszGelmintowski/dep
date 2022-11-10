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
def create_product(product: schemas.ProductCreate, db:Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id=product.id)
    # if db_product:
    #     raise HTTPException(status_code=400, detail='name already exist')
    return crud.create_product(db=db, product=product)

@app.get('/products/{product_id}', response_model=schemas.Product)
def get_product_by_id(product_id:int, db:Session=Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail='product not found')
    return db_product

@app.get('/products/', response_model=list[schemas.Product])
def get_product_by_name(product_name:str, db:Session=Depends(get_db)):
    db_product = crud.get_product_by_name(db, product_name=product_name)
    if db_product is None:
        raise HTTPException(status_code=404, detail='product not found')
    return db_product

@app.post('/provider/', response_model=schemas.Provider)
def create_provider(provider: schemas.ProviderCreate, db:Session = Depends(get_db)):
    db_provider = crud.get_provider_by_name(db, name=provider.name)
    if db_provider:
        raise HTTPException(status_code=400, detail='name already exist')
    
    

