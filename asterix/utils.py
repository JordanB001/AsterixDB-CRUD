from config import DATABASE_URL
from requests import post, Response


def post_request(sqlpp_query: str) -> Response:
    if not isinstance(sqlpp_query, str):
        raise TypeError("sqlpp_query must be a string")


    payload: dict = {
        "statement": sqlpp_query,
        "format": "json",
        "mode": "immediate"
    }
    headers: dict = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json"
    }

    response: Response = post(DATABASE_URL, data=payload, headers=headers)
    response.raise_for_status()
    
    return response