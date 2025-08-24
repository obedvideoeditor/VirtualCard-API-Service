# VirtualCard-API-Service

A FastAPI-based backend for managing virtual cards, simulating issuance and transaction processing. Integrates with PostgreSQL for data persistence and AWS S3 for transaction logs, with JWT authentication.

## Features
- RESTful endpoints for creating, retrieving, and managing virtual cards.
- Secure JWT authentication.
- PostgreSQL for storing card and transaction data.
- AWS S3 for storing transaction logs.
- Unit tests with pytest.
- CI/CD pipeline with GitHub Actions.
- Dockerized for easy deployment.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/VirtualCard-API-Service.git
   cd VirtualCard-API-Service
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   - Copy `.env.example` to `.env` and update with your PostgreSQL and AWS credentials:
     ```env
     DATABASE_URL=postgresql://user:password@localhost:5432/virtual_cards
     AWS_ACCESS_KEY_ID=your_aws_access_key
     AWS_SECRET_ACCESS_KEY=your_aws_secret_key
     AWS_REGION=us-east-1
     S3_BUCKET=your-s3-bucket
     JWT_SECRET_KEY=your_jwt_secret_key
     ```

4. **Set Up PostgreSQL**:
   - Ensure PostgreSQL is running and create a database named `virtual_cards`.
   - Run migrations (manually create tables using `models.py`).

5. **Run the Application**:
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Run Tests**:
   ```bash
   pytest tests/
   ```

7. **Build and Run Docker**:
   ```bash
   docker build -t virtual-card-api .
   docker run -d -p 8000:8000 --env-file .env virtual-card-api
   ```

## Project Structure
- `src/main.py`: FastAPI application with API endpoints.
- `src/models.py`: SQLAlchemy models for database tables.
- `src/schemas.py`: Pydantic schemas for request/response validation.
- `src/crud.py`: CRUD operations for database interactions.
- `src/auth.py`: JWT authentication logic.
- `src/aws_utils.py`: AWS S3 integration for transaction logs.
- `src/config.py`: Configuration and environment variable loading.
- `tests/test_api.py`: Unit tests for API endpoints.
- `.github/workflows/ci.yml`: CI/CD pipeline configuration.
- `Dockerfile`: Docker configuration for deployment.
- `.env.example`: Example environment variables.

## API Endpoints
- `POST /token`: Generate JWT token for authentication.
- `POST /cards`: Create a new virtual card (authenticated).
- `GET /cards/{card_id}`: Retrieve a virtual card by ID (authenticated).
- `POST /cards/{card_id}/transactions`: Log a transaction for a card (authenticated).

## Example Usage
```bash
curl -X POST "http://localhost:8000/token" -d '{"username": "user", "password": "pass"}'
curl -X POST "http://localhost:8000/cards" -H "Authorization: Bearer <token>" -d '{"card_number": "1234567890123456", "expiry": "12/27", "cvv": "123"}'
```

## Testing
Run `pytest tests/` to execute unit tests, covering card creation, retrieval, and transaction logging.

## Deployment
- Deploy to AWS ECS or a similar platform using the provided `Dockerfile`.
- Ensure AWS credentials and S3 bucket are configured in `.env`.
