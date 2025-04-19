import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:5000"

def test_root_route(page):
    page.goto(BASE_URL + "/")
    assert "Welcome, you are visitor number " in page.content() 


def test_visits_route(page):
    response = page.goto(BASE_URL + "/visits")
    assert response.status == 200 
    
def test_hello_form_page(page):
    page.goto(BASE_URL + "/hello-form")
    assert "Say Hello" in page.content()

def test_hello_form_with_name(page):
    page.goto(BASE_URL + "/hello?name=Alice")
    assert "Alice" in page.content()

def test_invalid_visit_id(page):
    response =page.goto(BASE_URL + "/visit/999999") 
    assert response.status == 404 or "not found" in page.content().lower()

