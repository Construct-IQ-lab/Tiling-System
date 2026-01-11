# Tiling System Architecture

> Part of the Construct-IQ Ecosystem

## Overview

The Tiling System is designed as a specialized module within the Construct-IQ ecosystem, focused on professional tiling project management, material calculations, and installation planning.

## System Purpose

- 📐 **Accurate Calculations**: Precise material and cost estimations
- 📊 **Project Management**: Track tiling projects from planning to completion
- 🎨 **Pattern Support**: Manage various tiling layouts and patterns
- 💰 **Cost Control**: Budget tracking and estimation
- 🔗 **Integration Ready**: Built for ecosystem connectivity

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Tiling System                             │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Project    │  │ Calculation  │  │   Pattern    │      │
│  │   Service    │  │   Engine     │  │   Library    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │             │
│  ┌──────────────────────────────────────────────────┐      │
│  │              Data Layer                          │      │
│  │    Projects | Materials | Calculations | Users  │      │
│  └──────────────────────────────────────────────────┘      │
│                          │                                  │
└──────────────────────────┼──────────────────────────────────┘
                           │
                  ┌────────┴─────────┐
                  │                  │
          ┌───────▼──────┐   ┌──────▼────────┐
          │ Integration  │   │  Decorating   │
          │     Hub      │   │    System     │
          └──────────────┘   └───────────────┘
```

## Core Components

### 1. Project Service

**Responsibilities:**
- CRUD operations for tiling projects
- Project lifecycle management
- Client information management
- Timeline tracking
- Status updates

**Key Features:**
- Create, read, update, delete projects
- Associate projects with clients
- Track project status (planning, in-progress, completed)
- Manage project metadata

**Data Model:**
```typescript
interface TilingProject {
  id: string;
  userId: string;
  name: string;
  description: string;
  client: ClientInfo;
  measurements: Measurements;
  tiles: TileSpecification;
  materials: MaterialList;
  status: ProjectStatus;
  timeline: Timeline;
  budget: BudgetInfo;
  createdAt: Date;
  updatedAt: Date;
}
```

### 2. Calculation Engine

**Core Calculations:**

#### Area Calculation
```
Total Area = Length × Width
Adjusted Area = Total Area × (1 + Wastage Factor)
```

#### Tile Quantity
```
Tile Area = Tile Length × Tile Width
Tiles Needed = Ceiling(Adjusted Area / Tile Area)
```

#### Grout Calculation
```
Joint Length = (Number of Tiles × Tile Perimeter)
Grout Volume = Joint Length × Joint Width × Joint Depth
Grout Needed = Grout Volume × Density Factor
```

#### Adhesive Calculation
```
Adhesive Coverage = Area × Thickness × Coverage Factor
Bags Needed = Ceiling(Adhesive Coverage / Bag Coverage)
```

**Wastage Factors:**
- Straight pattern: 5-10%
- Diagonal pattern: 10-15%
- Complex pattern: 15-20%
- Irregular area: Additional 5%

**Responsibilities:**
- Area calculations (rectangular, irregular shapes)
- Material quantity estimations
- Cost calculations
- Wastage factor application
- Pattern-specific adjustments

**Technology Considerations:**
- Pure functions for calculations
- Comprehensive unit testing
- Support for metric and imperial units
- Precision handling for decimals

### 3. Pattern Library

**Responsibilities:**
- Store tiling pattern definitions
- Pattern visualization data
- Layout recommendations
- Pattern-specific calculations

**Pattern Types:**
- Straight/Grid
- Diagonal
- Herringbone
- Brick/Running Bond
- Basketweave
- Chevron
- Hexagonal
- Custom patterns

**Pattern Data:**
```typescript
interface TilingPattern {
  id: string;
  name: string;
  description: string;
  wastagePercent: number;
  complexity: 'simple' | 'moderate' | 'complex';
  visualizationData: any;
  instructions: string[];
  recommendedFor: string[];
}
```

### 4. Material Management

**Material Types:**
- Tiles (ceramic, porcelain, natural stone, etc.)
- Grout (sanded, unsanded, epoxy)
- Adhesive (thin-set, mastic, epoxy)
- Sealer
- Underlayment
- Tools and supplies

**Material Database:**
```typescript
interface Material {
  id: string;
  type: MaterialType;
  name: string;
  manufacturer: string;
  specifications: {
    size?: string;
    coverage?: number;
    unit: string;
  };
  cost: {
    amount: number;
    currency: string;
    unit: string;
  };
  availability: boolean;
}
```

## API Design

### RESTful Endpoints

#### Projects
```
POST   /api/v1/projects              Create new project
GET    /api/v1/projects              List all projects
GET    /api/v1/projects/:id          Get project details
PUT    /api/v1/projects/:id          Update project
DELETE /api/v1/projects/:id          Delete project
PATCH  /api/v1/projects/:id/status   Update project status
```

#### Calculations
```
POST   /api/v1/calculate/area        Calculate tiling area
POST   /api/v1/calculate/materials   Calculate material needs
POST   /api/v1/calculate/cost        Calculate project cost
POST   /api/v1/calculate/pattern     Calculate for specific pattern
```

#### Patterns
```
GET    /api/v1/patterns              List available patterns
GET    /api/v1/patterns/:id          Get pattern details
POST   /api/v1/patterns              Create custom pattern
```

#### Materials
```
GET    /api/v1/materials             List available materials
GET    /api/v1/materials/:id         Get material details
POST   /api/v1/materials/search      Search materials
```

### Request/Response Examples

**Calculate Materials Request:**
```json
{
  "measurements": {
    "length": 5.0,
    "width": 4.0,
    "unit": "meters"
  },
  "tileSize": {
    "length": 0.3,
    "width": 0.3,
    "unit": "meters"
  },
  "pattern": "straight",
  "wastagePercent": 10
}
```

**Calculate Materials Response:**
```json
{
  "success": true,
  "data": {
    "area": 20.0,
    "adjustedArea": 22.0,
    "tiles": {
      "quantity": 245,
      "boxes": 11,
      "tilesPerBox": 22
    },
    "grout": {
      "amount": 2.5,
      "unit": "kg"
    },
    "adhesive": {
      "bags": 3,
      "coverage": "25kg bags"
    },
    "estimatedCost": {
      "tiles": 490.00,
      "grout": 25.00,
      "adhesive": 75.00,
      "total": 590.00,
      "currency": "USD"
    }
  },
  "meta": {
    "calculatedAt": "2026-01-11T12:00:00Z",
    "version": "1.0.0"
  }
}
```

## Data Flow

### Creating a Project with Calculations

```
1. User Input → API Gateway
2. Validate Input Data
3. Calculate Area
4. Calculate Materials
   ├─ Tile quantity
   ├─ Grout amount
   └─ Adhesive amount
