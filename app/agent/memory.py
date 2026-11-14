import json
import hashlib
from contextlib import contextmanager
from datetime import datetime
from sqlalchemy import text
from app.database.connection import engine


@contextmanager
def session_lock(session_id, timeout=10):
    """
    Acquire a MySQL named lock for this conversation.
    The lock is shared across application processes.
    """

    # MySQL lock names are limited to 64 characters.
    lock_hash = hashlib.sha256(
        session_id.encode("utf-8")
    ).hexdigest()[:48]

    lock_name = f"employee_agent_{lock_hash}"

    # Keep this connection open while holding the named lock.
    # Opening connection > Lock acquiring later
    connection = engine.connect()

    acquired = False

    print(f"[{datetime.now():%M:%S.%f}] Attempting to acquire session lock: {lock_name}")
    try:
        result = connection.execute(
            text("SELECT GET_LOCK(:lock_name, :timeout)"),
            {
                "lock_name": lock_name,
                "timeout": timeout
            }
        )

        # GET_LOCK() returns 1 means the lock was acquired, 0 means timeout, NULL means error
        acquired = result.scalar() == 1
        print(f"[{datetime.now():%M:%S.%f}] Session lock acquired: {acquired}")

        if not acquired:
            raise TimeoutError(
                f"Could not acquire session lock within {timeout} seconds."
            )

        yield

    finally:
        try:
            if acquired:
                connection.execute(
                    text("SELECT RELEASE_LOCK(:lock_name)"),
                    {"lock_name": lock_name}
                )
        finally:
            connection.close()

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

    with session_lock(session_id):
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

