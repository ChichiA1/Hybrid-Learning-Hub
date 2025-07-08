import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient
from fastapi import status
from httpx._transports.asgi import ASGITransport
# from app.models.books import BookModel  # Adjust the import path as needed


class TestBookEndpoints:

    @pytest.mark.asyncio
    @patch('app.api.routes.books.book_repo')  # Adjust the path if different
    async def test_add_book_success(self, mock_book_repo, client, test_book):
        """Test successful book creation"""

        # Mock return value from book_repo.add_book
        mock_book_repo.add_book = AsyncMock(return_value=test_book)

        async with AsyncClient(transport=ASGITransport(app=client.app), base_url="http://test") as ac:
            response = await ac.post(
                "/api/books/add-book/",
                json={
                    "title": test_book.title,
                    "author": test_book.author,
                    "book_id": test_book.book_id,
                    "quantity": test_book.quantity,
                    "category": test_book.category,
                    "status": test_book.status.value
                }
            )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["book_id"] == test_book.book_id
        assert data["title"] == test_book.title
        assert data["author"] == test_book.author
        assert data["category"] == test_book.category
        assert data["quantity"] == test_book.quantity
        assert data["status"] == test_book.status.value

    @pytest.mark.asyncio
    @patch('app.api.routes.books.book_repo')
    async def test_add_book_bad_request(self, mock_book_repo, client):
        """Test book creation with bad request data"""

        async with AsyncClient(transport=ASGITransport(app=client.app), base_url="http://test") as ac:
            response = await ac.post(
                "/api/books/add-book/",
                json={
                    "title": "Test Book"
                    # Missing required fields: author, book_id, etc.
                }
            )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    @patch('app.api.routes.books.book_repo')
    async def test_add_book_server_error(self, mock_book_repo, client, test_book):
        """Test book creation server error"""

        mock_book_repo.add_book.side_effect = Exception("Unexpected DB Error")

        async with AsyncClient(transport=ASGITransport(app=client.app), base_url="http://test") as ac:
            response = await ac.post(
                "/api/books/add-book/",
                json={
                    "title": test_book.title,
                    "author": test_book.author,
                    "book_id": test_book.book_id,
                    "quantity": test_book.quantity,
                    "category": test_book.category,
                    "status": test_book.status.value
                }
            )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
