from connect.connect_mongo import connect_mongodb
from utils.logger import logger


def delete_all_commitments():

    try:
        collection = connect_mongodb()

        result = collection.delete_many({})

        logger.info(
            f"Deleted {result.deleted_count} commitments from MongoDB"
        )

        print(
            f"Deleted {result.deleted_count} commitments from MongoDB"
        )

    except Exception as e:
        logger.error(f"Failed to delete MongoDB data: {e}")
        raise


if __name__ == "__main__":
    delete_all_commitments()