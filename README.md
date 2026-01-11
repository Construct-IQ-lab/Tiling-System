# Tiling System - Multi-Tenant SaaS Platform

A comprehensive multi-tenant SaaS platform for managing tiling projects, calculations, quotes, and invoices. Features separate admin and company portals with dynamic theming and role-based access control.

## Features

### Multi-Tenancy
- **URL-based tenant identification**: Each company gets a branded portal at `/{company-slug}/*`
- **Dynamic theming**: Custom colors and branding per company
- **Data isolation**: Complete separation of company data

### Authentication & Authorization
- **JWT-based authentication** with secure token management
- **Role-based access control**:
  - `admin`: Full system access, manages all companies and users
  - `company_owner`: Full access to their company's data
  - `company_staff`: Access to their company's projects and quotes
- **Secure password hashing** with bcrypt

### Admin Portal (`/admin/*`)
- Dashboard with system-wide statistics
- Company management (CRUD operations)
- User management across all companies
- Project overview across all tenants
- Reports and analytics

### Company Portal (`/{company-slug}/*`)
- Customized dashboard with company branding
- Project management
- Material calculator (area, materials, cost estimation)
- Quote generation and tracking
- Invoice management
- Company profile customization

### API Features
- RESTful API design
- Automatic OpenAPI documentation (Swagger UI)
- Comprehensive validation with Pydantic
- Database ORM with SQLAlchemy
- PostgreSQL support

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Primary database
- **Pydantic**: Data validation
- **JWT**: Authentication tokens
- **Bcrypt**: Password hashing

### Frontend
- **Vanilla JavaScript**: No framework dependencies
- **CSS3**: Custom styling with CSS variables for theming
- **HTML5**: Semantic markup

## Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- pip

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Construct-IQ-lab/Tiling-System.git
cd Tiling-System
```

2. **Set up PostgreSQL**
```bash
# Start PostgreSQL (using Docker)
docker run --name tiling-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=tiling_system \
  -p 5432:5432 \
  -d postgres:15-alpine

