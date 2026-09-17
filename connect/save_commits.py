from connect.connect_mongo import connect_mongodb
from utils.logger import logger


def save_commitments(commitments):

    try:
        collection = connect_mongodb()

        if not commitments:
            logger.info("No commitments to save")
            return

        # result = collection.insert_many(commitments)
        commitments_to_save = [commitment.copy() for commitment in commitments]

        result = collection.insert_many(commitments_to_save)

        logger.info(
            f"Saved {len(result.inserted_ids)} commitments to MongoDB"
        )

        print(
            f"Saved {len(result.inserted_ids)} commitments to MongoDB"
        )

    except Exception as e:
        logger.error(f"Failed to save commitments: {e}")
        raise