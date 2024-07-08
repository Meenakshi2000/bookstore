import pytest
import httpx

# Replace with your actual FastAPI application and configuration
from main import app
from database import DATABASE_URL

@pytest.fixture(scope="module")
def test_app():

    yield app

@pytest.mark.asyncio
async def test_login_and_access_books_apis(test_app):
    async with httpx.AsyncClient(app=test_app, base_url="http://testserver") as client:
        # Step 1: Simulate login to obtain access token
                # Step 1: Simulate login to obtain access token
        signup_url = "/signup"
        signup_data = {
            "name": "Meenakshi Kumar",
            "email": "meenakshi.daisy@gmail.com",
            "password": "password123",
            "passwordConfirm": "password123",
            "photo": "default.png"

        }

        response = await client.post(signup_url, json=signup_data)
        assert response.status_code == 200
        login_url = "/login"
        login_data = {
            "email": "meenakshi.daisy@gmail.com",
            "password": "password123"
        }

        response = await client.post(login_url, json=login_data)
        assert response.status_code == 200
        token_response = response.json()
        access_token = token_response.get('access_token')
        print("access_token",access_token)
        assert access_token is not None

        # Step 2: Use the obtained access token to access book-related APIs
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        # Create a book
        create_book_url = "/books/"
        book_data = {
            "name": "Your Book Name",
            "author": "John Doe",
            "published_year": 2023,
            "book_summary": "Your book summary"
        }
        response = await client.post(create_book_url, json=book_data, headers=headers)
        assert response.status_code == 200
        created_book = response.json()
        assert created_book["name"] == "Your Book Name"
        assert created_book["author"] == "John Doe"

        # Retrieve all books
        get_all_books_url = "/books/"
        response = await client.get(get_all_books_url, headers=headers)
        assert response.status_code == 200
        all_books = response.json()
        assert len(all_books) > 0  # Assuming at least one book is created

        # Retrieve a specific book by ID
        get_book_by_id_url = f"/books/{created_book['id']}"
        response = await client.get(get_book_by_id_url, headers=headers)
        assert response.status_code == 200
        retrieved_book = response.json()
        assert retrieved_book["id"] == created_book["id"]

        # Update the created book
        update_book_url = f"/books/{created_book['id']}"
        update_data = {
            "name": "Updated Book Name"
        }
        response = await client.put(update_book_url, json=update_data, headers=headers)
        assert response.status_code == 200
        updated_book = response.json()
        assert updated_book["name"] == "Updated Book Name"

        # Delete the created book
        delete_book_url = f"/books/{created_book['id']}"
        response = await client.delete(delete_book_url, headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Book deleted successfully"}





@pytest.mark.asyncio
async def test_book_api_error_handling(test_app):
    async with httpx.AsyncClient(app=test_app, base_url="http://testserver") as client:
        # Step 1: Simulate login to obtain access token
        login_url = "/login"
        login_data = {
            "email": "meenakshi.daisy@gmail.com",
            "password": "password123"
        }

        response = await client.post(login_url, json=login_data)
        assert response.status_code == 200
        token_response = response.json()
        access_token = token_response.get('access_token')
        assert access_token is not None

        # Step 2: Use the obtained access token to access book-related APIs
        headers = {
            "Authorization": f"Bearer {access_token}"
        }



        # Test retrieving a book that doesn't exist
        get_invalid_book_url = "/books/99999"  # Assuming this ID doesn't exist
        response = await client.get(get_invalid_book_url, headers=headers)
        assert response.status_code == 404  # Not Found

        # Test updating a book with invalid data
        update_invalid_book_url = "/books/99999"  # Assuming this ID doesn't exist
        invalid_update_data = {
            "name": "Updated Book Name"
        }
        response = await client.put(update_invalid_book_url, json=invalid_update_data, headers=headers)
        assert response.status_code == 404  # Not Found

        # Test deleting a book that doesn't exist
        delete_invalid_book_url = "/books/99999"  # Assuming this ID doesn't exist
        response = await client.delete(delete_invalid_book_url, headers=headers)
        assert response.status_code == 404  # Not Found        
