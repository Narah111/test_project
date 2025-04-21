from playwright.sync_api import sync_playwright, expect, Playwright
import json
import re

 
APPLICATION_BASE_URL = "http://127.0.0.1:5000"
 
def test_homepage():
     with sync_playwright() as p:
         browser = p.chromium.launch(headless=False)
         context = browser.new_context()
         page = context.new_page()
 
         page.goto(f"{APPLICATION_BASE_URL}")
         
         page_text = page.locator("p")
         expect(page_text).to_contain_text("Welcome")
 
         browser.close()
 
def test_visits_page():
     with sync_playwright() as p:
         browser = p.chromium.launch(headless=False)
         context = browser.new_context()
         page = context.new_page()
 
         response = page.goto(f"{APPLICATION_BASE_URL}/visits")
         assert response.ok, f"Expected 200, got {response.status}"
         
         pre_tag = page.locator("pre")
 
         expect(pre_tag).to_be_visible()
 
         json_text = pre_tag.inner_text()
         assert json_text.strip(), "Expected non-empty"
         assert re.match(r"^\s*(\{.*\}|\[.*\])\s*$", json_text, re.DOTALL), "Text does not resemble JSON"
 
         try:
             json.loads(json_text)
         except json.JSONDecodeError as e:
             print(f"Raw content: {json_text}")
             raise AssertionError("Content in <pre> is not valid json") from e
         
         browser.close()
     
 
def test_visit_with_specific_id():
     with sync_playwright() as p:
         browser = p.chromium.launch(headless=False)
         context = browser.new_context()
         page = context.new_page()
 
         response = page.goto(f"{APPLICATION_BASE_URL}/visit/1")
         assert response.ok, f"Expected 200, got {response.status}"
 
         visit_id = page.locator("h1")
 
         expect(visit_id).to_be_visible()
         expect(visit_id).to_contain_text("Visit #1")
 
         browser.close()
 
def test_visit_hello_page():
     with sync_playwright() as p:
         browser = p.chromium.launch(headless=False)
         context = browser.new_context()
         page = context.new_page()
 
         response = page.goto(f"{APPLICATION_BASE_URL}/hello")
         assert response.ok, f"Expected 200, got {response.status}"
 
         text_content = page.locator("p")
 
         expect(text_content).to_be_visible()
         expect(text_content).to_have_text("Hello, mysterious visitor!")
 
         browser.close()
 
def test_hello_form():
     with sync_playwright() as p:
         browser = p.chromium.launch(headless=False)
         context = browser.new_context()
         page = context.new_page()
 
         response = page.goto(f"{APPLICATION_BASE_URL}/hello-form")
         assert response.ok, f"Expected 200, got {response.status}"
 
         input = page.get_by_role("textbox")
 
         expect(input).to_be_visible()
         expect(input).to_be_enabled()
 
         input.focus()
 
         expect(input).to_be_focused()
 
         input.fill("Playwright test")
 
         button = page.get_by_role("button")
         button.focus()
         button.click()
 
         expect(page).to_have_url(f"{APPLICATION_BASE_URL}/hello?name=Playwright+test")
 
         hello_text = page.locator("p")
         expect(hello_text).to_have_text("Hello, Playwright test!")