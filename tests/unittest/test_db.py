import pytest
import psycopg2
from db import get_all_visits, get_visit_by_id, add_visit
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from hamcrest import *

@pytest.fixture
def mock_db():  # First define the mock fixture
    with patch("db.psycopg2.connect") as mock_connect:  
        # In mock syntax, only focus on the top-level function.
        # Everything under that is declared inside the mock body, and all sub-methods are written flatly.
        mock_conn = MagicMock()
        mock_cur = MagicMock()

        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur  # Flat writing with return_value chaining
        mock_cur.fetchone.return_value = [1]

        yield {
            "mock_connect": mock_connect,
            "mock_conn": mock_conn,
            "mock_cur": mock_cur
        }


@patch("db.datetime")  # Since datetime is also an external dependency, we patch it here
def test_add_visit_with_fixed_time(mock_datetime, mock_db):
    fixed_dt = datetime(2025, 1, 1, 8, 0, tzinfo=timezone.utc)  # tzinfo is required for timezone-aware datetime
    mock_datetime.now.return_value = fixed_dt
    mock_datetime.timezone = timezone  # timezone also needs to be mocked

    ip = "0.0.0.0"
    user_agent = "test_test"
    now = fixed_dt
    id = mock_db["mock_cur"].fetchone()  # Since yield returns a dictionary, use dict-style access rather than chaining like mock_db.mock_cur.fetchone()

    result = add_visit(ip, user_agent)
    mock_cur = mock_db["mock_cur"]  # Declare and extract cursor from fixture for repeated use

    # Behavior assertion to check if the function has been called with expected SQL and parameters
    mock_cur.execute.assert_called_with(
        'INSERT INTO visits (timestamp, ip, user_agent) VALUES (%s, %s, %s) RETURNING id',
        (now, ip, user_agent)
    )

    assert_that(result["ip"], equal_to("0.0.0.0"))
    assert_that(result["user_agent"], equal_to("test_test"))
    assert_that(result["id"], equal_to(1))
    assert_that(result["timestamp"], datetime)
    assert_that(result["timestamp"], equal_to(now))


def test_get_all_visits(mock_db):
    mock_cur = mock_db["mock_cur"]
    mock_cur.fetchall.return_value = [
        (1, "2025-01-01T00:00:00Z", "0.0.0.0", "test_test"),
        (2, "2025-01-02T00:00:00Z", "1.1.1.1", "testtest")
    ]

    result = get_all_visits()

    assert_that(result[0]["timestamp"], equal_to("2025-01-01T00:00:00Z"))
    assert_that(result[0]["ip"], equal_to("0.0.0.0"))
    assert_that(result[0]["user_agent"], equal_to("test_test"))
    assert_that(result[1]["ip"], equal_to("1.1.1.1"))
    assert_that(len(result), equal_to(2))


def test_get_all_visits_empty_list(mock_db):
    mock_cur = mock_db["mock_cur"]
    mock_cur.fetchall.return_value = []

    result = get_all_visits()

    assert_that(result, equal_to([]))  # Assert that an empty list is returned


def test_get_visit_by_id(mock_db):
    mock_cur = mock_db["mock_cur"]
    mock_cur.fetchone.return_value = (1, "2025-01-01T00:00:00Z", "0.0.0.0", "test_test")

    visit_id = 1

    result = get_visit_by_id(visit_id)

    # Behavior assertion to check if the function has been called
    mock_cur.execute.assert_called_with(
        'SELECT id, timestamp, ip, user_agent FROM visits WHERE id = %s', 
        (visit_id,)  # visit_id is a tuple, so the comma is required
    )

    assert_that(result["id"], equal_to(1))
    assert_that(result["ip"], equal_to("0.0.0.0"))
    assert_that(result["user_agent"], equal_to("test_test"))
    assert_that(result["timestamp"], equal_to("2025-01-01T00:00:00Z"))


def test_get_visit_by_none_id(mock_db):
    mock_cur = mock_db["mock_cur"]
    mock_cur.fetchone.return_value = None  # Mocking the behavior of not finding the value in DB

    visit_id = 1

    result = get_visit_by_id(visit_id)
    mock_cur.execute.assert_called_with(
        'SELECT id, timestamp, ip, user_agent FROM visits WHERE id = %s', 
        (visit_id,)
    )

    assert_that(result, equal_to(None))
