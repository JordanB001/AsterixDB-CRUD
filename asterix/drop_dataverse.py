from requests import Response
from asterix.utils import post_request


def drop_dataverse(dataverse_name: str) -> bool:
    if not isinstance(dataverse_name, str):
        raise TypeError("dataverse_name must be a string")


    sqlpp_query: str = f"DROP DATAVERSE {dataverse_name} IF EXISTS;"
    response: Response = post_request(sqlpp_query=sqlpp_query)

    return True
