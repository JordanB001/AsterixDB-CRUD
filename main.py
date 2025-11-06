from asterix.asterixdb import Asterixdb
from config import DATABASE_HOST, DATABASE_PORT, DATAVERSE


if __name__ == "__main__":
    dataverse_name: str = "Dataverse_CRUD"
    asterix: Asterixdb = Asterixdb(database_host=DATABASE_HOST, database_port=DATABASE_PORT)

    results: list[dict] = asterix.display_dataverses()
    
    

