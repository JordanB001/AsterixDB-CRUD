from requests import Response, Session, post


class Asterixdb:
    def __init__(self, database_host: str, database_port: str) -> None:
        if not isinstance(database_host, str):
            raise TypeError("database_host must be a string")
        
        if not isinstance(database_port, str):
            raise TypeError("database_port must be a string")


        self.database_url: str = f"http://{database_host}:{database_port}/query/service"
        self.dataverse: str = ""

        self.connexion: Session = self.asterixdb_connexion()


    def asterixdb_connexion(self) -> Session:
        connexion: Session = Session()

        headers: dict = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json"
        }

        connexion.headers.update(headers)
        return connexion



    def post_request(self, sqlpp_query: str) -> Response:
        if not isinstance(sqlpp_query, str):
            raise TypeError("sqlpp_query must be a string")


        payload: dict = {
            "statement": sqlpp_query,
            "format": "json",
            "mode": "immediate"
        }

        response: Response = self.connexion.post(self.database_url, data=payload)
        response.raise_for_status()
        
        return response


    def use_dataverse(self, dataverse_name: str) -> bool:
        if not isinstance(dataverse_name, str):
            raise TypeError("dataverse_name must be a string")

        # Check if dataverse exist
        if len(self.get_dataverse(dataverse_name=dataverse_name)) != 1:
            print(f"Dataverse {dataverse_name} don't exists")
            return False

        sqlpp_query: str = f"USE {dataverse_name}"
        response: Response = self.post_request(sqlpp_query=sqlpp_query)

        if response.json()["status"] != "success":
            return False

        return True


    def display_dataverses(self) -> None:
        sqlpp_query: str = f"SELECT * FROM Metadata.`Dataverse`;"
        response: Response = self.post_request(sqlpp_query=sqlpp_query)

        print("--- SHOW DATAVERSES ---")
        if response.json()["results"]:
            for dataverse in response.json()["results"]:
                print(dataverse["Dataverse"]["DataverseName"])
        else:
            print("None")
        print("-----------------------")


    def get_dataverses(self) -> list[dict]:
        sqlpp_query: str = f"SELECT * FROM Metadata.`Dataverse`;"
        response: Response = self.post_request(sqlpp_query=sqlpp_query)

        response.raise_for_status()

        return response.json()["results"]


    def get_dataverse(self, dataverse_name: str) -> list[dict]:
        if not isinstance(dataverse_name, str):
            raise TypeError("dataverse_name must be a string")


        sqlpp_query: str = f"SELECT * FROM Metadata.`Dataverse` WHERE `Dataverse`.DataverseName = '{dataverse_name}';"
        response: Response = self.post_request(sqlpp_query=sqlpp_query)

        response.raise_for_status()

        return response.json()["results"]
    

    def create_dataverse(self, dataverse_name: str, recreate_dataverse: bool=False) -> bool:
        if not isinstance(dataverse_name, str):
            raise TypeError("dataverse_name must be a string")
        if dataverse_name.strip() == "":
            raise ValueError("dataverse_name cannot be empty or only whitespace")

        if not isinstance(recreate_dataverse, bool):
            raise TypeError("recreate_dataverse must be a boolean")

        # Drop dataverse for recreation
        if recreate_dataverse:
            self.drop_dataverse(dataverse_name=dataverse_name)

        # Create dataverse
        sqlpp_query: str = f"CREATE DATAVERSE {dataverse_name} IF NOT EXISTS;"
        response: Response = self.post_request(sqlpp_query=sqlpp_query)

        # Check if the dataverse was created
        if len(self.get_dataverse(dataverse_name=dataverse_name)) != 1:
            return False

        return True
    

    def drop_dataverse(self, dataverse_name: str) -> bool:
        if not isinstance(dataverse_name, str):
            raise TypeError("dataverse_name must be a string")


        sqlpp_query: str = f"DROP DATAVERSE {dataverse_name} IF EXISTS;"
        response: Response = self.post_request(sqlpp_query=sqlpp_query)

        return True

