from connect.connect_mongo import connect_mongodb
from utils.logger import logger


def delete_all_commitments():

    try:
        collection = connect_mongodb()

        result = collection.delete_many({})

        logger.info(f"deleted {result.deleted_count} commitments from mongodb")

        print(f"deleted {result.deleted_count} commitments from mongodb")

    except Exception as e:
        logger.error(f"failed to delete Mongodb data: {e}")
        raise


if __name__ == "__main__":
    delete_all_commitments()