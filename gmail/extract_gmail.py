import base64
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from utils.logger import logger


def extract_email(service):
    try:
        logger.info("Starting email extraction")

        today = datetime.now().date()
        five_days_ago = today - timedelta(days=5)
        tomorrow = today + timedelta(days=1)

        query = (
            f"after:{five_days_ago} "
            f"before:{tomorrow} "
            "category:primary"
        )

        inbox_messages = service.users().messages().list(
            userId="me",
            labelIds=["INBOX"],
            q=query,
            maxResults=5
        ).execute().get("messages", [])

        sent_messages = service.users().messages().list(
            userId="me",
            labelIds=["SENT"],
            maxResults=5
        ).execute().get("messages", [])

        logger.info(
            f"Found {len(inbox_messages)} inbox and "
            f"{len(sent_messages)} sent messages"
        )

        emails = []

        for message in inbox_messages:
            email = extract_header(service, message["id"])
            email["direction"] = "received"
            emails.append(email)

        for message in sent_messages:
            email = extract_header(service, message["id"])
            email["direction"] = "sent"
            emails.append(email)

        logger.info(f"Email extraction completed: {len(emails)} emails")

        return emails

    except Exception:
        logger.exception("Failed to extract emails")
        raise


def extract_header(service, message_id):
    try:
        message = service.users().messages().get(
            userId="me",
            id=message_id,
            format="full"
        ).execute()

        headers = message.get("payload", {}).get("headers", [])

        email_data = {
            "message_id": message_id,
            "thread_id": message.get("threadId"),
            "from": None,
            "to": None,
            "subject": None,
            "date": None,
            "body": None
        }

        for header in headers:
            name = header.get("name")
            value = header.get("value")

            if name == "From":
                email_data["from"] = value
            elif name == "To":
                email_data["to"] = value
            elif name == "Subject":
                email_data["subject"] = value
            elif name == "Date":
                email_data["date"] = value

        email_data["body"] = extract_body(
            message.get("payload", {})
        )

        return email_data

    except Exception:
        logger.exception(
            f"Failed to extract email: {message_id}"
        )
        raise


def extract_body(payload):
    try:
        body_data = payload.get("body", {}).get("data")

        if body_data:
            return base64.urlsafe_b64decode(
                body_data
            ).decode("utf-8", errors="replace")

        parts = payload.get("parts", [])

        plain_text = None
        html_text = None

        for part in parts:
            mime_type = part.get("mimeType", "")

            if part.get("parts"):
                nested_body = extract_body(part)

                if nested_body:
                    return nested_body

            part_body = part.get("body", {}).get("data")

            if not part_body:
                continue

            decoded_body = base64.urlsafe_b64decode(
                part_body
            ).decode("utf-8", errors="replace")

            if mime_type == "text/plain":
                plain_text = decoded_body

            elif mime_type == "text/html":
                html_text = decoded_body

        if plain_text and plain_text.strip() != "Please Enable HTML":
            return plain_text.strip()

        if html_text:
            return html_to_text(html_text)

        return "No readable body found."

    except Exception:
        logger.exception("Failed to extract email body")
        raise


def html_to_text(html):
    try:
        soup = BeautifulSoup(html, "html.parser")

        for element in soup(["script", "style"]):
            element.decompose()

        text = soup.get_text(separator="\n")

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        return "\n".join(lines)

    except Exception:
        logger.exception("Failed to convert HTML to text")
        raise


def create_semantic_text(email):
    try:
        subject = (email.get("subject") or "").strip()
        body = (email.get("body") or "").strip()

        return f"""Subject: {subject}

            Body:
            {body}""".strip()

    except Exception:
        logger.exception("Failed to create semantic text")
        raise