5. Calculate Cost
6. Create Project Record
7. Store in Database
8. Return Project + Calculations
```

### Updating a Project

```
1. User Update → API Gateway
2. Fetch Existing Project
3. Validate Changes
4. Recalculate if measurements changed
5. Update Database
6. Return Updated Project
```

## Integration Points

### With Decorating System
- Share client information
- Link related projects (decorating + tiling)
- Cross-reference room specifications

### With Integration Hub (Future)
- Centralized authentication
- Shared user profiles
- Cross-system reporting
- Unified dashboard

### External Integrations (Future)
- Supplier APIs for material pricing
- Payment processing
- Document generation (invoices, quotes)
- Calendar/scheduling systems

## Technology Stack (Recommendations)

### Backend Options

**Option 1: Node.js + Express**
```
- Runtime: Node.js 18+
- Framework: Express.js
- Language: TypeScript
- ORM: Prisma / TypeORM
- Validation: Zod / Joi
```

**Option 2: Python + FastAPI**
```
- Runtime: Python 3.10+
- Framework: FastAPI
- ORM: SQLAlchemy
- Validation: Pydantic
```

### Database

**PostgreSQL** (Recommended)
- Relational data structure
- JSONB for flexible fields
- Strong ecosystem
- Excellent for calculations

**Schema Example:**
```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  measurements JSONB NOT NULL,
  tiles JSONB NOT NULL,
  materials JSONB,
  status VARCHAR(50) NOT NULL,
  budget DECIMAL(10,2),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE calculations (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects(id),
  calculation_type VARCHAR(50),
  inputs JSONB NOT NULL,
  outputs JSONB NOT NULL,
  calculated_at TIMESTAMP DEFAULT NOW()
);
```

### Frontend (Future)

```
- Framework: React / Vue / Svelte
- UI Library: Material-UI / Tailwind CSS
- State Management: Redux / Zustand
- Forms: React Hook Form
- Visualization: Chart.js / D3.js
```

## Security Considerations

### Authentication
- JWT-based authentication
- Token expiration and refresh
- Role-based access control (RBAC)

### Authorization Levels
- **Admin**: Full system access
- **Professional**: Full project management
- **Client**: View-only access to their projects
- **Guest**: Limited public access

### Data Protection
- Input validation and sanitization
- SQL injection prevention (parameterized queries)
- XSS protection
- Rate limiting on API endpoints
- Encryption for sensitive data

## Performance Optimization

### Caching Strategy
- Cache material prices (TTL: 1 hour)
- Cache pattern definitions
- Memoize calculation results
- Use Redis for session storage

### Database Optimization
- Index on user_id, status, created_at
- Pagination for large result sets
- Query optimization for complex calculations

### API Optimization
- Response compression (gzip)
- Lazy loading for large datasets
- Batch endpoints for multiple operations

## Testing Strategy

### Unit Tests
- Calculation functions (100% coverage)
- Data validation
- Utility functions

### Integration Tests
- API endpoints
- Database operations
- Authentication flows

### E2E Tests
- Complete user workflows
- Project creation to completion
- Calculation accuracy

### Test Coverage Goals
- Overall: 80%+
- Calculation engine: 100%
- API endpoints: 90%+

## Deployment Strategy

### Development Environment
```
- Local development with Docker
- Hot reloading
- Mock data seeding
- Development database
```

### Staging Environment
```
- Replica of production
- Integration testing
- Performance testing
- UAT (User Acceptance Testing)
```

### Production Environment
```
- Container-based (Docker)
- Load balancing
- Auto-scaling
- Monitoring and alerting
- Automated backups
```

### CI/CD Pipeline
```
1. Code Push → GitHub
2. Run Tests
3. Build Docker Image
4. Deploy to Staging
5. Run E2E Tests
6. Manual Approval
7. Deploy to Production
8. Health Checks
```

## Monitoring & Logging

### Metrics to Track
- API response times
- Calculation accuracy
- Error rates
- User activity
- System resource usage

### Logging
- Structured logging (JSON format)
- Log levels (DEBUG, INFO, WARN, ERROR)
- Centralized log aggregation
- Log retention policy

### Alerting
- System downtime
- High error rates
- Performance degradation
- Security incidents

## Future Enhancements

### Phase 1: Core Features (Months 1-3)
- [ ] Basic project management
- [ ] Core calculation engine
- [ ] Material database
- [ ] REST API

### Phase 2: Enhanced Features (Months 4-6)
- [ ] Pattern library
- [ ] Advanced calculations (irregular shapes)
- [ ] Cost tracking and reporting
- [ ] Client portal

### Phase 3: Advanced Features (Months 7-12)
- [ ] 3D visualization
- [ ] Mobile application
- [ ] Supplier integrations
- [ ] AI-powered recommendations
- [ ] Augmented reality (AR) preview

### Phase 4: Ecosystem Integration
- [ ] Integration Hub connectivity
- [ ] Cross-system data sharing
- [ ] Unified reporting
- [ ] Multi-system authentication

## Development Guidelines

### Code Organization
```
src/
├── api/
│   ├── routes/
│   ├── controllers/
│   └── middleware/
├── services/
│   ├── projectService.ts
│   ├── calculationService.ts
│   └── patternService.ts
├── models/
│   ├── Project.ts
│   ├── Calculation.ts
│   └── Pattern.ts
├── utils/
│   ├── calculations.ts
│   ├── validation.ts
│   └── converters.ts
├── config/
│   ├── database.ts
│   └── environment.ts
└── types/
    └── index.ts
```

### Best Practices
- Write self-documenting code
- Keep functions pure where possible
- Use TypeScript for type safety
- Document complex algorithms
- Follow SOLID principles
- Write tests first (TDD)

## Support & Maintenance

### Documentation
- Keep API docs updated
- Maintain changelog
- Document breaking changes
- Provide migration guides

### Versioning
- Semantic versioning (MAJOR.MINOR.PATCH)
- API versioning in URL path
- Deprecation warnings
- Backward compatibility where possible

---

**Version**: 1.0.0
**Last Updated**: 2026-01-11
**Status**: Initial Setup Phase

**Part of the Construct-IQ Ecosystem**