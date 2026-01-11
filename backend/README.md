# Tiling System Backend

FastAPI backend for the Tiling System application.

## Features

- **Projects API**: Full CRUD operations for tiling projects
- **Calculations API**: Area, materials, and cost calculations
- **SQLAlchemy ORM**: Database management with PostgreSQL
- **Automatic API Documentation**: Swagger UI and ReDoc
- **CORS Support**: Cross-origin resource sharing configured

## Quick Start

### Using Docker (Recommended)

```bash
# From project root
docker-compose up
```

API will be available at:
- http://localhost:8000
- Documentation: http://localhost:8000/docs

### Manual Setup

1. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. **Start PostgreSQL**:
```bash
# Using Docker
docker run --name tiling-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=tiling_system -p 5432:5432 -d postgres:15-alpine

# Or use your own PostgreSQL instance
```

5. **Run the application**:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Projects
- `POST /api/v1/projects` - Create a new project
- `GET /api/v1/projects` - List all projects
- `GET /api/v1/projects/{id}` - Get project by ID
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

### Calculations
- `POST /api/v1/calculations/area` - Calculate area
- `POST /api/v1/calculations/materials` - Calculate materials needed
- `POST /api/v1/calculations/cost` - Calculate total cost

## Project Structure

```
backend/
├── main.py              # FastAPI application and routes
├── config.py            # Application configuration
├── database.py          # Database connection and session
├── models/              # SQLAlchemy models
├── routes/              # API route handlers
├── services/            # Business logic
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
└── .env.example        # Environment variables template
```

## Development

### Run with auto-reload
```bash
uvicorn main:app --reload
```

### Access API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Database Migrations

For production, consider using Alembic for database migrations:

```bash
pip install alembic
alembic init alembic
# Configure alembic.ini and env.py
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Testing

Run tests with pytest:

```bash
pip install pytest pytest-asyncio httpx
pytest tests/
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@localhost:5432/tiling_system` |
| `SECRET_KEY` | Secret key for JWT tokens | Change in production |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_ORIGINS` | CORS allowed origins | localhost URLs |

## Production Deployment

1. Set `DEBUG=False` in environment
2. Use a strong `SECRET_KEY`
3. Configure proper CORS origins
4. Use a production WSGI server (uvicorn with workers)
5. Set up proper database backups
6. Enable HTTPS

```bash
# Production command
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## License

Part of the Construct-IQ Lab ecosystem.