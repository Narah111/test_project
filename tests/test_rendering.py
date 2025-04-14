import pytest
from unittest.mock import patch
from rendering import format_welcome_message ,format_visit_history,format_visit_details,format_hello_greeting
from hamcrest import assert_that, contains_string


#1.
@patch('rendering.to_basic_html_page')
def test_get_welcome_message_to_user(request_mock_basic_html_page):
    #Given mocked html data and user_id
    request_mock_basic_html_page.return_value="<html>Welcome<html>"
    user_visit_id={"id":5}

    #When retriving the user_id and html
    welcome_message_result=format_welcome_message(user_visit_id)

    #Then welcome message contains Welcome and 
    assert_that(welcome_message_result,contains_string("Welcome"))
    request_mock_basic_html_page.assert_called_once_with("Welcome","Welcome, you are visitor number 5")


