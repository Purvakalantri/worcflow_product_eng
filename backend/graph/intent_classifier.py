from openai import OpenAI
from dotenv import load_dotenv
import os
from utils.logger import logger

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def classify_intent(conversation, connected_user_email):
   
    try:
        logger.info("Starting intent classification")

        prompt = f"""
        You are an intent classifier for a commitment tracking system.

        Classify the conversation into one primary intent:
        commitment, conversation, promotional, notification, transactional, or other.

        The main goal is to identify commitments made BY the connected user.

        A commitment exists only when the connected user has agreed to, promised to,
        or taken responsibility for completing an action for another person.

        An action requested FROM the connected user is not a commitment by itself.
        If another person asks the connected user to do something and the connected
        user has not agreed to do it, classify it as conversation.

        Use the full conversation and identify who is speaking using the email addresses.

        Return only valid JSON:
        {{"intent": "...", "has_commitment": true/false}}

        Connected user: {connected_user_email}

        Conversation:
        {conversation}
        """

        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise email intent classifier. "
                        "Return only valid JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )

        result = response.choices[0].message.content
        # print(result)

        logger.info("Intent classification completed")

        return result

    except Exception as e:
        logger.error(f"Intent classification failed: {e}")
        raise


def extract_data(conversation, connected_user_email):
    try:
        logger.info("Extracting commitment details")

        prompt = f"""
            Extract the commitment made by the connected user from the conversation.

            Extract:
            - recipient_name
            - recipient_email
            - task
            - due_date
            - requirements
            - status

            Use only information present in the conversation.
            Use null when a field is unavailable.
            For requirements, return a list.
            Set status to "fulfilled" if the commitment has already been completed,
            otherwise set it to "outstanding".

            Return only valid JSON.

            Connected User: {connected_user_email}

            Conversation:
            {conversation}
            """

        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You extract commitment details from email conversations. "
                        "Return only valid JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )

        result = response.choices[0].message.content

        # print("EXTRACTED DATA:", result)

        logger.info("Commitment details extracted")

        return result

    except Exception as e:
        print("Can't extract commitment details:", e)
        logger.error(f"Can't extract commitment details: {e}")
        raise


if __name__ == "__main__":

    test_email = {
        "subject": "Re: Re: Re: project thing",
        "body": """
        Hi,

        Sorry completely missed this yesterday.

        Regarding what we discussed — yes, I'll do it. I should be able
        to get it to you by Friday, although if the numbers from finance
        don't come through today it might slip a little.

        The other thing you mentioned about the meeting, let's just keep
        that for next week.

        Also I think Neha already sent the previous version? If not I can
        forward it.

        Anyway don't worry about the formatting, just send me whatever
        you have.

        Thanks,
        Purva
        """
    }

    result = classify_intent(
        test_email["body"],
        "purva@example.com"
    )


    print(result)