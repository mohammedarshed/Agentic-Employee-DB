USE employee_db;

-- Stores individual conversation sessions
CREATE TABLE conversations (
    session_id VARCHAR(36) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

-- Stores individual messages in each conversation
CREATE TABLE conversation_messages (
    message_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    message_json LONGTEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id)
        REFERENCES conversations(session_id)
        ON DELETE CASCADE,

    INDEX idx_session_messages (session_id, message_id)
);
