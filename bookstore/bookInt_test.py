import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app  
from database import get_db, Book  

# Create a test client for FastAPI
client = TestClient(app)

# Mock data
mock_book = Book(id=1, name="Test Book", author="Test Author", published_year=2023, book_summary="Test Summary")
mock_books = [mock_book]

# Mock JWTBearer dependency
@pytest.fixture
def mock_jwt_bearer():
    with patch("middleware.JWTBearer.__call__", return_value=True):
        yield

# Mock database session
@pytest.fixture
def mock_db_session():
   
    mock_session = MagicMock(spec=Session)
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.side_effect = lambda x: x  # Mock refresh to return the object itself
    with patch("database.get_db", return_value=mock_session):
        yield mock_session

# Mock database queries
@pytest.fixture
def mock_db_query():
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_book
    mock_query.all.return_value = mock_books
    return mock_query

# Test create_book endpoint
@pytest.mark.asyncio
async def test_create_book(mock_jwt_bearer, mock_db_session, mock_db_query):
    response = client.post("/books/", json=mock_book.dict())
    assert response.status_code == 200
    assert response.json() == mock_book.dict()

# Test update_book endpoint
@pytest.mark.asyncio
async def test_update_book(mock_jwt_bearer, mock_db_session, mock_db_query):
    update_data = {"name": "Updated Book"}
    response = client.put("/books/1", json=update_data)
    assert response.status_code == 200
    updated_book = mock_book.dict()
    updated_book.update(update_data)
    assert response.json() == updated_book

# Test delete_book endpoint
@pytest.mark.asyncio
async def test_delete_book(mock_jwt_bearer, mock_db_session, mock_db_query):
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Book deleted successfully"}

# Test get_book endpoint after creating it
@pytest.mark.asyncio
async def test_create_and_get_book(mock_jwt_bearer, mock_db_session, mock_db_query):
    # Create the book
    response_create = client.post("/books/", json=mock_book.dict())
    assert response_create.status_code == 200
    created_book = response_create.json()

    # Get the created book
    response_get = client.get(f"/books/{created_book['id']}")
    assert response_get.status_code == 200
    assert response_get.json() == created_book

# Additional test cases

# Test get_book endpoint with non-existent book
@pytest.mark.asyncio
async def test_get_non_existent_book(mock_jwt_bearer, mock_db_session, mock_db_query):
    mock_db_query.filter.return_value.first.return_value = None
    response = client.get("/books/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

# Test list_books endpoint
@pytest.mark.asyncio
async def test_list_books(mock_jwt_bearer, mock_db_session, mock_db_query):
    response = client.get("/books/")
    assert response.status_code == 200
    assert response.json() == [book.dict() for book in mock_books]

# Test update_book endpoint with non-existent book
@pytest.mark.asyncio
async def test_update_non_existent_book(mock_jwt_bearer, mock_db_session, mock_db_query):
    mock_db_query.filter.return_value.first.return_value = None
    update_data = {"name": "Updated Book"}
    response = client.put("/books/999", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

# Test delete_book endpoint with non-existent book
@pytest.mark.asyncio
async def test_delete_non_existent_book(mock_jwt_bearer, mock_db_session, mock_db_query):
    mock_db_query.filter.return_value.first.return_value = None
    response = client.delete("/books/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

# Test list_books by author endpoint
@pytest.mark.asyncio
async def test_list_books_by_author(mock_jwt_bearer, mock_db_session, mock_db_query):
    mock_db_query.filter_by.return_value.all.return_value = mock_books
    response = client.get("/books/?author_id=1")
    assert response.status_code == 200
    assert response.json() == [book.dict() for book in mock_books]

