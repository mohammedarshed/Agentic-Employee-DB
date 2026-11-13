
# Stores conversations in application memory

conversation_store = {}


def get_conversation(session_id, system_prompt):

    # Check whether this session already exists
    if session_id not in conversation_store:

        conversation_store[session_id] = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

    return conversation_store[session_id]


def clear_conversation(session_id):

    if session_id in conversation_store:
        del conversation_store[session_id]

    print("Conversation memory cleared.")
