# LLM Assistant Guidelines

This document outlines the rules and workflow for Large Language Model (LLM) assistants contributing to this project. Adherence to these guidelines is mandatory.

## Rule 1: Code Modification Protocol

> **IMPORTANT:** You MUST NOT modify any code in this project unless you receive a direct and explicit instruction to do so.

### Clarifications:

*   **No Implied Instructions:** Do not interpret conversational cues, suggestions, or discussions as instructions to write or change code.
*   **Suggestions vs. Actions:** If you identify a potential code change during a conversation, you should propose it as a suggestion to the developer. You are not permitted to implement the change yourself without explicit approval.
*   **Direct Command Required:** A direct instruction will be unambiguous, for example: "Please change the `playerSpeed` variable to `200` in `player.py`" or "Go ahead and implement the changes we just discussed."

This rule is in place to ensure the developer maintains full control over the codebase and that all changes are deliberate and well-considered.

## Rule 2: LLM Assistant Workflow Guide

This document outlines the specific workflow to be followed by the LLM assistant when collaborating on this project. The goal is to ensure a sequential, incremental, and review-driven process.

### Core Principles

1.  **Sequential Execution:** The assistant must follow the steps outlined in a `plan` document in the exact order they are presented. Do not skip steps or work on multiple items simultaneously.
2.  **Incremental Changes:** Each step (or sub-item) in the plan should be treated as a single, atomic unit of work. The assistant will make only the changes required to complete that specific item.
3.  **Halt and Report:** After completing the work for a single sub-item, the assistant must **halt** all further code modifications. It will then report back, indicating which specific sub-item has been completed.
4.  **Await Review and Instruction:** The assistant will remain in a waiting state after reporting completion. It will only proceed to the next sub-item after receiving an explicit instruction to do so from the user. The user will specify which sub-item to work on next.
5.  **Clarification on Completed Steps:** If the user instructs the assistant to perform a step that has already been completed, the assistant will not proceed. Instead, it will inform the user that the step is already done and ask for clarification on which step to take next.

## Example Workflow

1.  **User:** "Please proceed with sub-item 1a from the plan."
2.  **Assistant:** *(Performs the actions for sub-item 1a)*
3.  **Assistant:** "I have completed sub-item 1a. I am now awaiting your review and further instructions."
4.  **User:** *Reviews the changes.*
5.  **User:** "Looks good. Please proceed with sub-item 1b."
6.  **Assistant:** *...and so on.*

# Planning & Task Sequencing Principles

This section outlines the rules for how planning documents should be structured to ensure an efficient, testable, and incremental development workflow.

## Rule 3: The Principle of Vertical Slicing & Immediate Testability

> **IMPORTANT:** Plans MUST be structured as granular, end-to-end "vertical slices" of functionality. Each step must result in a small, immediately verifiable change. Avoid planning broad, horizontal layers of interdependent code that cannot be tested until all layers are complete.

### Clarifications:

*   **Build Just-In-Time:** Do not plan to build an entire abstract system (e.g., a complete data access layer, a full state management store, a comprehensive set of UI components) before it is needed. Instead, build only the specific methods, state variables, or components required for the immediate user-facing feature being implemented.
*   **Ensure Immediate Feedback:** Each task, or a very small group of tasks, should result in a testable outcome. This creates a tight feedback loop to catch errors early. A testable outcome can be:
    *   A visible UI change that renders correctly.
    *   A verifiable print statement from a backend function.
    *   A specific database record being created or updated.
    *   A component that appears or disappears based on a state change.
*   **Follow the Data Flow:** When planning features, the task sequence should follow the flow of data and user interaction. For a user-facing feature, this often means starting with the UI and progressively building out the backend logic that supports it. This aligns the automated development process with the natural, iterative way a human developer works.

### Example: Planning a Sign-Up Form

#### **INCORRECT (Horizontal Layers - AVOID THIS):**

1.  **Plan A:** Build the entire data access layer for all user operations (create, read, update, delete).
2.  **Plan B:** Build the entire validation layer with all Zod schemas for all user-related forms.
3.  **Plan C:** Build the static UI for the sign-up form.
4.  **Plan D:** Connect the UI to the validation and data layers.

*   **Problem:** The work in Plan A and B is abstract and untestable until Plan D. Errors made in these foundational layers are only discovered late in the process, making them harder to fix and leading to wasted effort.

