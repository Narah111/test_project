import pytest
from unittest.mock import patch
from rendering import format_welcome_message ,format_visit_history,format_visit_details,format_hello_greeting
from hamcrest import assert_that, contains_string


#6.
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


#7. Den generarar neråt och upp
@patch('rendering.get_html_end_block')#sist
@patch('rendering.to_text_paragraph')
@patch('rendering.to_heading_line')
@patch('rendering.get_html_start_block')# först
def test_get_users_visit_history(request_mock_start_block, request_mock_heading,request_mock_paragraph,request_mock_html_end_block):

    #Given html

    request_mock_start_block.return_value="<html>"
    request_mock_heading.return_value="<h1>Visit history</h1>"
    def mock_text_paragraph(text_paragraph):
        return f"<p>{text_paragraph}</p>"
    
    request_mock_paragraph.side_effect=mock_text_paragraph
    request_mock_html_end_block.return_value="</html>"

    #value of user_visits

    user_visit_id=[
        {
            "id":1,
            "timestamp":"2025-04-11 13:00 00",
            "ip":"127.0.0.1",
            "user_agent":"Mozilla/5.0"
        },
        {
            "id":2,
            "timestamp":"2025-04-11 17:00 00",
            "ip":"127.0.0.1",
            "user_agent":"Mozilla/5.0"

        }
    ]



    #When retreving the userid and html from function"format_visit_history"
    result_mock_value_user_history=format_visit_history(user_visit_id)

    #Then
    #heading-line
   
    assert_that(result_mock_value_user_history,contains_string("Visit history"))
    assert_that(result_mock_value_user_history,contains_string((f"- {user_visit_id[0]['timestamp']}: Visit #{user_visit_id[0]['id']}\n")))
    assert_that(result_mock_value_user_history,contains_string((f"- {user_visit_id[1]['timestamp']}: Visit #{user_visit_id[1]['id']}\n")))
    
#8.
@patch('rendering.get_html_end_block')#sist
@patch('rendering.to_text_paragraph')
@patch('rendering.to_heading_line')
@patch('rendering.get_html_start_block')# först
def test_get_user_visit_details(request_mock_start_block, request_mock_heading,request_mock_paragraph,request_mock_html_end_block):
    #Given
    request_mock_start_block.return_value="<html><h2>Visit details</h2>"

    def mock_text_headline(text_headline):
        return f"<h1>{text_headline}</h1>"
    request_mock_heading.side_effect=mock_text_headline
   

    def mock_text_paragraph(text_paragraph):
        return f"<p>{text_paragraph}</p>"
    
    request_mock_paragraph.side_effect=mock_text_paragraph


    request_mock_html_end_block.return_value="</html>"

    #value of user_visits
    user_visit_id={
            "id":1,
            "timestamp":"2025-04-11 13:00 00",
            "ip":"127.0.0.1",
            "user_agent":"Mozilla/5.0"
        }
        
    

    #When retreving the userid and html from function"format_visit_history"
    result_mock_value_user_details=format_visit_details(user_visit_id)

    print(result_mock_value_user_details)

    #Then
    assert_that(result_mock_value_user_details, contains_string("Visit details"))
    assert_that(result_mock_value_user_details, contains_string(f"Visit #{user_visit_id['id']}")) 
    assert_that(result_mock_value_user_details, contains_string(f"When: {user_visit_id['timestamp']}"))
    assert_that(result_mock_value_user_details, contains_string(f"IP: {user_visit_id['ip']}"))
    assert_that(result_mock_value_user_details, contains_string(f"User agent: {user_visit_id['user_agent']}"))

#9.
@patch('rendering.to_basic_html_page')
def test_gretting_message(request_mock_basic_html_page):
    #Given
    request_mock_basic_html_page.return_value="<html>Hello,Alice!</html>"
    user_name="Alice"

    #When
    result_getting_message=format_hello_greeting(user_name)

    #Then
    assert_that(result_getting_message,contains_string("Hello"))
    request_mock_basic_html_page.assert_called_once_with("Hello", f"Hello, {user_name}!")
   

