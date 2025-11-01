from config import DATABASE_URL
from requests import post, Response


def post_request(sqlpp_query: str) -> Response:
    if not isinstance(sqlpp_query, str):
        raise TypeError("sqlpp_query must be a string")


    payload: dict = {
        "query": sqlpp_query,
        "query-language": "SQL++",
        "output-format": "CLEAN_JSON",
        "plan-format": "JSON",
        "execute-query": "true"
    }
    headers: dict = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    response: Response = post(DATABASE_URL, data=payload, headers=headers)
    
    response.raise_for_status()
    return response