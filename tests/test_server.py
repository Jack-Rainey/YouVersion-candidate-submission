import sys
from pathlib import Path
from unittest.mock import Mock, patch

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import server


def test_happy_path():
    client = server.app.test_client()
    calendar = Mock()
    calendar.json.return_value = {"passage_id": "REV.3.20"}
    passage = Mock()
    passage.json.return_value = {
        "reference": "Revelation 3:20", "content": "Test verse text"
    }
    with patch.dict(server.votd_cache, {}, clear=True), patch("src.server.requests.get", side_effect=[calendar, passage]):
        response = client.get("/votd?day=195&version=206")
    assert response.status_code == 200
    assert response.get_json() == {
        "day": 195, "reference": "Revelation 3:20",
        "text": "Test verse text", "version_id": 206
    }

def test_invalid_day():
    client = server.app.test_client()
    with patch.dict(server.votd_cache, {}, clear=True), patch("src.server.requests.get") as upstream:
        response = client.get("/votd?day=0&version=206")
    upstream.assert_not_called()
    assert response.status_code == 400
    assert response.get_json() == {"error": {
        "code": "INVALID_DAY",
        "message": "day must be an integer between 1 and 366"
    }}

def test_timeout():
    client = server.app.test_client()
    with patch.dict(server.votd_cache, {}, clear=True), patch("src.server.requests.get", side_effect=requests.Timeout):
        response = client.get("/votd?day=195&version=206")
    assert response.status_code == 502
    assert response.get_json() == {"error": {
        "code": "UPSTREAM_ERROR",
        "message": "Unable to retrieve data from YouVersion"
    }}


if __name__ == "__main__":
    for test in (test_happy_path, test_invalid_day, test_timeout):
        test()
        print(f"{test.__name__}: passed")
