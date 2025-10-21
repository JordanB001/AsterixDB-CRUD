from dotenv import load_dotenv
from os import getenv


load_dotenv()


### DATABASE ###
DATABASE_HOST: str = getenv("DATABASE_HOST")
DATABASE_PORT: str = getenv("DATABASE_PORT")




### TESTS ###
# DATABASE
if not DATABASE_HOST:
    raise RuntimeError("DATABASE_HOST environment variable is not set")
if not DATABASE_PORT:
    raise RuntimeError("DATABASE_PORT environment variable is not set")


