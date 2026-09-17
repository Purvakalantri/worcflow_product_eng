from langgraph.graph import StateGraph, START, END

from gmail.extract_gmail import extract_email
from basemodel import WorkflowState
from connect.connect_gmail import connect_gmail
from utils.logger import logger
from gmail.group_threads import group_by_thread
from gmail.email_processing import process_emails
from connect.save_commits import save_commitments


def gmail_ingestion_node(state):

    try:
        logger.info("Gmail ingestion started")

        print("Heyy inside gmail ingestion node")

        service, connected_user_email = connect_gmail()

        print("connected_user_profile", connected_user_email)
        print("Service from gmail ingestion pipeline", service)

        emails = extract_email(service)

        threads = group_by_thread(emails)

        commitments = process_emails(
            threads,
            connected_user_email
        )

        # print("processing_emails", processing_emails)

        # print("Total emails:", len(emails))
        # print("Total threads:", len(threads))

        # for thread in threads[:1]:

        #     print("\n==============================")
        #     print("Thread ID:", thread["thread_id"])
        #     print("Messages:", len(thread["messages"]))

        #     conversation = build_thread_text(thread)

        #     print("\ntHE CONVERSATION HERE IS: ", conversation)

        # threads = group_by_thread(emails)

        logger.info(
            f"Gmail ingestion completed: {len(emails)} emails"
        )

        return {
            "gmail_service": service,
            "messages": emails,
            "threads": threads,
            "commitments": commitments,
            "connected_user_email": connected_user_email
        }

    except Exception as e:
        logger.error(f"Gmail ingestion failed: {e}")
        raise


# def thread_grouping_node(state):

#     logger.info("Grouping emails by thread")

#     emails = state["messages"]

#     threads = group_by_thread(emails)

#     logger.info(f"Created {len(threads)} threads")

#     return {
#         "threads": threads
#     }


def save_commitments_node(state):

    try:
        logger.info("Saving commitments to MongoDB")

        commitments = state.get("commitments", [])

        save_commitments(commitments)

        logger.info("Commitments saved to MongoDB")

        return {}

    except Exception as e:
        logger.error(f"Failed to save commitments: {e}")
        raise


def create_graph():

    try:
        logger.info("Creating LangGraph workflow")

        graph = StateGraph(WorkflowState)

        graph.add_node("gmail_ingestion", gmail_ingestion_node)
        graph.add_node("save_commitments", save_commitments_node)

        graph.add_edge(START, "gmail_ingestion")
        graph.add_edge("gmail_ingestion", "save_commitments")
        graph.add_edge("save_commitments", END)

        workflow = graph.compile()

        logger.info("LangGraph workflow compiled successfully")

        return workflow

    except Exception as e:
        logger.error(f"Failed to create LangGraph workflow: {e}")
        raise


if __name__ == "__main__":

    workflow = create_graph()

    result = workflow.invoke({})

    

    

    