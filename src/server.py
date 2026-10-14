# =============================================================================
# IMPORTS
# =============================================================================
from datetime import UTC, datetime

import requests
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

# =============================================================================
# MACROS
# =============================================================================

app = Flask(__name__)
votd_cache = {}
versions_cache = {}



# =============================================================================
# ERROR HANDLING AND VALIDATION
# =============================================================================
class APIError(HTTPException):
    def __init__(self, status, error_code, message):
        super().__init__(description=message)
        self.code = status
        self.error_code = error_code


def handle_http_error(error):
    response = error.get_response()
    code = error.error_code if isinstance(error, APIError) else error.name.upper().replace(" ", "_")
    
    response.set_data(jsonify({"error": {
        "code": code,
        "message": error.description
    }}).get_data())
    response.content_type = "application/json"
    return response


app.register_error_handler(HTTPException, handle_http_error)


def validate_day(day):
    day = day.isascii() and day.isdecimal() and 1 <= int(day) <= 366
    if not day:
        raise APIError(400, "INVALID_DAY", "day must be an integer between 1 and 366")


def validate_version(version):
    version = version.isascii() and version.isdecimal()
    if not version:
        raise APIError(400, "INVALID_VERSION", "version must be an integer")


def require_fields(data, fields):
    if not isinstance(data, dict) or any(
        not isinstance(data.get(field), expected_type)
        for field, expected_type in fields.items()
    ):
        raise APIError(502, "UPSTREAM_ERROR", "YouVersion returned an unexpected response")



# =============================================================================
# API CALLS
# =============================================================================
def call_youversion_api(endpoint):
    try:
        response = requests.get(
            f"https://api.youversion.com{endpoint}",
            headers={
                "x-yvp-app-key": "1gqBksQ6ec6GdOCCDfMrmyV6x5UlZGDWSkLxmCTWjGgrg5hm"
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        raise APIError(502, "UPSTREAM_ERROR", "Unable to retrieve data from YouVersion") from None



# =============================================================================
# ROUTES
# =============================================================================
@app.route("/votd")
def home():
    day = str(datetime.now(UTC).timetuple().tm_yday)
    day = request.args.get("day", day)
    validate_day(day)
    version = request.args.get("version", "")
    validate_version(version)
    day = int(day)
    version = int(version)
    cache_key = (day, version)
    if cache_key in votd_cache:
        return votd_cache[cache_key]

    votd = call_youversion_api(f"/v1/verse_of_the_days/{day}")
    require_fields(votd, {"passage_id": str})
    passage_id = votd["passage_id"]
    
    passage = call_youversion_api(
        f"/v1/bibles/{version}/passages/{passage_id}?format=text"
    )
    require_fields(passage, {"reference": str, "content": str})

    response = {
        "day": day,
        "reference": passage["reference"],
        "text": passage["content"],
        "version_id": version
    }
    votd_cache[cache_key] = response
    return response


@app.route("/versions")
def versions():
    cache_key = "en*"
    if cache_key in versions_cache:
        return versions_cache[cache_key]

    response = call_youversion_api("/v1/bibles?language_ranges[]=en*")
    require_fields(response, {"data": list})
    for bible in response["data"]:
        require_fields(bible, {"id": int, "abbreviation": str, "title": str})

    response = [
        {
            "id": bible["id"],
            "abbreviation": bible["abbreviation"],
            "title": bible["title"]
        }
        for bible in response["data"]
    ]
    versions_cache[cache_key] = response
    return response