# Or use your existing PostgreSQL instance
```

3. **Create Python virtual environment**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

6. **Seed the database**
```bash
cd ..
python3 scripts/seed_database.py
```

7. **Run the application**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

8. **Access the application**
- API Documentation: http://localhost:8000/docs
- Admin Portal: http://localhost:8000/frontend/admin/index.html
- Company Portal: http://localhost:8000/frontend/company/index.html?slug={company-slug}

## Test Credentials

After running the seed script, use these credentials:

### Admin Access
- **Email**: admin@tilingsystem.com
- **Password**: admin123
- **URL**: http://localhost:8000/frontend/admin/index.html

### Company 1 - Elite Tiling Solutions
- **Owner Email**: owner@elitetiling.com
- **Staff Email**: staff@elitetiling.com
- **Password**: owner123 / staff123
- **URL**: http://localhost:8000/frontend/company/index.html?slug=elitetilingsolutions

### Company 2 - Pro Tile Masters
- **Owner Email**: owner@protilemasters.com
- **Password**: owner123
- **URL**: http://localhost:8000/frontend/company/index.html?slug=protilemasters

## Database Schema

### Core Models

1. **Company**: Multi-tenant entity with branding
   - Fields: id, name, slug, email, phone, address, logo_url, primary_color, secondary_color, status, subscription_plan
   
2. **User**: System users with roles
   - Fields: id, email, password_hash, first_name, last_name, role, company_id, is_active, last_login
   - Roles: admin, company_owner, company_staff

3. **Project**: Tiling projects
   - Fields: id, name, description, company_id, created_by, client_info, measurements, tiles, materials, status, budget
   
4. **Quote**: Customer quotes
   - Fields: id, quote_number, company_id, project_id, client_info, total_amount, status, valid_until
   
5. **Invoice**: Customer invoices
   - Fields: id, invoice_number, company_id, project_id, amount, status, due_date, paid_date

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user info

### Admin Routes (Requires admin role)
- `GET /api/admin/dashboard/stats` - System statistics
- `GET /api/admin/companies` - List companies
- `POST /api/admin/companies` - Create company
- `PUT /api/admin/companies/{id}` - Update company
- `DELETE /api/admin/companies/{id}` - Archive company
- `GET /api/admin/users` - List users
- `POST /api/admin/users` - Create user
- `PUT /api/admin/users/{id}` - Update user
- `DELETE /api/admin/users/{id}` - Deactivate user

### Company Routes (Requires company access)
- `GET /api/companies/{slug}/theme` - Get company branding (public)
- `GET /api/companies/{slug}/dashboard` - Company dashboard stats
- `GET /api/companies/{slug}/projects` - List company projects
- `POST /api/companies/{slug}/projects` - Create project
- `GET /api/companies/{slug}/quotes` - List quotes
- `POST /api/companies/{slug}/quotes` - Create quote

### Calculations
- `POST /api/v1/calculations/area` - Calculate tiling area
- `POST /api/v1/calculations/materials` - Calculate materials needed
- `POST /api/v1/calculations/cost` - Calculate total cost

## Project Structure

```
Tiling-System/
├── backend/
│   ├── models/           # Database models
│   │   ├── company.py
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── quote.py
│   │   └── invoice.py
│   ├── routes/           # API endpoints
│   │   ├── auth.py
│   │   ├── admin.py
│   │   ├── companies.py
│   │   ├── projects.py
│   │   └── calculations.py
│   ├── services/         # Business logic
│   │   └── auth_service.py
│   ├── middleware/       # Request middleware
│   │   ├── auth.py
│   │   └── company_context.py
│   ├── config.py         # Configuration
│   ├── database.py       # Database setup
│   ├── main.py           # FastAPI app
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── auth/             # Authentication pages
│   │   ├── login.html
│   │   └── forgot-password.html
│   ├── admin/            # Admin portal
│   │   ├── index.html
│   │   ├── companies.html
│   │   ├── users.html
│   │   ├── projects.html
│   │   └── reports.html
│   ├── company/          # Company portal
│   │   ├── index.html
│   │   ├── projects.html
│   │   ├── calculator.html
│   │   ├── quotes.html
│   │   └── profile.html
│   ├── css/              # Stylesheets
│   │   ├── common.css
│   │   ├── auth.css
│   │   ├── admin.css
│   │   └── company.css
│   └── js/               # JavaScript
│       ├── api.js
│       ├── auth.js
│       ├── theme.js
│       ├── admin.js
│       ├── admin-companies.js
│       ├── company.js
│       └── company-projects.js
├── scripts/
│   └── seed_database.py  # Database seeding
└── ARCHITECTURE.md       # Architecture documentation
```

## Development

### Run with auto-reload
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Access API documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Database migrations
For production, consider using Alembic:
```bash
pip install alembic
alembic init alembic
# Configure alembic.ini and env.py
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Security Features

- **Password hashing**: Bcrypt with salt
- **JWT tokens**: HS256 algorithm with configurable expiry
- **Role-based access**: Dependency injection for authorization
- **Data isolation**: Automatic tenant filtering in queries
- **CORS configuration**: Configurable allowed origins
- **Input validation**: Pydantic models for all requests

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@localhost:5432/tiling_system` |
| `SECRET_KEY` | Secret key for JWT signing | **Change in production** |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry time | `30` |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_ORIGINS` | CORS allowed origins | localhost URLs |

## Production Deployment

1. Set environment variables securely
2. Use strong `SECRET_KEY`
3. Set `DEBUG=False`
4. Configure proper CORS origins
5. Use production WSGI server with workers:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```
6. Set up HTTPS with reverse proxy (nginx/caddy)
7. Configure database backups
8. Enable database connection pooling
9. Set up monitoring and logging

## License

Part of the Construct-IQ Lab ecosystem.

## Contributing

Please read ARCHITECTURE.md for detailed information about the system design and implementation guidelines.
