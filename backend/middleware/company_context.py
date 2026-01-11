from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import re


class CompanyContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract company slug from URL path and add it to request state.
    This allows easy access to the current company context throughout the request lifecycle.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Extract company slug from URL path patterns like:
        - /api/companies/{company_slug}/...
        - /{company_slug}/...
        
        Args:
            request: The incoming request
            call_next: The next middleware or route handler
            
        Returns:
            Response from the next handler
        """
        # Try to extract company slug from URL path
        path = request.url.path
        
        # Pattern 1: /api/companies/{slug}/...
        pattern1 = r'^/api/companies/([a-z0-9-]+)(?:/|$)'
        match = re.search(pattern1, path)
        
        if match:
            request.state.company_slug = match.group(1)
        else:
            # Pattern 2: /{slug}/... (but not /api/...)
            pattern2 = r'^/(?!api/)([a-z0-9-]+)(?:/|$)'
            match = re.search(pattern2, path)
            if match:
                request.state.company_slug = match.group(1)
            else:
                request.state.company_slug = None
        
        response = await call_next(request)
        return response
