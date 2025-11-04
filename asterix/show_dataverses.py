from requests import Response
from asterix.utils import post_request


def show_dataverses() -> None:
    sqlpp_query: str = f"SELECT * FROM Metadata.`Dataverse`;"
    response: Response = post_request(sqlpp_query=sqlpp_query)

    response.raise_for_status()

    print("--- SHOW DATAVERSES ---")
    if response.json()["results"]:
        for dataverse in response.json()["results"]:
            print(dataverse["Dataverse"]["DataverseName"])
    else:
        print("None")
    print("-----------------------")

