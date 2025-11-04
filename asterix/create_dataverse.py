from requests import Response
from asterix.drop_dataverse import drop_dataverse
from asterix.utils import post_request
from asterix.get_dataverse import get_dataverse


def create_dataverse(dataverse_name: str, recreate_dataverse: bool=False) -> bool:
    if not isinstance(dataverse_name, str):
        raise TypeError("dataverse_name must be a string")
    if dataverse_name.strip() == "":
        raise ValueError("dataverse_name cannot be empty or only whitespace")

    if not isinstance(recreate_dataverse, bool):
        raise TypeError("recreate_dataverse must be a boolean")

    # Drop dataverse for recreation
    if recreate_dataverse:
        drop_dataverse(dataverse_name=dataverse_name)

    # Create dataverse
    sqlpp_query: str = f"CREATE DATAVERSE {dataverse_name} IF NOT EXISTS;"
    response: Response = post_request(sqlpp_query=sqlpp_query)

    # Check if the dataverse was created
    if len(get_dataverse(dataverse_name=dataverse_name)) != 1:
        return False

    return True