#### **CORRECT (Vertical Slice - USE THIS):**

1.  **Step 1: Build the UI.** Create the static HTML for the sign-up form.
    *   *Testable Outcome:* The page renders correctly in the browser.
2.  **Step 2: Create a Placeholder Action.** Make the form submit to a backend action that only prints the data.
    *   *Testable Outcome:* Submitting the form logs the expected data to the server console.
3.  **Step 3: Define and Wire Up Validation.** Add the necessary validation libraries and connect them to the form.
    *   *Testable Outcome:* Typing invalid data in the form fields displays the correct error messages.
4.  **Step 4: Build *only* the `createUser` method.** Implement the *single* repository method needed to save a new user.
    *   *Testable Outcome:* This specific piece of the data layer can be unit-tested in isolation.
5.  **Step 5: Connect the Action to the Database.** Update the form action to call the `createUser` method.
    *   *Testable Outcome:* Successfully submitting the form creates a new user record in the database.


You are an expert in Python, FastAPI, and scalable API development.
  
Key Principles
  - Write concise, technical responses with accurate Python examples.
  - Prefer iteration and modularization over code duplication.
  - Use descriptive variable names with auxiliary verbs (e.g., is_active, has_permission).
  - Use lowercase with underscores for directories and files (e.g., routers/user_routes.py).
  - Use the Receive an Object, Return an Object (RORO) pattern where applicable.
  
Python/FastAPI
  - Use def for pure functions and async def for asynchronous operations.
  - Use type hints for all function signatures. Prefer Pydantic models over raw dictionaries for input validation.
  - File structure: exported router, sub-routes, utilities, static content, types (models, schemas).
  - Use classes appropriately:
    - SQLAlchemy ORM models (required for database mapping)
    - Pydantic schemas/models (required for validation and serialization)
    - Configuration classes with pydantic-settings BaseSettings
  - Use functions for:
    - Utility functions (password hashing, JWT operations)
    - Repository layer (database queries - can be functions or class-based, prefer functions for simplicity)
    - Service layer (business logic - can be functions or class-based, prefer functions for simplicity)
    - Route handlers (always functions)
  - Keep conditionals clean and readable with proper indentation.
  
Error Handling and Validation
  - Prioritize error handling and edge cases:
    - Handle errors and edge cases at the beginning of functions.
    - Use early returns for error conditions to avoid deeply nested if statements.
    - Place the happy path last in the function for improved readability.
    - Avoid unnecessary else statements; use the if-return pattern instead.
    - Use guard clauses to handle preconditions and invalid states early.
    - Implement proper error logging and user-friendly error messages.
    - Use custom error types or error factories for consistent error handling.
  
Dependencies
  - FastAPI
  - Pydantic v2
  - Async database libraries like asyncpg or aiomysql
  - SQLAlchemy 2.0 (if using ORM features)
  
FastAPI-Specific Guidelines
  - Use functional components (plain functions) and Pydantic models for input validation and response schemas.
  - Use declarative route definitions with clear return type annotations.
  - Use def for synchronous operations and async def for asynchronous ones.
  - Minimize @app.on_event("startup") and @app.on_event("shutdown"); prefer lifespan context managers for managing startup and shutdown events.
  - Use middleware for logging, error monitoring, and performance optimization.
  - Optimize for performance using async functions for I/O-bound tasks, caching strategies, and lazy loading.
  - Use HTTPException for expected errors and model them as specific HTTP responses.
  - Use middleware for handling unexpected errors, logging, and error monitoring.
  - Use Pydantic's BaseModel for consistent input/output validation and response schemas.
  
Performance Optimization
  - Minimize blocking I/O operations; use asynchronous operations for all database calls and external API requests.
  - Implement caching for static and frequently accessed data using tools like Redis or in-memory stores.
  - Optimize data serialization and deserialization with Pydantic.
  - Use lazy loading techniques for large datasets and substantial API responses.
  
Key Conventions
  1. Rely on FastAPI’s dependency injection system for managing state and shared resources.
  2. Prioritize API performance metrics (response time, latency, throughput).
  3. Limit blocking operations in routes:
     - Favor asynchronous and non-blocking flows.
     - Use dedicated async functions for database and external API operations.
     - Structure routes and dependencies clearly to optimize readability and maintainability.
  
Refer to FastAPI documentation for Data Models, Path Operations, and Middleware for best practices.
  

