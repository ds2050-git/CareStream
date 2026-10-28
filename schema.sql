CREATE TABLE users(
user_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
username VARCHAR2(50) UNIQUE NOT NULL,
role VARCHAR2(20) NOT NULL,
status VARCHAR2(10) DEFAULT 'ACTIVE'
);

CREATE TABLE care_tasks(
task_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
encounter_id NUMBER NOT NULL,
assigned_role VARCHAR2(20) NOT NULL,
task_description VARCHAR2(200) NOT NULL,
status VARCHAR2(20) DEFAULT 'PENDING',
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs(
log_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
user_id NUMBER NOT NULL,
action_type VARCHAR2(50) NOT NULL,
entity_name VARCHAR2(50) NOT NULL,
entity_id NUMBER NOT NULL,
action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
CONSTRAINT fk_audit_user FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_task_enc_status ON care_tasks(encounter_id,status);
CREATE INDEX idx_audit_user_action ON audit_logs(user_id,action_type);