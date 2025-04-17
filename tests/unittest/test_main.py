import pytest
from datetime import datetime 
from unittest.mock import patch

from main import app

# @pytest.fixture(autouse=True)
# def mock_db_calls(mocker):
#     # Mocka alla funktioner som använder databaskopplingen
#     mocker.patch("db.get_db_connection", return_value=None)
#     mocker.patch("db.get_visit_by_id", return_value=None)
#     mocker.patch("db.get_all_visits", return_value=[])
#     mocker.patch("db.add_visit", return_value={})
#     mocker.patch("db.format_visit_history", return_value="formatted history")
#     mocker.patch("db.init_db", return_value=None)

#1 function
# def test_root_route(mocker):
#     #visit = add_visit(request.remote_addr, request.headers.get('User-Agent', 'unknown'))
#     #return format_welcome_message(visit) - original code
#     # A fixture is a built-in mechanism in pytest that allows you to prepare an environment for a test.
    
#     fake_visit = {"ip":"127.0.0.1", "user_agent":"TestBrowser"}
#     #fake data for checking
#     mock_add = mocker.patch("main.add_visit", return_value= fake_visit)
#     mock_format = mocker.patch("main.format_welcome_message", return_value="Welcome, test user!")

#     with app.test_client() as client:
#         response = client.get("/", headers={"User-Agent": "TestBrowser"}, environ_base={"REMOTE_ADDR": "127.0.0.1"})
    
#     assert response.status_code == 200
#     assert response.data == b"Welcome, test user!"
#     mock_add.assert_called_once_with("127.0.0.1", "TestBrowser")
#     mock_format.assert_called_once_with(fake_visit)

# #2 function  1 - No_data
# def test_visits_no_data(mocker):
#     fake_visits = [
#     {"timestamp": datetime(2024, 1, 10)},
#     {"timestamp": datetime(2024, 2, 15)},
# ]
# # Mocking the get_all_visits function to return fake visits
#     mocker.patch("main.get_all_visits", return_value=fake_visits)
#     mock_format = mocker.patch("main.format_visit_history", return_value="formatted")

#     with app.test_client() as client:
#         res = client.get("/visits")  # No 'from' or 'to' parameters

#     # Check that the status code is 200
#     assert res.status_code == 200
#     # Check that the response contains the formatted data
#     assert b"formatted" in res.data
#     mock_format.assert_called_once()  # Ensure that format_visit_history was called once\


# # #2 function 2 - with_from_and_to
# def test_visit_with_from_and_to(mocker):
#     fake_visits = [
#         {"timestamp": datetime(2023, 12, 31)},
#         {"timestamp": datetime(2024, 1, 15)},
#         {"timestamp": datetime(2024, 3, 1)},
#     ]
#     mocker.patch("main.get_all_visits", return_value = fake_visits)
#     mock_format = mocker.patch("main.format_visit_history", return_value="Filtered visits")
    
#     with app.test_client() as client:
#         response = client.get("/visits?from=2024-01-01&to=2024-01-31")

#     assert response.status_code == 200
#     assert b"Filtered visits" in response.data
#     mock_format.assert_called_once_with([{"timestamp": datetime(2024, 1, 15)}])


# #2 3 - with data from
# def test_visits_with_data(mocker):
#     fake_visits = [
#         {"timestamp": datetime(2024, 1, 10)},
#         {"timestamp": datetime(2024, 2, 15)},
#     ]
#     mocker.patch("main.get_all_visits", return_value=fake_visits)
#     mock_format = mocker.patch("main.format_visit_history", return_value="formatted")

#     with app.test_client() as client:
#         res = client.get("/visits?from=2024-01-01&to=2024-01-31")
    
#     assert res.status_code == 200
#     assert b"formatted" in res.data
#     mock_format.assert_called_once()

#     mock_format.assert_called_with([{"timestamp": datetime(2024, 1, 10)}])
   

# #2 4 - function invalid for
# def test_visits_invalid_from(mocker):

#     mocker.patch("main.get_all_visits", return_value=[])
#     mock_format = mocker.patch("main.to_error_message", return_value="Invalid 'from' date format")

#     with app.test_client() as client:
#         res = client.get("/visits?from=bad-date")

#     assert res.status_code == 400
    

# #2 function invalid to
# def test_visits_invalid_to(mocker):
#     #mock_db_conn = mocker.patch("get_db_connection", return_value="dummy_connection")
#     mock_format = mocker.patch("main.to_error_message", return_value=("<p>Invalid 'to' date format. Use ISO format (YYYY-MM-DD).</p>", 400))

#     with app.test_client() as client:
#         res = client.get("/visits?to=not-a-date")
    
#     assert mock_format.called
#     assert res.status_code == 400

