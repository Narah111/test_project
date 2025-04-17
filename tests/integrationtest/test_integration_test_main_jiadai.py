from datetime import datetime, timedelta
from hamcrest import *
import html

import pytest
from db import get_all_visits





def test_root_homepage_should_log_user_visit_and_return_welcome_message(client):
    # When: när vi besöker root-route i main.py
    headers={"User-Agent":"TestSuiteAgent"} 

    respons_data=client.get("/",headers=headers)

    #Then: får vi 200OK i respons
    assert_that(respons_data.status_code, 200)

    all_db_visits=get_all_visits()
    get_visit=all_db_visits[-1] # senaste besöket


    user_agents=[v["user_agent"] for v in all_db_visits]
    welcome_message_to_user= f"Welcome, you are visitor number {get_visit['id']}"

    assert_that(respons_data.data.decode("utf-8"),contains_string(welcome_message_to_user))
    assert_that(user_agents,has_item(contains_string("TestSuiteAgent")))


def test_visits_with_no_date_range(client,visits):
    
    respons_data=client.get("/visits")
    assert_that(respons_data.status_code,200)
    visits=get_all_visits()
    assert_that(len(visits),greater_than(0))

def test_visits_within_date_range(client,visits):

    from_date ="2025-03-11"
    to_date="2025-07-11"

    respons_data= client.get(f"/visits?from={from_date}&to={to_date}")
    assert_that(respons_data.status_code,200)
    visits=get_all_visits()
    assert_that(len(visits),greater_than(0))
    for visit in visits:
        visit_date=visit["timestamp"]

    assert_that(visit_date,greater_than_or_equal_to(datetime.fromisoformat(from_date)))
    assert_that(visit_date,less_than_or_equal_to(datetime.fromisoformat(to_date)))

def test_invalid_visits_to_date_format(client):

    respons_data=client.get("/visits?from=2025-03-11&to=invalid-date")
    error_message="Invalid 'to' date format"

    body_text=html.unescape(respons_data.data.decode("utf-8"))

    assert_that(respons_data.status_code, 400)
    assert_that(body_text,contains_string(error_message))

def test_invalid_visits_from_date_format(client):
    respons_data=client.get("/visits?from=invalid-format&to=2025-05-11")
    error_message="Invalid 'from' date format"

    body_text=html.unescape(respons_data.data.decode("utf-8"))

    assert_that(respons_data.status_code, 400)
    assert_that(body_text,contains_string(error_message))



