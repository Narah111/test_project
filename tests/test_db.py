import pytest
import psycopg2
from db import get_all_visits, get_visit_by_id, add_visit
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from hamcrest import *

@pytest.fixture
def mock_db(): #先定义mock方法
    with patch("db.psycopg2.connect") as mock_connect: #在mock的格式里，只关注最上层的方法是什么，这个方法之下都在mock方法内部声明，而且无论下属方法层级如何，都是用平级写法
        mock_conn = MagicMock()
        mock_cur = MagicMock()

        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur #虽然用平级写法，但用retuern_value进行链式调用
        mock_cur.fetchone.return_value = [1]

        yield{
            "mock_connect" : mock_connect,
            "mock_conn" : mock_conn,
            "mock_cur" :mock_cur
        }


@patch("db.datetime") #由于原方法饿时间也是一个外部依赖，所以这里用patch mock了datetime
def test_add_visit_with_fixed_time(mock_datetime,mock_db):
    fiexd_dt = datetime(2025, 1, 1, 8, 0, tzinfo=timezone.utc) #tzinfo是固定写法，如果不写tzinfo就默认无时区
    mock_datetime.now.return_value = fiexd_dt
    mock_datetime.timezone = timezone #这里timezone也需要mock


    ip = "0.0.0.0"
    user_agent = "test_test"
    now = fiexd_dt
    id = mock_db["mock_cur"].fetchone()      #因为yeild返回的是一个字典，所以需要用字典取值的方式，而不能直接链式调用mock_db.mock_cur.fetchone() 

    result = add_visit(ip, user_agent)
    mock_cur = mock_db["mock_cur"] #声明并把fiture里的cursor封装以便反复使用

    mock_cur.execute.assert_called_with('INSERT INTO visits (timestamp, ip, user_agent) VALUES (%s, %s, %s) RETURNING id',(now, ip, user_agent)) ##behavior assertion to check if funection has been called
    
    assert_that(result["ip"], equal_to("0.0.0.0"))
    assert_that(result["user_agent"], equal_to("test_test"))
    assert_that(result["id"], equal_to(1))
    assert_that(result["timestamp"], datetime)
    assert_that(result["timestamp"], equal_to(now))


def test_get_all_visits(mock_db):
    mock_cur = mock_db["mock_cur"]
    mock_cur.fetchall.return_value = [
        (1,"2025-01-01T00:00:00Z", "0.0.0.0", "test_test"),
        (2,"2025-01-02T00:00:00Z", "1.1.1.1", "testtest")
    ]

    result = get_all_visits()

    assert_that(result[0]["timestamp"],equal_to("2025-01-01T00:00:00Z"))
    assert_that(result[0]["ip"], equal_to("0.0.0.0"))
    assert_that(result[0]["user_agent"], equal_to("test_test"))
    assert_that(result[1]["ip"],equal_to("1.1.1.1"))
    assert_that(len(result), equal_to(2))


def test_get_all_visits_empty_list(mock_db):
    mock_cur = mock_db["mock_cur"]
    mock_cur.fetchall.return_value = []

    result = get_all_visits()

    assert_that(result, equal_to([])) #assert a empty list retured


def test_get_visit_by_id(mock_db):
    mock_cur = mock_db["mock_cur"]
    mock_cur.fetchone.return_value = (1,"2025-01-01T00:00:00Z", "0.0.0.0", "test_test")

    visit_id = 1

    result = get_visit_by_id(visit_id)

    #behavior assertion to check if funection has been called
    mock_cur.execute.assert_called_with('SELECT id, timestamp, ip, user_agent FROM visits WHERE id = %s', (visit_id,)) #visit_id is a turple， nso need to write liske 'visit_id,'
    
    assert_that(result["id"], equal_to(1))
    assert_that(result["ip"], equal_to("0.0.0.0"))
    assert_that(result["user_agent"], equal_to("test_test"))
    assert_that(result["timestamp"], equal_to("2025-01-01T00:00:00Z"))



def test_get_visit_by_none_id(mock_db):
    mock_cur = mock_db["mock_cur"]
    mock_cur.fetchone.return_value = None #mock that can't find the value in db 

    visit_id = 1

    result = get_visit_by_id(visit_id)
    mock_cur.execute.assert_called_with('SELECT id, timestamp, ip, user_agent FROM visits WHERE id = %s', (visit_id,))

    assert_that(result, equal_to(None))





    













