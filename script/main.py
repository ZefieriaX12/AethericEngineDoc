import getpass
from  connector import DataFetch
from database.InitDb import initDB

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    initDB(dropTables=True)

    numberOfMessage = 600

    host = getpass.getpass("Enter Host: ")
    port = int(getpass.getpass("Enter Port: "))
    jwt = getpass.getpass("Enter JWT Token: ")

    logger.info("Start Fetching")
    DataFetch.fetchStoreData(host, port, jwt, numberOfMessage)

if __name__ == "__main__":
    main()