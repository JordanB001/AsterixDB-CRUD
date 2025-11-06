from requests import Response, Session, post


class Asterixdb:
    def __init__(self, database_host: str, database_port: str, pretty: bool=False, dataverse: str="Default", client_context_id: str | None=None, mode: str="immediate", readonly: bool=False) -> None:
        if not isinstance(database_host, str):
            raise TypeError("database_host must be a string")
        
        if not isinstance(database_port, str):
            raise TypeError("database_port must be a string")

        if not isinstance(pretty, bool):
            raise TypeError("pretty must be a boolean")

        if not isinstance(dataverse, str):
            raise TypeError("dataverse must be a string")

        if client_context_id is not None and not isinstance(client_context_id, str):
            raise TypeError("client_context_id must be a string or None")

        if not isinstance(mode, str):
            raise TypeError("mode must be a string")
        if mode not in ["immediate", "deferred", "async"]:
            raise ValueError("mode must be one of: 'immediate', 'deferred', or 'async'")

        if not isinstance(readonly, bool):
            raise TypeError("readonly must be a boolean")


        # Session parameters
        self.database_url: str = f"http://{database_host}:{database_port}/query/service"
        self.connexion: Session = self.asterixdb_connexion()


        # Payload parameters
        self.payload: dict = {
            "pretty": "true" if pretty else "false",
            "dataverse": dataverse,
            "mode": mode,
            "readonly": "true" if readonly else "false"
        }

        if client_context_id:
            self.payload["client_context_id"] = client_context_id


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


        self.payload["statement"] = sqlpp_query
        
        response: Response = self.connexion.post(self.database_url, data=self.payload)
        response.raise_for_status()
        
        return response


    def use_dataverse(self, dataverse_name: str) -> bool:
        if not isinstance(dataverse_name, str):
            raise TypeError("dataverse_name must be a string")

        # Check if dataverse exist
        if len(self.get_dataverse(dataverse_name=dataverse_name)) != 1:
            print(f"Dataverse {dataverse_name} don't exists")
            return False

        self.payload["dataverse"] = dataverse_name

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

