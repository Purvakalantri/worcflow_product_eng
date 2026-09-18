from connect.connect_calendar import connect_calendar
from utils.logger import logger
from datetime import datetime, timedelta

def add_calendar_event(task, due_date, recipient_email, user_email, requirements=None):

    try:
        service = connect_calendar()

        event = {
            "summary": task,
            "description": (
                f"To: {recipient_email}\n\n"
                f"Requirements:\n" + "\n".join(requirements or [])
            ),
            "start": {
                "date": due_date
            },
            "end": {
                    "date": (datetime.strptime(due_date, "%Y-%m-%d").date() +
                     timedelta(days=1)).isoformat()
                },
            "attendees": [
                    {
                        "email": recipient_email
                    }
            ]
        }

        created_event = service.events().insert(
            calendarId="primary",
            body=event
        ).execute()

        # print("Created_Event",created_event)

        logger.info(f"Calendar event created: {task}")

        return {
            "event_id": created_event["id"],
            "event_link": created_event["htmlLink"]
        }

    except Exception:
        logger.exception("Failed to create calendar event")
        raise