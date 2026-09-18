from email.utils import parsedate_to_datetime

from utils.logger import logger


def group_by_thread(emails):
    try:
        threads = {}

        for email in emails:
            thread_id = email.get("thread_id")

            if not thread_id:
                continue

            if thread_id not in threads:
                threads[thread_id] = {
                    "thread_id": thread_id,
                    "messages": []
                }

            threads[thread_id]["messages"].append(email)

        
        for thread in threads.values():
            thread["messages"].sort(
                key=lambda email: parsedate_to_datetime(email["date"])
            )

        logger.info(f"Grouped {len(emails)} emails into {len(threads)} threads")
        return list(threads.values())

    except Exception:
        logger.exception("Failed to group emails by thread")
        raise


def build_thread_text(thread):
    try:
        messages = []

        for index, email in enumerate(thread["messages"], start=1):

            direction = email.get("direction", "").upper()
            sender = (email.get("from") or "").strip()
            recipient = (email.get("to") or "").strip()
            date = (email.get("date") or "").strip()
            subject = (email.get("subject") or "").strip()
            body = (email.get("body") or "").strip()

            message_text = (
                f"===== MESSAGE {index} =====\n"
                f"Direction: {direction}\n"
                f"From: {sender}\n"
                f"To: {recipient}\n"
                f"Date: {date}\n"
                f"Subject: {subject}\n\n"
                f"{body}"
            )

            messages.append(message_text)

        logger.info(
            f"Built conversation text for thread: {thread.get('thread_id')}"
        )

        return "\n\n".join(messages)

    except Exception:
        logger.exception(
            f"Failed to build thread text: {thread.get('thread_id')}"
        )
        raise