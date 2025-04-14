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
