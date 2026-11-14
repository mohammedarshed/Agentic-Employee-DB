import json

from sqlalchemy import text
from app.database.connection import engine

# Stores conversations in application memory

conversation_store = {}


def get_conversation(session_id, system_prompt):

    # Create session if it doesn't exist
    with engine.begin() as connection:

        #Inserts if session_id doesn't exist, if exists, it doesn't insert & continues execution
        connection.execute(
            text("""
                INSERT IGNORE INTO conversations (session_id)
                VALUES (:session_id)
            """),
            {"session_id": session_id}
        )
        
        """
        INSERT IGNORE means:
        - If the session doesn't exist, insert it.
        - If it already exists, don't insert a duplicate.
        - Continue execution without throwing a duplicate-key error.
        It does not retrieve conversation history.
        """

        # Retrieve previous messages
        result = connection.execute(
            text("""
                SELECT message_json
                FROM conversation_messages
                WHERE session_id = :session_id
                ORDER BY message_id
            """),
            {"session_id": session_id}
        )

        stored_messages = result.scalars().all()

    # Reconstruct conversation history
    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    for message in stored_messages:
        messages.append(json.loads(message))

    return messages

def save_message(session_id, message):

    message_json = json.dumps(
        message,
        default=str
    )

    with engine.begin() as connection:

        connection.execute(
            text("""
                INSERT INTO conversation_messages
                (session_id, message_json)
                VALUES (:session_id, :message_json)
            """),
            {
                "session_id": session_id,
                "message_json": message_json
            }
        )


def clear_conversation(session_id):

    with engine.begin() as connection:

        #cascading delete set in DB
        connection.execute(
            text("""
                DELETE FROM conversations
                WHERE session_id = :session_id
            """),
            {"session_id": session_id}
        )

    print("Conversation memory cleared.")

