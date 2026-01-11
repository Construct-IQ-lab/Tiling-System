# Tiling System Frontend

Multi-tenant frontend system for the Tiling System application with separate Admin and Company portals.

## Features

### Admin Portal
- **Dashboard**: View system-wide statistics (companies, users, projects)
- **Companies Management**: Create, edit, and delete companies with custom branding
- **Users Management**: Manage user accounts across all companies
- **Projects Overview**: Monitor all projects across the system
- **Reports**: Placeholder for future analytics

### Company Portal (Dynamic Multi-Tenant)
- **Custom Branding**: Each company has unique colors and logo
- **Dynamic URLs**: Access via `/{company-slug}/` (e.g., `/elitetilingsolutions/`)
- **Dashboard**: Company-specific statistics
- **Projects**: Create and manage tiling projects
- **Calculator**: Three-step material and cost calculator
- **Quotes**: Placeholder for quote management
- **Profile**: View and edit company information

### Authentication
- Secure login with JWT tokens
- Role-based access control (Admin, Owner, Manager, Staff)
- Password toggle visibility
- Forgot password (placeholder)

## Directory Structure

```
frontend/
├── auth/                   # Authentication pages
│   ├── login.html
│   └── forgot-password.html
├── admin/                  # Admin portal
│   ├── index.html          # Dashboard
│   ├── companies.html      # Companies management
│   ├── users.html          # Users management
│   ├── projects.html       # All projects
│   └── reports.html        # Reports placeholder
├── company/                # Company portal (templates)
│   ├── index.html          # Company dashboard
│   ├── projects.html       # Company projects
│   ├── calculator.html     # Materials calculator
│   ├── quotes.html         # Quotes management
│   └── profile.html        # Company profile
├── css/                    # Stylesheets
│   ├── common.css          # Base styles
│   ├── auth.css            # Authentication styles
│   ├── admin.css           # Admin portal styles
│   └── company.css         # Company portal styles
└── js/                     # JavaScript files
    ├── api.js              # API helper functions
    ├── auth.js             # Authentication logic
    ├── theme.js            # Dynamic theming
    ├── admin.js            # Admin dashboard
    ├── admin-companies.js  # Companies management
    ├── admin-users.js      # Users management
    ├── company.js          # Company dashboard
    ├── company-projects.js # Projects management
    └── calculator.js       # Calculator functionality
```

## Quick Start

### Prerequisites
- Backend API running on `http://localhost:8000`
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Option 1: Simple HTTP Server (Development)

Using Python 3:
```bash
# From the repository root
python -m http.server 8080
```

Using Node.js:
```bash
# Install http-server globally
npm install -g http-server

# Run from repository root
http-server -p 8080
```

Then visit: `http://localhost:8080/frontend/auth/login.html`

### Option 2: Nginx (Production)

```nginx
server {
    listen 80;
    server_name localhost;
    root /path/to/Tiling-System;
    index index.html;

    # Main redirect
    location = / {
        return 301 /frontend/auth/login.html;
    }

    # Serve static files
    location / {
        try_files $uri $uri/ =404;
    }

    # API proxy (if backend on same server)
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Usage

### First Time Setup

1. **Start the backend API** (see backend README)
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Serve the frontend**
   ```bash
   # From repository root
   python -m http.server 8080
   ```

3. **Access the application**
   - Login page: `http://localhost:8080/frontend/auth/login.html`
   - Or just visit: `http://localhost:8080/` (auto-redirects)

### Default Admin Account

Create an admin account using the backend:

```python
# In Python shell or script
from backend.models.user import User
from backend.services.auth_service import AuthService
from backend.database import SessionLocal

db = SessionLocal()
admin = User(
    email="admin@example.com",
    password_hash=AuthService.get_password_hash("admin123"),
    first_name="Admin",
    last_name="User",
    role="admin",
    is_active=True
)
db.add(admin)
db.commit()
```

### Creating Your First Company

1. Login as admin: `http://localhost:8080/frontend/auth/login.html`
2. Navigate to Companies page
3. Click "Add New Company"
4. Fill in company details:
   - **Name**: Elite Tiling Solutions
   - **Slug**: elitetilingsolutions (auto-generated)
   - **Email**: info@elitetiling.com
   - **Colors**: Choose primary and secondary colors
5. Save the company

### Creating Company Users

1. Navigate to Users page in admin portal
2. Click "Add New User"
3. Fill in user details:
   - Select the company
   - Enter email and password
   - Choose role (owner, manager, staff)
4. Save the user

### Accessing Company Portal

Company users can access their portal at:
```
http://localhost:8080/{company-slug}/index.html
```

For example:
```
http://localhost:8080/elitetilingsolutions/index.html
```

**Note**: You need to manually copy the company template files to create the company-specific URLs. See "Multi-Tenant Routing" section below.

## Multi-Tenant Routing

The frontend supports dynamic company URLs via the slug pattern. There are two approaches:

### Approach 1: Manual Copy (Simple)

For each company, copy the template files:

```bash
# Create company directory
mkdir -p elitetilingsolutions

# Copy company portal templates
cp frontend/company/*.html elitetilingsolutions/
```

Then access: `http://localhost:8080/elitetilingsolutions/index.html`

