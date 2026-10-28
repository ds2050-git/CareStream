# CareStream

CareStream is a lightweight, role-based clinical workflow and audit engine built to handle task assignments, role permissions, and full action audit logging across healthcare teams.

## Tech Stack
* Language: Python 3.10+
* Database: Relational SQL
* Testing Framework: Python `unittest`

## Repository Structure
```text
.
├── schema.sql           # Database schema, RBAC tables, and audit log tracking
├── workflow.py          # Workflow engine class, state transitions, and audit logging
├── test_workflow.py     # Automated unit test suite
```

## Core Features
* Role-Based Task Execution: Managed workflow state transitions (`PENDING`, `COMPLETED`) tied strictly to user roles and authorization.
* Automated Audit Logging: Every task creation and status change automatically generates an immutable audit record for traceability.
* Performance Indexing: Optimized composite indexes on frequent lookup fields (`encounter_id`, `status`, `user_id`, `action_type`).
* Unit Testing Coverage: Comprehensive unit tests using Python's `unittest` framework to verify permission constraints and audit accuracy.

## Quick Start

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ds2050-git/CareStream.git
   cd CareStream
   ```

### Running Unit Tests
To execute the automated unit test suite:
```bash
python test_workflow.py
```
