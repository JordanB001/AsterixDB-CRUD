from asterix.utils import post_request
from requests import Response


def get_dataverse(dataverse_name: str) -> dict:
    if not isinstance(dataverse_name, str):
        raise TypeError("dataverse_name must be a string")


    sqlpp_query: str = f"SELECT * FROM Metadata.`Dataverse` WHERE `Dataverse`.DataverseName = '{dataverse_name}';"
    response: Response = post_request(sqlpp_query=sqlpp_query)

    response.raise_for_status()

    return response.json()["results"]