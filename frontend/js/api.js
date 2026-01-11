// API Helper Functions

// Determine API base URL based on environment
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000/api'
    : (window.location.origin + '/api');

/**
 * Makes an API request with proper error handling
 * @param {string} endpoint - API endpoint (without base URL)
 * @param {string} method - HTTP method (GET, POST, PUT, DELETE)
 * @param {object|null} data - Request body data
 * @param {boolean} auth - Whether to include authentication token
 * @returns {Promise} Response data
 */
async function apiRequest(endpoint, method = 'GET', data = null, auth = true) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const headers = {
        'Content-Type': 'application/json',
    };
    
    // Add authorization header if auth is required
    if (auth) {
        const token = localStorage.getItem('access_token');
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
    }
    
    const options = {
        method: method,
        headers: headers,
    };
    
    // Add body for POST, PUT, PATCH requests
    if (data && ['POST', 'PUT', 'PATCH'].includes(method)) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        
        // Handle different response types
        if (response.status === 204) {
            // No content
            return null;
        }
        
        // Try to parse JSON response
        let responseData;
        try {
            responseData = await response.json();
        } catch (e) {
            // If not JSON, return text
            responseData = await response.text();
        }
        
        // Handle error responses
        if (!response.ok) {
            // Handle specific status codes
            if (response.status === 401) {
                // Unauthorized - redirect to login
                localStorage.clear();
                window.location.href = '/auth/login.html';
                throw new Error('Unauthorized. Please login again.');
            } else if (response.status === 403) {
                throw new Error('Access denied. You do not have permission to perform this action.');
            } else if (response.status === 404) {
                throw new Error('Resource not found.');
            } else if (response.status === 500) {
                throw new Error('Server error. Please try again later.');
            } else {
                // Use error message from API if available
                const errorMessage = responseData.detail || responseData.message || 'An error occurred';
                throw new Error(errorMessage);
            }
        }
        
        return responseData;
        
    } catch (error) {
        // Handle network errors
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            throw new Error('Network error. Please check your connection.');
        }
        throw error;
    }
}

/**
 * Display an error message to the user
 * @param {string} message - Error message to display
 * @param {string} elementId - ID of the element to display the error in
 */
function showError(message, elementId = 'error-message') {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.classList.add('active');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            errorElement.classList.remove('active');
        }, 5000);
    } else {
        // Fallback to alert if element not found
        alert(message);
    }
}

/**
 * Display a success message to the user
 * @param {string} message - Success message to display
 * @param {string} elementId - ID of the element to display the success in
 */
function showSuccess(message, elementId = 'success-message') {
    const successElement = document.getElementById(elementId);
    if (successElement) {
        successElement.textContent = message;
        successElement.classList.add('active');
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            successElement.classList.remove('active');
        }, 3000);
    }
}

/**
 * Set loading state on a button
 * @param {HTMLElement} button - Button element
 * @param {boolean} loading - Whether to set loading state
 */
function setButtonLoading(button, loading) {
    if (loading) {
        button.disabled = true;
        button.classList.add('loading');
        button.dataset.originalText = button.textContent;
        button.textContent = 'Loading...';
    } else {
        button.disabled = false;
        button.classList.remove('loading');
        if (button.dataset.originalText) {
            button.textContent = button.dataset.originalText;
        }
    }
}

/**
 * Format currency
 * @param {number} amount - Amount to format
 * @param {string} currency - Currency code
 * @returns {string} Formatted currency string
 */
function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

/**
 * Format date
 * @param {string} dateString - Date string to format
 * @returns {string} Formatted date string
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

/**
 * Generate slug from string
 * @param {string} str - String to convert to slug
 * @returns {string} Slug
 */
function generateSlug(str) {
    return str
        .toLowerCase()
        .trim()
        .replace(/[^\w\s-]/g, '') // Remove non-word chars except spaces and hyphens
        .replace(/[\s_-]+/g, '-') // Replace spaces, underscores, and multiple hyphens with single hyphen
        .replace(/^-+|-+$/g, ''); // Remove leading/trailing hyphens
}
