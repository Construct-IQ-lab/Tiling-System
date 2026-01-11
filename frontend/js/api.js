// API Configuration and Helper Functions
const API_BASE_URL = 'http://localhost:8000';

/**
 * Make an authenticated API request
 * @param {string} endpoint - API endpoint path
 * @param {object} options - Fetch options
 * @returns {Promise} Response data
 */
async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem('access_token');
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers
    });
    
    if (response.status === 401) {
        // Token expired or invalid, redirect to login
        localStorage.clear();
        window.location.href = '/frontend/auth/login.html';
        throw new Error('Unauthorized');
    }
    
    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `HTTP ${response.status}`);
    }
    
    // Handle 204 No Content
    if (response.status === 204) {
        return null;
    }
    
    return response.json();
}

// Auth API
const authAPI = {
    login: (email, password) => 
        apiRequest('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        }),
    
    logout: () => 
        apiRequest('/api/auth/logout', { method: 'POST' }),
    
    getCurrentUser: () => 
        apiRequest('/api/auth/me')
};

// Admin API
const adminAPI = {
    // Dashboard
    getDashboardStats: () => 
        apiRequest('/api/admin/dashboard/stats'),
    
    // Companies
    getCompanies: (page = 1, perPage = 30) => 
        apiRequest(`/api/admin/companies?page=${page}&per_page=${perPage}`),
    
    createCompany: (data) => 
        apiRequest('/api/admin/companies', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
    
    getCompany: (id) => 
        apiRequest(`/api/admin/companies/${id}`),
    
    updateCompany: (id, data) => 
        apiRequest(`/api/admin/companies/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        }),
    
    deleteCompany: (id) => 
        apiRequest(`/api/admin/companies/${id}`, { method: 'DELETE' }),
    
    // Users
    getUsers: (page = 1, perPage = 30) => 
        apiRequest(`/api/admin/users?page=${page}&per_page=${perPage}`),
    
    createUser: (data) => 
        apiRequest('/api/admin/users', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
    
    updateUser: (id, data) => 
        apiRequest(`/api/admin/users/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        }),
    
    deleteUser: (id) => 
        apiRequest(`/api/admin/users/${id}`, { method: 'DELETE' })
};

// Company API
const companyAPI = {
    // Theme
    getTheme: (slug) => 
        apiRequest(`/api/companies/${slug}/theme`),
    
    // Dashboard
    getDashboard: (slug) => 
        apiRequest(`/api/companies/${slug}/dashboard`),
    
    // Projects
    getProjects: (slug, page = 1, perPage = 30) => 
        apiRequest(`/api/companies/${slug}/projects?page=${page}&per_page=${perPage}`),
    
    createProject: (slug, data) => 
        apiRequest(`/api/companies/${slug}/projects`, {
            method: 'POST',
            body: JSON.stringify(data)
        }),
    
    // Quotes
    getQuotes: (slug, page = 1, perPage = 30) => 
        apiRequest(`/api/companies/${slug}/quotes?page=${page}&per_page=${perPage}`),
    
    createQuote: (slug, data) => 
        apiRequest(`/api/companies/${slug}/quotes`, {
            method: 'POST',
            body: JSON.stringify(data)
        })
};

// Projects API
const projectsAPI = {
    getAll: () => 
        apiRequest('/api/v1/projects'),
    
    getById: (id) => 
        apiRequest(`/api/v1/projects/${id}`),
    
    create: (data) => 
        apiRequest('/api/v1/projects', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
    
    update: (id, data) => 
        apiRequest(`/api/v1/projects/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        }),
    
    delete: (id) => 
        apiRequest(`/api/v1/projects/${id}`, { method: 'DELETE' })
};

// Calculations API
const calculationsAPI = {
    calculateArea: (data) => 
        apiRequest('/api/v1/calculations/area', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
    
    calculateMaterials: (data) => 
        apiRequest('/api/v1/calculations/materials', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
    
    calculateCost: (data) => 
        apiRequest('/api/v1/calculations/cost', {
            method: 'POST',
            body: JSON.stringify(data)
        })
};

// Helper to show error messages
function showError(message, elementId = 'error-message') {
    const errorEl = document.getElementById(elementId);
    if (errorEl) {
        errorEl.textContent = message;
        errorEl.classList.add('active');
        setTimeout(() => errorEl.classList.remove('active'), 5000);
    } else {
        alert(message);
    }
}

// Helper to generate slug from name
function generateSlug(name) {
    return name
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-+|-+$/g, '');
}
