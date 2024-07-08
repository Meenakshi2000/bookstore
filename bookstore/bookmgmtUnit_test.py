import unittest
from fastapi.testclient import TestClient
from main import app

class TestBookManagementAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.book_data = {
            "name": "Your Book Name",
            "author": "John Doe",
            "published_year": 2023,
            "book_summary": "Your book summary"
        }

        # Bearer token for authentication
        self.token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtZWVuYWtzaGkuZGFpc3lAZ21haWwuY29tIiwiZXhwIjoxNzIwMjkyNzQxfQ.RReI4TAZ_IKWX_-EMnJIQqZS31Imz0oEVAE-dKTiCE8"

    def get_headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def test_create_book(self):
        headers = self.get_headers()
        response = self.client.post("/books/", json=self.book_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        created_book = response.json()
        self.assertEqual(created_book["name"], self.book_data["name"])
        self.assertEqual(created_book["author"], self.book_data["author"])
        self.assertEqual(created_book["published_year"], self.book_data["published_year"])
        self.assertEqual(created_book["book_summary"], self.book_data["book_summary"])

    def test_update_book(self):
        headers = self.get_headers()
        response = self.client.post("/books/", json=self.book_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        created_book = response.json()

        updated_data = {
            "name": "Updated Book Name",
            "author": "Jane Doe",
            "published_year": 2024,
            "book_summary": "Updated book summary"
        }
        response = self.client.put(f"/books/{created_book['id']}", json=updated_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        updated_book = response.json()
        self.assertEqual(updated_book["name"], updated_data["name"])
        self.assertEqual(updated_book["author"], updated_data["author"])
        self.assertEqual(updated_book["published_year"], updated_data["published_year"])
        self.assertEqual(updated_book["book_summary"], updated_data["book_summary"])

    def test_delete_book(self):
        headers = self.get_headers()
        response = self.client.post("/books/", json=self.book_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        created_book = response.json()

        response = self.client.delete(f"/books/{created_book['id']}", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Book deleted successfully"})

    def test_get_book_by_id(self):
        headers = self.get_headers()
        response = self.client.post("/books/", json=self.book_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        created_book = response.json()

        response = self.client.get(f"/books/{created_book['id']}", headers=headers)
        self.assertEqual(response.status_code, 200)
        retrieved_book = response.json()
        self.assertEqual(retrieved_book["name"], self.book_data["name"])
        self.assertEqual(retrieved_book["author"], self.book_data["author"])
        self.assertEqual(retrieved_book["published_year"], self.book_data["published_year"])
        self.assertEqual(retrieved_book["book_summary"], self.book_data["book_summary"])

    def test_get_all_books(self):
        headers = self.get_headers()
        response = self.client.get("/books/", headers=headers)
        self.assertEqual(response.status_code, 200)
        books_list = response.json()
        self.assertIsInstance(books_list, list)
        if books_list:
            first_book = books_list[0]
            self.assertEqual(first_book["name"], self.book_data["name"])
            self.assertEqual(first_book["author"], self.book_data["author"])
            self.assertEqual(first_book["published_year"], self.book_data["published_year"])
            self.assertEqual(first_book["book_summary"], self.book_data["book_summary"])



if __name__ == "__main__":
    unittest.main()

