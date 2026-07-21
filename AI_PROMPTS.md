# AI Usage Documentation

## Prompt 1 – Architecture

Prompt:
Design the architecture for a full-stack seat allocation system using React, FastAPI, PostgreSQL and SQLAlchemy that satisfies the following requirements...

AI Output:
Suggested layered architecture using React frontend, FastAPI backend, SQLAlchemy ORM, PostgreSQL and REST APIs.

Manual Validation:
Compared architecture against assessment document.

Manual Changes:
Selected Vite instead of Next.js as both are permitted and Vite offers faster development for this assessment.

Verification:
Confirmed every required feature can be implemented within this architecture.

## Prompt 2 – Backend Initialization

Prompt:
Initialize a production-ready FastAPI backend for a seat allocation system using a modular folder structure. Include dependency recommendations and project organization, but avoid generating unnecessary files.

AI Output:
Suggested a modular FastAPI structure with separate folders for APIs, models, schemas, services, database configuration, and utilities.

Manual Validation:
Removed unnecessary folders and kept only the components required for the assessment.

Manual Changes:
Created only the folders needed at the current stage to keep the repository clean and maintainable.

Verification:
Successfully started the FastAPI server and verified the root endpoint and Swagger documentation.

## Prompt 3 – Database Configuration

Prompt:
Configure PostgreSQL, SQLAlchemy 2.0, Alembic, and environment variables for a FastAPI project. Follow production best practices while keeping the setup minimal for a CRUD application.

AI Output:
Suggested SQLAlchemy engine, session factory, declarative base, environment variable loading, and Alembic initialization.

Manual Validation:
Verified the database connection using a simple SQL query through SQLAlchemy.

Manual Changes:
Used SQLAlchemy 2.x compatible syntax (`text("SELECT 1")`) and kept the configuration minimal until models are introduced.

Verification:
Successfully connected FastAPI to PostgreSQL and confirmed connectivity through the `/health` endpoint.