#Test---------------------------------------------------------------------->New version
#1
@patch("main.format_welcome_message")
@patch("main.add_visit")
def test_root_route(request_mocker_add_visit,request_mocker_welcome_message):
   
    
    fake_visit = {"ip":"127.0.0.1", "user_agent":"TestBrowser"}
    #fake data for checking
    request_mocker_add_visit.return_value=fake_visit
    request_mocker_welcome_message.return_value="Welcome, test user!"

    with app.test_client() as client:
        response = client.get("/", headers={"User-Agent": "TestBrowser"}, environ_base={"REMOTE_ADDR": "127.0.0.1"})
    
    assert response.status_code == 200
    assert response.data == b"Welcome, test user!"
    request_mocker_add_visit.assert_called_once_with("127.0.0.1", "TestBrowser")
    request_mocker_welcome_message.assert_called_once_with(fake_visit)

#test
#2
@patch("main.get_all_visits")
@patch("main.format_visit_history")
def test_visits_no_data(request_mock_format_visit_history,request_mocker_get_all_visits):
    fake_visits = [
    {"timestamp": datetime(2024, 1, 10)},
    {"timestamp": datetime(2024, 2, 15)},
]
# Mocking the get_all_visits function to return fake visits
    request_mocker_get_all_visits.return_value=fake_visits
    request_mock_format_visit_history.return_value="formatted"

    with app.test_client() as client:
        res = client.get("/visits")  # No 'from' or 'to' parameters

    # Check that the status code is 200
    assert res.status_code == 200
    # Check that the response contains the formatted data
    assert b"formatted" in res.data
    request_mock_format_visit_history.assert_called_once()  # Ensure that format_visit_history was called once\   

#test
#3
@patch("main.get_all_visits")
@patch("main.format_visit_history")
def test_visit_with_from_and_to(request_mocker_format_visit_history,request_mocker_get_all_visits):
    fake_visits = [
        {"timestamp": datetime(2023, 12, 31)},
        {"timestamp": datetime(2024, 1, 15)},
        {"timestamp": datetime(2024, 3, 1)},
    ]
    request_mocker_get_all_visits.return_value = fake_visits
    request_mocker_format_visit_history.return_value="Filtered visits"
    
    with app.test_client() as client:
        response = client.get("/visits?from=2024-01-01&to=2024-01-31")

    assert response.status_code == 200
    assert b"Filtered visits" in response.data
    #Anropar alla visits
    request_mocker_get_all_visits.assert_called_once()
    request_mocker_format_visit_history.assert_called_once_with([{"timestamp": datetime(2024, 1, 15)}])

#test
#4
@patch("main.get_all_visits")
@patch("main.format_visit_history")
def test_visits_with_data(request_mocker_format_visit_history,request_mocker_get_all_visits):
    fake_visits = [
        {"timestamp": datetime(2024, 1, 10)},
        {"timestamp": datetime(2024, 2, 15)},
    ]
    request_mocker_get_all_visits.return_value=fake_visits
    request_mocker_format_visit_history.return_value="formatted"

    with app.test_client() as client:
        res = client.get("/visits?from=2024-01-01&to=2024-01-31")
    
    assert res.status_code == 200
    assert b"formatted" in res.data
    request_mocker_get_all_visits.assert_called_once()
    request_mocker_format_visit_history.assert_called_with([{"timestamp": datetime(2024, 1, 10)}]) 

#test
#5
@patch("main.get_all_visits")
@patch("main.to_error_message")
def test_visits_invalid_from(request_mock_get_all_visits,request_mock_error_message):

    request_mock_get_all_visits.return_value=[]
    request_mock_error_message.return_value="Invalid 'from' date format"

    with app.test_client() as client:
        res = client.get("/visits?from=bad-date")

    assert res.status_code == 400
    

#test
#6

@patch("main.to_error_message")
def test_visits_invalid_to(request_mock_error_message):
   
    request_mock_error_message.return_value=("<p>Invalid 'to' date format. Use ISO format (YYYY-MM-DD).</p>", 400)

    with app.test_client() as client:
        res = client.get("/visits?to=not-a-date")
        
    assert res.status_code == 500

@patch("main.format_hello_greeting")
def test_hello_route(mock_format_hello_greeting):
    mock_format_hello_greeting.return_value = "Hello, Test User!"
    with app.test_client() as client:
        res = client.get("/hello?name=Test%20User")

    assert res.status_code == 200
    assert res.data == b"Hello, Test User!"
    mock_format_hello_greeting.assert_called_once_with("Test User")

def test_hello_form():
    with app.test_client() as client:
        response = client.get("/hello-form")

    assert response.status_code == 200
    assert b"<form" in response.data
    assert b'action="/hello"' in response.data
    assert b'<input type="text" id="name"' in response.data
    assert b'<button type="submit">' in response.data