# Python Web Server API

A modern, scalable web API built with FastAPI, featuring JWT authentication, PostgreSQL database, and a clean layered architecture.

## Features

- 🚀 **FastAPI** - High-performance async web framework
- 🔐 **JWT Authentication** - Access and refresh token support
- 🗄️ **PostgreSQL** - Robust relational database with SQLAlchemy 2.0 ORM
- 🔒 **Argon2** - Secure password hashing
- 📝 **OpenAPI/Swagger** - Auto-generated interactive API documentation
- 🌐 **CORS** - Configured for frontend integration
- 🏗️ **Layered Architecture** - Repository pattern for database abstraction

## Prerequisites

- Python 3.14+
- PostgreSQL (running locally or accessible via connection string)

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   On Windows (PowerShell):
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   
   Copy `.env.example` to `.env` and update with your configuration:
   ```bash
   copy .env.example .env
   ```
   
   **Important**: Update the following in your `.env` file:
   - `DATABASE_URL` - Your PostgreSQL connection string
   - `JWT_SECRET_KEY` - Generate a secure secret key (see instructions in .env.example)

## Database Setup

1. **Create a PostgreSQL database**
   ```sql
   CREATE DATABASE your_database_name;
   ```

2. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

## Running the Server

**Development mode** (with auto-reload):
```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Swagger UI (Interactive)**: http://localhost:8000/docs
- **ReDoc (Alternative)**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Public Endpoints
- `POST /auth/signup` - Create a new user account
- `POST /auth/login` - Login and receive JWT tokens

### Protected Endpoints (Require Access Token)
- `GET /auth/me` - Get current user information
- `POST /auth/refresh` - Refresh access token (requires refresh token)

### Utility Endpoints
- `GET /health` - Health check endpoint

## Project Structure

```
py-web-server/
├── app/
│   ├── models/          # SQLAlchemy ORM models
│   ├── schemas/         # Pydantic request/response schemas
│   ├── repositories/    # Data access layer
│   ├── services/        # Business logic layer
│   ├── routers/         # API endpoint definitions
│   ├── utils/           # Utility functions
│   ├── config.py        # Configuration management
│   ├── database.py      # Database connection
│   ├── dependencies.py  # FastAPI dependencies
│   └── main.py          # Application entry point
├── alembic/             # Database migrations
├── tests/               # Test suite
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
└── README.md
```

## Development Workflow

### Creating Database Migrations

After modifying SQLAlchemy models:

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## Tech Stack

- **Framework**: FastAPI 0.115.0
- **Database**: PostgreSQL with SQLAlchemy 2.0
- **Authentication**: PyJWT with Argon2 password hashing
- **Migrations**: Alembic
- **Configuration**: Pydantic Settings

## Security Notes

- Passwords are hashed using Argon2 before storage
- JWT tokens expire after 24 hours (configurable)
- CORS is configured to only allow specified origins
- Never commit your `.env` file to version control

## License

[Your License Here]

