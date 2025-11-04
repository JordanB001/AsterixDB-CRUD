from asterix.utils import post_request
from requests import Response


def get_dataverses() -> list[dict]:
    sqlpp_query: str = f"SELECT * FROM Metadata.`Dataverse`;"
    response: Response = post_request(sqlpp_query=sqlpp_query)

    response.raise_for_status()

    return response.json()["results"]