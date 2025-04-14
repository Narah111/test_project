import pytest
from hamcrest import assert_that, equal_to, contains_string, calling, raises
from html_utils import get_html_start_block, get_html_end_block, to_heading_line, to_text_paragraph, to_error_message, to_basic_html_page

#1.
def test_retriving_basic_html_block():
    # Given the 
    title_html = "Page"

    # When:getting the html page
    result_html_page = get_html_start_block(title_html)

    # Then assert that the html page contains: language english,has titel,UTF-8 sign language,html documentation type ans has a body 
    assert_that(result_html_page, contains_string('<!DOCTYPE html>'))
    assert_that(result_html_page, contains_string('<html lang="en">'))
    assert_that(result_html_page, contains_string('<meta charset="UTF-8">'))
    assert_that(result_html_page, contains_string(f"<title>{title_html}</title>"))
    assert_that(result_html_page, contains_string('<body>'))

#2.
def test_returns_html_end_block():

    #When retriving the html endblock
    result_html_end_block=get_html_end_block()

    #Then assert that it contains body and html
    assert_that(result_html_end_block,contains_string('body'))
    assert_that(result_html_end_block,contains_string('html'))

#3.
def test_creating_html_heading_line_text():
   #Given text value "Hello World" and text html heading of 1
   html_heading_size=1
   text='Hello World'
   
   # When retriving the result of value text and html_heading_size
   result_html_heading_line_text=to_heading_line(text,html_heading_size)

   #Then assert that the result of text is Hello World and heading line is of level 1
   assert_that(result_html_heading_line_text, equal_to(f"<h{html_heading_size}>{text}</h{html_heading_size}>\n"))

#4.
def test_get_html_text_paragraph():
    # Given a text paragraph
    text_paragraph="This is my short paragraph"


    #When retreiving the text paragraph
    result_text_paraghraph=to_text_paragraph(text_paragraph)

    #Then assert that the text paragraph is "This is my short paragraph"
    assert_that(result_text_paraghraph, equal_to(f"<p>{text_paragraph}</p>\n"))

#5.
def test_get_error_message():
    #Given error message
    text_message="Bona Dimiatza"
    #When retreving the error message
    result_given_text_message=to_error_message(text_message)
    #Then assert that the result contains Error, error occured and the error message
    assert_that(result_given_text_message, contains_string("Error!"))
    assert_that(result_given_text_message,contains_string("An error occurred"))
    assert_that(result_given_text_message, contains_string(text_message))