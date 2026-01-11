from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import re


class CompanyContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract company slug from URL path and attach to request state.
    Extracts slug from paths like: /{company-slug}/dashboard
    Skips extraction for /api, /admin, /auth, /static paths
    """
    
    # Paths to skip company slug extraction
    SKIP_PATHS = ["/api", "/admin", "/auth", "/static", "/docs", "/redoc", "/openapi.json", "/health", "/"]
    
    async def dispatch(self, request: Request, call_next):
        """
        Extract company slug from URL path if applicable.
        
        Args:
            request: The incoming request
            call_next: The next middleware/handler in chain
            
        Returns:
            Response from the next handler
        """
        path = request.url.path
        
        # Check if path should skip slug extraction
        should_skip = any(path.startswith(skip) for skip in self.SKIP_PATHS)
        
        if not should_skip:
            # Extract company slug from path: /{slug}/... pattern
            match = re.match(r'^/([a-z0-9-]+)(/.*)?$', path)
            if match:
                slug = match.group(1)
                # Attach slug to request state
                request.state.company_slug = slug
            else:
                request.state.company_slug = None
        else:
            request.state.company_slug = None
        
        response = await call_next(request)
        return response
