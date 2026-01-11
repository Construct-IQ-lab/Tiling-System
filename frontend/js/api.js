/**
 * API Client for Tiling System
 * Handles all HTTP requests to the backend API
 */

// API Configuration
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000/api' 
    : '/api';

/**
 * Make an API request with proper authentication and error handling
 * @param {string} endpoint - API endpoint path
 * @param {string} method - HTTP method (GET, POST, PUT, DELETE)
 * @param {object} body - Request body data
 * @param {boolean} requiresAuth - Whether authentication is required
 * @returns {Promise<object>} Response data
 */
async function apiRequest(endpoint, method = 'GET', body = null, requiresAuth = true) {
    const headers = {
        'Content-Type': 'application/json',
    };

    // Add authorization header if required
    if (requiresAuth) {
        const token = localStorage.getItem('access_token');
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
    }

    const config = {
        method,
        headers,
    };

    // Add body for POST, PUT, PATCH requests
    if (body && ['POST', 'PUT', 'PATCH'].includes(method)) {
        config.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

        // Handle 401 Unauthorized - redirect to login
        if (response.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            window.location.href = '/frontend/auth/login.html';
            throw new Error('Unauthorized - please login again');
        }

        // Handle 403 Forbidden
        if (response.status === 403) {
            throw new Error('Access denied - insufficient permissions');
        }

        // Handle 404 Not Found
        if (response.status === 404) {
            throw new Error('Resource not found');
        }

        // For 204 No Content responses
        if (response.status === 204) {
            return { success: true };
        }

        // Parse JSON response
        const data = await response.json();

        // Handle error responses
        if (!response.ok) {
            throw new Error(data.detail || data.message || 'Request failed');
        }

        return data;
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

/**
 * GET request helper
 * @param {string} endpoint - API endpoint
 * @returns {Promise<object>} Response data
 */
async function get(endpoint) {
    return apiRequest(endpoint, 'GET');
}

/**
 * POST request helper
 * @param {string} endpoint - API endpoint
 * @param {object} data - Request body data
 * @returns {Promise<object>} Response data
 */
async function post(endpoint, data) {
    return apiRequest(endpoint, 'POST', data);
}

/**
 * PUT request helper
 * @param {string} endpoint - API endpoint
 * @param {object} data - Request body data
 * @returns {Promise<object>} Response data
 */
async function put(endpoint, data) {
    return apiRequest(endpoint, 'PUT', data);
}

/**
 * DELETE request helper
 * @param {string} endpoint - API endpoint
 * @returns {Promise<object>} Response data
 */
async function deleteRequest(endpoint) {
    return apiRequest(endpoint, 'DELETE');
}

/**
 * Login request (doesn't require auth)
 * @param {string} email - User email
 * @param {string} password - User password
 * @returns {Promise<object>} Login response with token and user data
 */
async function login(email, password) {
    const formData = new URLSearchParams();
    formData.append('username', email);  // OAuth2 uses 'username' field
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Login failed');
    }

    return response.json();
}

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { apiRequest, get, post, put, deleteRequest, login, API_BASE_URL };
}
