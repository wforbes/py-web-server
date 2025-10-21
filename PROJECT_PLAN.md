# Python Web Server - Project Plan

## Project Overview
Building a Python web API server using FastAPI with JWT authentication, PostgreSQL database, and a modular architecture designed for scalability.

## Documentation References
- [Python 3.14 Release Notes](https://docs.python.org/3/whatsnew/3.14.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Users](https://fastapi-users.github.io/fastapi-users/latest/) - Referenced for patterns but building custom auth
- [JWT Token & FastAPI Article](https://pythonebasta.medium.com/jwt-token-fastapi-8dba8fdd35e0)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/en/stable/)
- [Psycopg Documentation](https://www.psycopg.org/docs/)
- [Psycopg Installation](https://www.psycopg.org/docs/install.html)
- [SQLAlchemy 2.0 ORM](https://docs.sqlalchemy.org/en/20/orm/index.html)
- [SQLAlchemy 2.0 Quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [argon2-cffi GitHub](https://github.com/hynek/argon2-cffi)

## Tech Stack
- **Python**: 3.14 ([Python 3.14 Release Notes](https://docs.python.org/3/whatsnew/3.14.html))
- **Web Framework**: FastAPI ([FastAPI Documentation](https://fastapi.tiangolo.com/))
  - Async support, automatic OpenAPI docs, Pydantic v2 validation
  - Built on Starlette and Pydantic for high performance
- **Database**: PostgreSQL with psycopg2-binary driver ([Psycopg Documentation](https://www.psycopg.org/docs/))
- **ORM**: SQLAlchemy 2.0 ([SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/orm/quickstart.html))
  - Modern API with explicit select() statements
  - Better async support and improved type hints
- **Migrations**: Alembic
- **JWT**: PyJWT ([PyJWT Documentation](https://pyjwt.readthedocs.io/en/stable/))
  - Simple, actively maintained, well-documented
- **Password Hashing**: argon2-cffi ([argon2-cffi GitHub](https://github.com/hynek/argon2-cffi))
  - Using PasswordHasher class for secure password hashing
- **Environment Config**: pydantic-settings + python-dotenv
  - Leverages Pydantic v2 for type-safe configuration management
- **CORS**: FastAPI CORS middleware
- **Custom Authentication**: Building custom auth system instead of using FastAPI Users
  - Provides full control over authentication flow
  - Allows custom login logic (email OR username)
  - Better learning opportunity and easier to customize

## Dependencies (requirements.txt)
```txt
# Web Framework
fastapi==0.115.0
uvicorn[standard]==0.32.0

# Database
sqlalchemy==2.0.35
psycopg2-binary==2.9.10
alembic==1.13.3

# Authentication & Security
pyjwt==2.9.0
argon2-cffi==23.1.0
cryptography==43.0.1

# Configuration
pydantic-settings==2.6.0
python-dotenv==1.0.1

# Validation
pydantic[email]==2.9.2
email-validator==2.2.0
```

## Project Structure
```
py-web-server/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization, CORS setup
│   ├── config.py               # Environment configuration (pydantic-settings)
│   ├── database.py             # Database connection and session management
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/                # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── auth.py
│   ├── repositories/           # Data access layer (DB queries)
│   │   ├── __init__.py
│   │   └── user_repository.py
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── user_service.py
│   ├── routers/                # API endpoint definitions
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── dependencies.py         # FastAPI dependencies (auth, DB, etc.)
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── password.py         # Password hashing (argon2-cffi)
│       └── jwt.py              # JWT token utilities (PyJWT)
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
├── tests/                      # Test suite (future)
├── .env.example                # Example environment variables
├── .gitignore
├── requirements.txt            # Python dependencies
├── alembic.ini                 # Alembic configuration
├── PROJECT_PLAN.md             # This file - development plan and progress
└── README.md
```

## User Schema
```
users table:
- id (UUID, primary key)
- username (string, unique, indexed)
- email (string, unique, indexed)
- password_hash (string)
- created_at (timestamp)
- updated_at (timestamp)
```

## Authentication Flow
- **Access Token**: JWT with 24 hour expiration, contains user details
- **Refresh Token**: JWT with 24 hour expiration, used to obtain new access tokens
- **Login**: Accepts username OR email + password
- **Token Payload**: user_id, username, email, token_type (access/refresh), exp, iat

## Key Implementation Notes

### SQLAlchemy 2.0 Patterns
- Use explicit `select()` statements instead of legacy query API
- Example: `stmt = select(User).where(User.email == email)`
- Use `session.execute(stmt).scalar_one_or_none()` for queries
- Use `session.add()` and `session.commit()` for inserts

### PyJWT Usage
- `jwt.encode(payload, secret, algorithm="HS256")` to create tokens
- `jwt.decode(token, secret, algorithms=["HS256"])` to verify tokens
- Handle `jwt.ExpiredSignatureError` and `jwt.InvalidTokenError`

### Argon2 Password Hashing
- `PasswordHasher()` from argon2
- `hasher.hash(password)` to hash passwords
- `hasher.verify(hash, password)` to verify (raises VerifyMismatchError on failure)

### Pydantic Settings
- Use `BaseSettings` from pydantic-settings
- Automatic .env file loading
- Type-safe configuration with validation
- Example: `class Settings(BaseSettings): database_url: str`

---

## Development Plan (Vertical Slices)

### Phase 0: Project Foundation Setup
**Goal**: Set up the basic project structure, dependencies, and configuration

#### Step 0.1: Initialize Project Structure
- [x] Create directory structure
- [x] Create `requirements.txt` with all dependencies
- [x] Create `.gitignore` for Python projects
- [x] Create `.env.example` with required environment variables
- [x] Create basic `README.md` with setup instructions

#### Step 0.2: Configuration Layer
- [x] Create `app/config.py` - load environment variables (DB connection string, JWT secret, CORS origins, token expiration)
- [x] Implement Settings class using pydantic-settings BaseSettings
- [x] Use Pydantic v2 features for type-safe configuration management

#### Step 0.3: Database Foundation
- [x] Create `app/database.py` - SQLAlchemy 2.0 engine, session factory, Base class
- [x] Use SQLAlchemy 2.0 modern API patterns (explicit select statements)
- [x] Set up database connection with connection string from config
- [x] Create session dependency for FastAPI using dependency injection

#### Step 0.4: FastAPI Application Initialization
- [x] Create `app/main.py` - initialize FastAPI app
- [x] Configure CORS middleware with origins from environment
- [x] Set up OpenAPI documentation metadata
- [x] Create basic health check endpoint (GET `/health`)
- [x] Test that server starts and health endpoint responds

#### Step 0.5: Alembic Setup
- [x] Initialize Alembic (`alembic init alembic`)
- [x] Configure `alembic.ini` to use database URL from config
- [x] Configure `alembic/env.py` to import SQLAlchemy models

---

### Phase 1: User Signup Feature (Complete Vertical Slice)
**Goal**: Implement complete signup flow from request to database

#### Step 1.1: User Model (Data Layer)
- [x] Create `app/models/user.py` - SQLAlchemy User model
  - Fields: id, username, email, password_hash, created_at, updated_at
  - Indexes on username and email
  - Unique constraints on username and email
- [x] Create Alembic migration for users table
- [x] Run migration to create table in database

#### Step 1.2: Pydantic Schemas (API Layer)
- [x] Create `app/schemas/user.py`
  - `UserCreate` schema (input: username, email, password)
  - `UserResponse` schema (output: id, username, email, created_at - no password!)
- [x] Add validation (email format, password strength, username requirements)

#### Step 1.3: Password Utilities
- [x] Create `app/utils/password.py`
  - `hash_password()` function using argon2-cffi PasswordHasher
  - `verify_password()` function using PasswordHasher.verify()
  - Handle argon2 exceptions (InvalidHash, VerifyMismatchError)

#### Step 1.4: User Repository (Data Access Layer)
- [x] Create `app/repositories/user_repository.py`
  - `create_user()` - insert new user into database using SQLAlchemy 2.0 patterns
  - `get_user_by_email()` - query user by email using select()
  - `get_user_by_username()` - query user by username using select()
  - `get_user_by_email_or_username()` - query by either field using or_() filter
  - Use SQLAlchemy 2.0 explicit select statements throughout

#### Step 1.5: User Service (Business Logic Layer)
- [x] Create `app/services/user_service.py`
  - `register_user()` - validate uniqueness, hash password, call repository
  - Handle duplicate username/email errors

#### Step 1.6: Signup Endpoint (API Layer)
- [x] Create `app/routers/auth.py`
  - POST `/auth/signup` endpoint
  - Accept UserCreate schema
  - Call user service
  - Return UserResponse with 201 status
  - Handle errors (duplicate user, validation errors)
- [x] Register router in `app/main.py`

#### Step 1.7: Test Signup Flow
- [ ] Start server
- [ ] Test signup with valid data (via Swagger UI or curl)
- [ ] Test duplicate username error
- [ ] Test duplicate email error
- [ ] Test validation errors (invalid email, weak password)
- [ ] Verify user is created in database

---

### Phase 2: Login Feature (Complete Vertical Slice)
**Goal**: Implement login with JWT token generation

#### Step 2.1: JWT Utilities
- [ ] Create `app/utils/jwt.py`
  - `create_access_token()` - generate JWT access token using PyJWT (24h expiration)
  - `create_refresh_token()` - generate JWT refresh token using PyJWT (24h expiration)
  - `decode_token()` - verify and decode JWT token using jwt.decode()
  - Token payload includes: user_id, username, email, token_type, exp, iat
  - Handle PyJWT exceptions (ExpiredSignatureError, InvalidTokenError)

#### Step 2.2: Auth Schemas
- [ ] Create `app/schemas/auth.py`
  - `LoginRequest` schema (username_or_email, password)
  - `TokenResponse` schema (access_token, refresh_token, token_type="bearer")

#### Step 2.3: Auth Service (Business Logic Layer)
- [ ] Create `app/services/auth_service.py`
  - `authenticate_user()` - verify credentials using username or email
  - `login()` - authenticate and generate tokens
  - Handle invalid credentials error

#### Step 2.4: Login Endpoint (API Layer)
- [ ] Add POST `/auth/login` endpoint to `app/routers/auth.py`
  - Accept LoginRequest schema
  - Call auth service to authenticate
  - Return TokenResponse with access and refresh tokens
  - Return 401 for invalid credentials

#### Step 2.5: Test Login Flow
- [ ] Create a test user via signup
- [ ] Test login with username + correct password
- [ ] Test login with email + correct password
- [ ] Test login with incorrect password (should fail with 401)
- [ ] Test login with non-existent user (should fail with 401)
- [ ] Verify JWT tokens are valid and contain correct payload

---

### Phase 3: Protected Endpoints & Token Validation
**Goal**: Implement JWT authentication dependency for protected routes

#### Step 3.1: Authentication Dependencies
- [ ] Create `app/dependencies.py`
  - `get_current_user()` dependency - extract and validate access token from Authorization header
  - Decode JWT and verify it's an access token
  - Look up user from database using token payload
  - Return User model or raise 401 Unauthorized
  - Handle expired tokens, invalid tokens, missing tokens

#### Step 3.2: Current User Endpoint (Protected Route Example)
- [ ] Add GET `/auth/me` endpoint to `app/routers/auth.py`
  - Require authentication using `get_current_user` dependency
  - Return current user's information (UserResponse)

#### Step 3.3: Test Protected Endpoints
- [ ] Test `/auth/me` without token (should return 401)
- [ ] Test `/auth/me` with invalid token (should return 401)
- [ ] Test `/auth/me` with valid access token (should return user data)
- [ ] Test `/auth/me` with refresh token instead of access token (should fail)

---

### Phase 4: Token Refresh Feature
**Goal**: Implement refresh token endpoint to get new access tokens

#### Step 4.1: Refresh Token Dependency
- [ ] Add `get_current_user_from_refresh_token()` to `app/dependencies.py`
  - Similar to `get_current_user()` but validates refresh token type
  - Returns user for refresh token

#### Step 4.2: Refresh Token Endpoint
- [ ] Add POST `/auth/refresh` endpoint to `app/routers/auth.py`
  - Accept refresh token in Authorization header
  - Use `get_current_user_from_refresh_token()` dependency
  - Generate new access token and refresh token
  - Return TokenResponse

#### Step 4.3: Test Token Refresh
- [ ] Login to get tokens
- [ ] Use refresh token to get new tokens via `/auth/refresh`
- [ ] Verify new access token works with `/auth/me`
- [ ] Test using access token with `/auth/refresh` (should fail)
- [ ] Test using expired/invalid refresh token (should fail)

---

### Phase 5: Error Handling & Response Standardization
**Goal**: Ensure consistent error responses and proper HTTP status codes

#### Step 5.1: Exception Handlers
- [ ] Add custom exception handlers in `app/main.py`
  - Handle SQLAlchemy IntegrityError (duplicate entries)
  - Handle JWT exceptions (expired, invalid)
  - Handle validation errors
  - Return consistent JSON error format

#### Step 5.2: Test Error Scenarios
- [ ] Test all error cases return proper status codes
- [ ] Test error responses have consistent format
- [ ] Test validation errors include field-specific messages

---

### Phase 6: Documentation & Finalization
**Goal**: Complete documentation and ensure project is ready for use

#### Step 6.1: Update README
- [ ] Add prerequisites (Python 3.14, PostgreSQL)
- [ ] Add setup instructions
- [ ] Add database setup instructions
- [ ] Add how to run migrations
- [ ] Add how to start the server
- [ ] Add API endpoint documentation (or link to Swagger)
- [ ] Add environment variables documentation

#### Step 6.2: Environment Configuration
- [ ] Verify `.env.example` has all required variables with descriptions
- [ ] Document default values and required values

#### Step 6.3: Final Testing
- [ ] Run through complete user journey:
  1. Signup
  2. Login
  3. Access protected endpoint
  4. Refresh token
  5. Access protected endpoint with new token
- [ ] Verify OpenAPI docs are complete at `/docs`
- [ ] Test CORS with frontend domain

---

## Environment Variables (.env)
```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# JWT
JWT_SECRET_KEY=your-secret-key-here-use-something-secure-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours
REFRESH_TOKEN_EXPIRE_MINUTES=1440  # 24 hours

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Application
PROJECT_NAME=Python Web Server API
DEBUG=true
```

## API Endpoints Summary

### Public Endpoints
- `POST /auth/signup` - Create new user account
- `POST /auth/login` - Login and receive tokens

### Protected Endpoints (Require Access Token)
- `GET /auth/me` - Get current user information
- `POST /auth/refresh` - Refresh access token (requires refresh token)

### Utility Endpoints
- `GET /health` - Health check

---

## Success Criteria
- ✅ User can signup with username, email, and password
- ✅ Passwords are hashed with argon2 before storage
- ✅ User can login with username OR email
- ✅ JWT tokens (access & refresh) are returned on login
- ✅ Protected endpoints require valid access token
- ✅ Refresh endpoint provides new tokens
- ✅ CORS is configured for frontend domain
- ✅ OpenAPI/Swagger documentation is available
- ✅ Database queries use repository pattern for abstraction
- ✅ Code is modular and follows separation of concerns
- ✅ All environment configuration is externalized

---

## Future Enhancements (Post-MVP)
- Email verification
- Password reset flow
- Rate limiting
- Logout/token revocation (token blacklist)
- User profile updates
- Admin roles and permissions
- Unit and integration tests
- Docker containerization (deferred until MVP is stable)
- CI/CD pipeline
- Upgrade to psycopg3 for better async support (optional)
- Consider async SQLAlchemy sessions for higher performance (optional)

