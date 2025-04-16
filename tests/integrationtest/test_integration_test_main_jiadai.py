from datetime import datetime, timedelta
from hamcrest import *
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