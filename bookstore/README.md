# Bookstore API

## Overview

This project is a simple Bookstore API built with FastAPI. It allows users to manage books and perform user authentication, including sign-up and login functionalities. The API uses JWT tokens for securing endpoints related to book management.

## Features

- **Book Management**: Users can create, update, delete, and retrieve books.
- **User Authentication**: Includes user sign-up and login functionalities.
- **Secure Endpoints**: Uses JWT tokens to secure book management endpoints.

## Technologies

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **Passlib**: Comprehensive password hashing library for Python.
- **JWT**: JSON Web Tokens for securely transmitting information between parties.

## Getting Started

### Prerequisites

- Python 3.7+
- pip

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/sanjay-dandekar-jktech/git
    ```

2. Navigate to the project directory:

    ```bash
    cd bookstore
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1. Start the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

2. The API will be available at `http://127.0.0.1:8000`

### API Endpoints

- Book Management

    - POST /books/: Create a new book.
    - PUT /books/{book_id}: Update a book by ID.
    - DELETE /books/{book_id}: Delete a book by ID.
    - GET /books/{book_id}: Get a book by ID.
    - GET /books/: Get all books.

- User Authentication

    - POST /signup: Sign up a new user.
    - POST /login: Log in and receive an access token.

- Health Check
    - GET /health: Check the health of the API.

### Running using Docker

- Use the following command to bring up the bookstore API container

  ```bash
  docker compose up --build -d bookstore
  ```

### License
    This project is licensed under the MIT License - see the LICENSE file for details


### Prerequisites for Running Tests

Install dependencies: Open your terminal and navigate to the directory containing this file. Run the following command:

          pip install -r bookstore/requirements.txt  
          pip install -U coverage
          pip install pytest
          pip install pytest-asyncio

Note : Manually delete test.db(if exists) before running the testcases.
Run tests: Execute the following command in your terminal:

### Integration Tests
pytest bookstore\bookInt_test.py

Test Cases:

test_create_book: Simulates creating a new book and verifies a successful response (200) with the created book data.

test_update_book: Simulates updating an existing book and verifies a successful response (200) with the updated book data.

test_delete_book: Simulates deleting a book and verifies a successful response (200) with a confirmation message.

test_create_and_get_book: Simulates creating a book, then retrieves the created book by ID and verifies the retrieved data matches the created book.

Additional Test Cases:

test_get_non_existent_book (expected 404 Not Found for a non-existent book).
test_list_books (retrieves all books and verifies the response matches the expected data).
test_update_non_existent_book (expected 404 Not Found when updating a non-existent book).
test_delete_non_existent_book (expected 404 Not Found when deleting a non-existent book).
test_list_books_by_author (filters books by author ID and verifies the response matches the expected data) (Replace with your actual implementation if applicable).

### Unit Tests
pytest bookstore\bookUnit_test.py

Test Cases:

Test Cases:

test_login_and_access_books_apis:

Simulates user signup and login to obtain an access token.
Uses the access token to perform CRUD (Create, Read, Update, Delete) operations on books:
Creates a new book.
Retrieves all books.
Retrieves a specific book by ID.
Updates the created book.
Deletes the created book.
Verifies successful responses (200 status code) and validates data returned for each operation.
test_book_api_error_handling:

Simulates user login to obtain an access token.
Uses the access token to test error handling for book APIs:
Tries to retrieve a book with a non-existent ID (expected 404 Not Found).
Tries to update a book with a non-existent ID (expected 404 Not Found).
Tries to delete a book with a non-existent ID (expected 404 Not Found).
Verifies appropriate error codes (404 Not Found) for these scenarios.