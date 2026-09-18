import os
from pymongo import MongoClient
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()


def connect_mongodb():

    try:
        logger.info("Starting connection with MongoDB")

        url = os.getenv("MONGODB_URI")

        if not url:
            raise ValueError("MONGODB_URI is not set in .env")

        conn = MongoClient(url)

        
        conn.admin.command("ping")

        logger.info("Connected to MongoDB successfully")

        db = conn[os.getenv("DATABASE_NAME")]
        collection = db[os.getenv("COLLECTION_NAME")]

        # print("DB:",db)
        # print("collection", collection)
        
        logger.info(f"Connected to database: {db.name}")
        logger.info(f"Using collection: {collection.name}")

        logger.info(f"Connected to database: {db.name}")
        logger.info(f"Using collection: {collection.name}")

        return collection

    except Exception as e:

        logger.error(f"Failed to connect to MongoDB: {e}")

        raise


if __name__ == "__main__":

    collection = connect_mongodb()
        