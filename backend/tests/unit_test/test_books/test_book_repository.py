import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.db.repositories.books import BookRepository
from app.models.books import BookModel, BookStatus
from app.orm_model.book import Book

pytestmark = pytest.mark.asyncio


@pytest.fixture
def sample_book_model():
    return BookModel(
        title="Sample Book",
        author="Author Name",
        book_id="book123",
        quantity=3,
        category="Fiction",
        status=BookStatus.available
    )


@pytest.fixture
def book_repo():
    return BookRepository()


@patch("app.api.dependencies.database.add_update_table", new_callable=AsyncMock)
@patch.object(BookRepository, "retrieve_book_quantity", new_callable=AsyncMock)
async def test_add_book_new_entry(mock_retrieve, mock_add_update_table, sample_book_model, book_repo):
    mock_session = AsyncMock()
    mock_session.add = MagicMock()  # Prevent RuntimeWarning

    # Simulate no existing book
    mock_retrieve.return_value = None

    # Mock returned Book from DB after creation
    db_book = Book(
        book_id=sample_book_model.book_id,
        title=sample_book_model.title,
        author=sample_book_model.author,
        quantity=sample_book_model.quantity,
        category=sample_book_model.category,
        status=BookStatus.available,
    )
    mock_add_update_table.return_value = db_book

    result = await book_repo.add_book(mock_session, sample_book_model)

    assert result["book_id"] == sample_book_model.book_id
    assert result["quantity"] == sample_book_model.quantity
    assert result["status"] == BookStatus.available.value
    mock_session.add.assert_called_once()


@patch("app.api.dependencies.database.add_update_table", new_callable=AsyncMock)
@patch.object(BookRepository, "retrieve_book_quantity", new_callable=AsyncMock)
async def test_add_book_existing_entry(mock_retrieve, mock_add_update_table, sample_book_model, book_repo):
    mock_session = AsyncMock()
    mock_session.add = MagicMock()  # Prevent RuntimeWarning

    existing_book = Book(
        book_id=sample_book_model.book_id,
        title=sample_book_model.title,
        author=sample_book_model.author,
        quantity=2,
        category=sample_book_model.category,
        status=BookStatus.available,
    )

    mock_retrieve.return_value = existing_book
    mock_add_update_table.return_value = existing_book  # Let the function update quantity

    result = await book_repo.add_book(mock_session, sample_book_model)

    assert result["quantity"] == 5
    assert result["book_id"] == sample_book_model.book_id
    mock_session.add.assert_not_called()


@patch("app.db.repositories.books.logger")
@patch.object(BookRepository, "retrieve_book_quantity", new_callable=AsyncMock)
async def test_add_book_db_error(mock_retrieve, mock_logger, sample_book_model, book_repo):
    mock_session = AsyncMock()
    mock_session.add = MagicMock()  # Just in case

    # Simulate failure inside retrieve_book_quantity
    mock_retrieve.side_effect = Exception("DB failure")

    with pytest.raises(Exception):
        await book_repo.add_book(mock_session, sample_book_model)

    assert mock_logger.error.call_count >= 1
    mock_logger.error.assert_any_call("Error retrieving book quantity in the database: DB failure")
