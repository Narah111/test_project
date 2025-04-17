from hamcrest import *


def test_visit_with_valid_id(client,visits):
    response = client.get("/visit/1")
    assert_that(response.status_code, 200)
    html = response.data.decode()
    assert_that(html,contains_string("TestSuiteAgent1"))

def test_visit_with_invalid_id(client,visits):
    response = client.get("/visit/999")
    assert_that(response.status_code, 404)
    html = response.data.decode()
    assert_that(html,contains_string("Visit not found"))

