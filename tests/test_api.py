from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from src.main import app, get_db
from src.models import Base
from os import environ

SQLALCHEMY_DATABASE_URL = environ.get('DATABASE_URL')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)  # Удалем таблицы из БД
Base.metadata.create_all(bind=engine)  # Создаем таблицы в БД


def override_get_db():
    """
    Данная функция при тестах будет подменять функцию get_db() в main.py.
    Таким образом приложение будет подключаться к тестовой базе данных.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db  # Делаем подмену

client = TestClient(app)  # создаем тестовый клиент к нашему приложению


def test_create_product_1():
    """
    Тест на создание нового продукта
    """
    response = client.post(
        "/products/",
        json={"name": "test_prod", 
              "recieve_date": "2020-10-05T18:00:00",
              'price': 10000,
              'quantity':20,
              'id':1
            }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "test_prod"

def test_create_product_2():
    """
    Тест на создание нового продукта
    """
    response = client.post(
        "/products/",
        json={"name": "test_prod", 
              "recieve_date": "2020-10-05T18:00:00",
              'price': 10000,
              'quantity':20,
              'id':2
            }
    )
    assert response.status_code == 400, response.text
    assert response.text == '{"detail":"product already exist"}'

def test_get_product_by_id_1():
    """
    Тест получения продукта по id
    """
    response = client.get('/products/1')
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['name'] == 'test_prod'

def test_get_product_by_id_2():
    """
    Тест получения продукта по id
    """
    response = client.get('/products/2')
    assert response.status_code == 404, response.text
    assert response.text == '{"detail":"product not found"}'

def test_create_provider_1():
    """
    Тест на создание нового поставщика
    """
    response = client.post(
        '/provider/',
        json={
            'name':'test_name',
            'address':'ulitsa',
            'phone':'88005553535',
            'contactee':'test_name',
            'id':1
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "test_name"
    
def test_create_provider_2():
    """
    Тест на создание нового поставщика
    """
    response = client.post(
        '/provider/',
        json={
            'name':'test_name',
            'address':'ulitsa',
            'phone':'88005553535',
            'contactee':'test_name',
            'id':2
        }
    )
    assert response.status_code == 400, response.text
    assert response.text == '{"detail":"provider already exist"}'
    
def test_create_sale_1():
    response = client.post(
        '/sale/',
        json={
            'sale_date':"2020-10-05T18:00:00",
            'sale_quantity':10,
            'retail_price':222,
            'product_code':1,
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["sale_quantity"] == 10
    
def test_create_sale_2():
    response = client.post(
        '/sale/',
        json={
            'sale_date':"2020-10-05T18:00:00",
            'sale_quantity':1000,
            'retail_price':222,
            'product_code':1,
        }
    )
    assert response.status_code == 422, response.text
    assert response.text == '{"detail":"there is not enough product"}'
    
def test_get_sale_by_product_code_1():
    response = client.get('/sale/product/1')
    assert response.status_code == 200, response.text
    data = response.json()
    assert type(data) == list
    assert data[0] == {
            'sale_date':"2020-10-05T18:00:00",
            'sale_quantity':10,
            'retail_price':222,
            'product_code':1,
            'id':1
        }
    
def test_get_sale_by_product_code_2():
    response = client.get('/sale/product/222')
    assert response.status_code == 404, response.text
    assert response.text == '{"detail":"product not found"}'
    
def test_create_supply_1():
    response = client.post(
        '/supply/',
        json={
            'product_id': 1,
            'provider_id': 1,
            'bought_price': 200.0,
            'quantity': 2,
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["quantity"] == 2
    
def test_create_supply_2():
    response = client.post(
        '/supply/',
        json={
            'product_id': 1,
            'provider_id': 12234,
            'bought_price': 200.0,
            'quantity': 2,
        }
    )
    assert response.status_code == 400, response.text
    assert response.status_code == 400, response.text
    assert response.text == '{"detail":"provider doesnt exist"}'
 
def test_create_supply_3():
    response = client.post(
        '/supply/',
        json={
            'product_id': 12222,
            'provider_id': 1,
            'bought_price': 200.0,
            'quantity': 2,
        }
    )
    assert response.status_code == 400, response.text
    assert response.text == '{"detail":"product doesnt exist"}'
 
    
def test_get_supply_1():
    response = client.get('/supply/via_1')
    assert response.status_code == 200, response.text
    data = response.json()
    assert type(data)==list
    
def test_get_supply_2():
    response = client.get('/supply/via_5')
    assert response.status_code == 404, response.text
    assert response.text == '{"detail":"provider doesnt exist"}'