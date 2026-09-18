from connect.connect_mongo import connect_mongodb
from utils.logger import logger


def save_commitments(commitments, connected_user_email):

    try:
        collection = connect_mongodb()

        if not commitments:
            logger.info("No commitments to save")
            return

        for commitment in commitments:

            commitment["user_email"] = connected_user_email
            commitment["type"] = "commitment"

            collection.update_one(
                {
                    "type": "commitment",
                    "user_email": connected_user_email,
                    "thread_id": commitment["thread_id"]
                },
                {
                    "$set": commitment
                },
                upsert=True
            )

        logger.info(f"processed {len(commitments)} commitments")

    except Exception as e:
        logger.error(f"failed to save commitments: {e}")
        raise

def save_calendar(commitment, event_id, event_link):

    try:
        collection = connect_mongodb()

        commitment["calendar"] = {
            "added": True,
            "event_id": event_id,
            "event_link": event_link
        }

        collection.update_one(
            {
                "type": "commitment",
                "user_email": commitment["user_email"],
                "thread_id": commitment["thread_id"]
            },
            {
                "$set": commitment
            },
            upsert=True
        )

        logger.info(f"calendar details saved for commitment: {commitment['thread_id']}")

    except Exception as e:
        logger.error(f"failed to save calendar details: {e}")
        raise