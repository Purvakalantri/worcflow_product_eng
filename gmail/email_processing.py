from graph.intent_classifier import classify_intent, extract_data
from gmail.group_threads import build_thread_text
from utils.logger import logger
import json


def process_emails(threads, connected_user_email):

    commitments = []

    try:
        logger.info(f"Started processing {len(threads)} email threads")

        for thread in threads:

            thread_id = thread.get("thread_id")

            logger.info(f"Processing thread: {thread_id}")

            conversation = build_thread_text(thread)

            logger.info(f"Classifying thread: {thread_id}")

            result = classify_intent(
                conversation,
                connected_user_email
            )

            print("\n==============================")
            print("Thread ID:", thread_id)
            print("Messages:", len(thread["messages"]))
            print("Intent:", result)
            print("convo:", conversation)

            result = json.loads(result)

            if result["has_commitment"] is True:

                logger.info(
                    f"Commitment found in thread: {thread_id}"
                )

                data = extract_data(
                    conversation,
                    connected_user_email
                )

                data = json.loads(data)

                print("\nCOMMITMENT:")
                print(data)

                if data["status"] == "fulfilled":

                    logger.info(
                        f"Fulfilled commitment ignored: {thread_id}"
                    )

                    continue

                data["thread_id"] = thread_id

                commitments.append(data)

                logger.info(
                    f"Active commitment added: {thread_id}"
                )

        logger.info(
            f"Email processing completed. "
            f"Active commitments found: {len(commitments)}"
        )

        return commitments

    except Exception as e:

        logger.error(
            f"Failed while processing emails: {e}"
        )

        raise