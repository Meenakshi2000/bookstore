import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app, create_book, update_book, delete_book, get_book_by_id, get_all_books
from database import Book

class TestBookAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "description": "Test Description",
            "price": 9.99
        }

    @patch('main.JWTBearer')
    @patch('main.get_db')
    def test_create_book(self, mock_get_db, mock_jwt_bearer):
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        response = self.client.post("/books/", json=self.book_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.book_data)

    @patch('main.JWTBearer')
    @patch('main.get_db')
    def test_update_book(self, mock_get_db, mock_jwt_bearer):
        mock_session = MagicMock()
        mock_book = Book(**self.book_data)
        mock_book.id = 1
        mock_session.query().filter().first.return_value = mock_book
        mock_get_db.return_value = mock_session

        update_data = {"title": "Updated Book"}
        response = self.client.put("/books/1", json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Updated Book")

    @patch('main.JWTBearer')
    @patch('main.get_db')
    def test_delete_book(self, mock_get_db, mock_jwt_bearer):
        mock_session = MagicMock()
        mock_book = Book(**self.book_data)
        mock_book.id = 1
        mock_session.query().filter().first.return_value = mock_book
        mock_get_db.return_value = mock_session

        response = self.client.delete("/books/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Book deleted successfully"})

    @patch('main.JWTBearer')
    @patch('main.get_db')
    def test_get_book_by_id(self, mock_get_db, mock_jwt_bearer):
        mock_session = MagicMock()
        mock_book = Book(**self.book_data)
        mock_book.id = 1
        mock_session.query().filter().first.return_value = mock_book
        mock_get_db.return_value = mock_session

        response = self.client.get("/books/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.book_data)

    @patch('main.JWTBearer')
    @patch('main.get_db')
    def test_get_all_books(self, mock_get_db, mock_jwt_bearer):
        mock_session = MagicMock()
        mock_books = [Book(**self.book_data), Book(**self.book_data)]
        mock_session.query().all.return_value = mock_books
        mock_get_db.return_value = mock_session

        response = self.client.get("/books/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

if __name__ == '__main__':
    unittest.main()