### Approach 2: URL Rewrite (Production)

Use a web server with URL rewrite rules:

**Nginx:**
```nginx
location ~ ^/([a-z0-9-]+)/(index|projects|calculator|quotes|profile)\.html$ {
    alias /path/to/Tiling-System/frontend/company/$2.html;
}
```

**Apache (.htaccess):**
```apache
RewriteEngine On
RewriteRule ^([a-z0-9-]+)/(index|projects|calculator|quotes|profile)\.html$ frontend/company/$2.html [L]
```

## API Configuration

The API base URL is configured in `/frontend/js/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

For production, update this to your actual API URL:

```javascript
const API_BASE_URL = 'https://api.yourcompany.com/api';
```

Or make it dynamic:
```javascript
const API_BASE_URL = window.location.origin + '/api';
```

## Features Overview

### Admin Features

#### Dashboard
- Total companies, users, and projects
- Active vs. total counts
- Quick action shortcuts

#### Companies Management
- Create companies with custom branding
- Auto-generate slugs from company names
- Set primary and secondary colors
- Edit and delete companies

#### Users Management
- Create users for any company
- Assign roles (admin, owner, manager, staff)
- Link users to companies
- Manage user status

### Company Features

#### Dynamic Theming
- Each company has unique brand colors
- Colors applied automatically via CSS variables
- Company logo displayed in navigation
- Personalized navigation with company name

#### Projects Management
- Create and view company projects
- Track project details (client, area, budget)
- Project status badges
- Grid view with filtering

#### Materials Calculator
**Step 1: Area Calculation**
- Input length and width
- Calculate total area in m²

**Step 2: Materials Calculation**
- Tile size and wastage percentage
- Calculate tiles, grout, and adhesive needed

**Step 3: Cost Calculation**
- Input material prices
- Optional labor costs
- Total project cost estimation

#### Profile Management
- View company information
- See brand colors
- Edit profile (coming soon)
- Change password (coming soon)

## Technology Stack

- **HTML5**: Semantic markup
- **CSS3**: Custom properties, flexbox, grid
- **Vanilla JavaScript**: No frameworks, pure ES6+
- **Fetch API**: HTTP requests
- **LocalStorage**: Client-side token storage

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Responsive Design

The frontend is fully responsive with breakpoints at:
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

Mobile features:
- Hamburger menu navigation
- Stacked grid layouts
- Touch-friendly button sizes
- Optimized form inputs

## Security Features

- JWT token authentication
- Authorization headers on API requests
- XSS prevention via HTML escaping
- CSRF protection (backend handles)
- Secure password input with toggle
- Auto-logout on 401 responses

## Development

### Code Structure

**JavaScript Modules:**
- `api.js`: Core API functions
- `auth.js`: Authentication flow
- `theme.js`: Dynamic theming
- `admin-*.js`: Admin-specific logic
- `company-*.js`: Company-specific logic
- `calculator.js`: Calculator functionality

**CSS Organization:**
- `common.css`: Base styles (8KB)
- `auth.css`: Login pages (3KB)
- `admin.css`: Admin portal (6KB)
- `company.css`: Company portal (7KB)

### Adding New Pages

1. Create HTML file in appropriate directory
2. Include required CSS and JS files
3. Add navigation link
4. Implement page-specific JavaScript
5. Test authentication and API calls

### Debugging

Enable browser console to see:
- API request/response logs
- Authentication errors
- Theme loading issues

Check the browser's Network tab for:
- Failed API requests
- CORS issues
- 401/403 errors

## Common Issues

### CORS Errors
**Problem**: API requests blocked by CORS policy

**Solution**: Update backend `config.py`:
```python
ALLOWED_ORIGINS: List[str] = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
```

### 404 on Company URLs
**Problem**: Company pages not found

**Solution**: 
- Option 1: Copy template files to company directory
- Option 2: Configure web server URL rewriting

### Authentication Loops
**Problem**: Redirected to login repeatedly

**Solution**: 
- Check backend is running
- Verify API URL in `api.js`
- Clear localStorage and try again

### Theme Not Loading
**Problem**: Company colors not applied

**Solution**:
- Check `/api/companies/{slug}/theme` endpoint
- Verify company slug in URL
- Check browser console for errors

## Production Checklist

- [ ] Update `API_BASE_URL` in `api.js`
- [ ] Configure web server (Nginx/Apache)
- [ ] Set up URL rewriting for company portals
- [ ] Enable HTTPS
- [ ] Minify CSS and JavaScript
- [ ] Set up CDN for static assets
- [ ] Configure proper CORS origins
- [ ] Enable gzip compression
- [ ] Set up monitoring and analytics
- [ ] Test on multiple browsers and devices

## Future Enhancements

- [ ] Real-time updates with WebSocket
- [ ] File upload for company logos
- [ ] PDF quote generation
- [ ] Email notifications
- [ ] Advanced project management
- [ ] Mobile app (React Native)
- [ ] Offline support (PWA)
- [ ] Multi-language support

## Contributing

When contributing to the frontend:

1. Follow existing code style
2. Test on multiple browsers
3. Ensure responsive design
4. Add comments for complex logic
5. Update this README if needed

## License

Part of the Construct-IQ Lab ecosystem.
