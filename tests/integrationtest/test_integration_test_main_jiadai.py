from datetime import datetime, timedelta
from hamcrest import *
import html

import pytest
from db import get_all_visits,get_visit_by_id





def test_root_homepage_should_log_user_visit_and_return_welcome_message(client):
    # When: när vi besöker root-route i main.py
    headers={"User-Agent":"Mozilla/5.0"} 

    respons_data=client.get("/",headers=headers)

    #Then: får vi 200OK i respons
    assert_that(respons_data.status_code, 200)

    all_db_visits=get_all_visits()
    get_visit=all_db_visits[-1] # senaste besöket


    user_agents=[v["user_agent"] for v in all_db_visits]
    welcome_message_to_user= f"Welcome, you are visitor number {get_visit['id']}"

    assert_that(respons_data.data.decode("utf-8"),contains_string(welcome_message_to_user))
    assert_that(user_agents,has_item(contains_string("Mozilla/5.0")))


def test_visits_history_with_no_date_range(client,visits):
    
    respons_data=client.get("/visits")
    assert_that(respons_data.status_code,200)
    visits=get_all_visits()
    assert_that(len(visits),greater_than(0))

def test_visits_history_within_date_range(client,visits):

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

def test_get_valid_visitor_with_id(client, singel_visit_with_id):
    visit_id = singel_visit_with_id
    
   
    response_data = client.get(f"/visit/{visit_id}")
    
    
    assert_that(response_data.status_code, equal_to(200))

    # gör resultatet till en sträng
    decoded_data = response_data.data.decode("utf-8")
    
    
    assert_that(decoded_data, contains_string("127.0.0.1"))  
    assert_that(decoded_data, contains_string("Mozilla/5.0")) 
   
    visit = get_visit_by_id(visit_id)
    
   
    assert_that(visit, is_not(None))
    assert_that(visit["id"], equal_to(visit_id))
    assert_that(visit["ip"], equal_to("127.0.0.1"))
    assert_that(visit["user_agent"], contains_string("Mozilla/5.0"))
    
def test_invalid_visitor_returns_error_404(client):
    invalid_id=999

    respons_data=client.get(f"/visit/{invalid_id}")

    assert_that(respons_data.status_code,404)
    assert_that(respons_data.data.decode("utf-8"),contains_string("Visit not found"))




