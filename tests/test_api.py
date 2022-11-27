from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from src.main import app, get_db
from src.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Тестовая БД

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


def test_create_product():
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

def test_update_product_price():
    """
    Тест на обновление цены продукта
    """
    response = client.put(
        '/products/',
        json={"name": "test_prod", 
              "recieve_date": "2020-10-05T18:00:00",
              'price': 20000,
              'quantity':20,
              'id':1
            }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)
    assert data["price"] == 20000

def test_get_product_by_id():
    """
    Тест получения продукта по id
    """
    response = client.get('/products/1')
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['name'] == 'test_prod'

def test_create_provider():
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
    
def test_create_sale():
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
    
def test_get_sale_by_product_code():
    response = client.get('/sale/products/1')
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
    
def test_create_supply():
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
    
def test_get_supply():
    response = client.get('/supply/via_1')
    assert response.status_code == 200, response.text
    data = response.json()
    assert type(data)==list