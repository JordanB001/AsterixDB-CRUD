from asterix.utils import post_request
from requests import Response


def create_dataverse(dataverse_name: str) -> bool:
    if not isinstance(dataverse_name, str):
        raise TypeError("dataverse_name must be a string")
    if dataverse_name.strip() == "":
        raise ValueError("dataverse_name cannot be empty or only whitespace")

    sqlpp_query: str = f"CREATE DATAVERSE {dataverse_name} IF NOT EXISTS;"

    response: Response = post_request(sqlpp_query=sqlpp_query)
    
    # Check if the DATAVERSE was created




    
    return True   
