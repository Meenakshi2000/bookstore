import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app  # Import FastAPI app from the main module
from database import get_db, Book  # Import your Book model and get_db function

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

    # Set the expected return values for the database queries
    mock_session.query().filter().first.return_value = mock_book
    mock_session.query().all.return_value = mock_books

    with patch("database.get_db", return_value=mock_session):
        yield mock_session

# Test create_book endpoint
@pytest.mark.asyncio
async def test_create_book(mock_jwt_bearer, mock_db_session):
    response = client.post("/books/", json=mock_book.dict())
    assert response.status_code == 200
    assert response.json() == mock_book.dict()


# Test update_book endpoint
@pytest.mark.asyncio
async def test_update_book(mock_jwt_bearer, mock_db_session):
    update_data = {"name": "Updated Book"}
    response = client.put("/books/1", json=update_data)
    assert response.status_code == 200
    updated_book = mock_book.dict()
    updated_book.update(update_data)
    assert response.json() == updated_book


# Test delete_book endpoint
@pytest.mark.asyncio
async def test_delete_book(mock_jwt_bearer, mock_db_session):
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Book deleted successfully"}


# Test get_book_by_id endpoint
@pytest.mark.asyncio
async def test_get_book_by_id(mock_jwt_bearer, mock_db_session):
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json() == mock_book.dict()


# Test get_all_books endpoint
@pytest.mark.asyncio
async def test_get_all_books(mock_jwt_bearer, mock_db_session):
    response = client.get("/books/")
    assert response.status_code == 200
    assert response.json() == [book.dict() for book in mock_books]