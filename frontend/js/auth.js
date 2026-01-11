/**
 * Authentication utilities for Tiling System
 * Handles login, logout, and authentication checks
 */

/**
 * Check if user is authenticated
 * Redirects to login if not authenticated
 */
function checkAuth() {
    const token = localStorage.getItem('access_token');
    const user = getUserData();
    
    if (!token || !user) {
        window.location.href = '/frontend/auth/login.html';
        return false;
    }
    
    return true;
}

/**
 * Get stored user data
 * @returns {object|null} User data object or null
 */
function getUserData() {
    const userJson = localStorage.getItem('user');
    if (!userJson) return null;
    
    try {
        return JSON.parse(userJson);
    } catch (e) {
        console.error('Error parsing user data:', e);
        return null;
    }
}

/**
 * Handle user login
 * @param {string} email - User email
 * @param {string} password - User password
 * @returns {Promise<object>} Login response
 */
async function handleLogin(email, password) {
    try {
        const response = await login(email, password);
        
        // Store token and user info
        localStorage.setItem('access_token', response.access_token);
        localStorage.setItem('user', JSON.stringify(response.user));
        
        return response;
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

/**
 * Handle user logout
 */
function handleLogout() {
    // Clear localStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    
    // Redirect to login page
    window.location.href = '/frontend/auth/login.html';
}

/**
 * Get authentication token
 * @returns {string|null} Access token or null
 */
function getToken() {
    return localStorage.getItem('access_token');
}

/**
 * Get user role
 * @returns {string|null} User role or null
 */
function getUserRole() {
    const user = getUserData();
    return user ? user.role : null;
}

/**
 * Get company slug from user data
 * @returns {string|null} Company slug or null
 */
function getCompanySlug() {
    const user = getUserData();
    if (!user || !user.company) return null;
    return user.company.slug;
}

/**
 * Get company ID from user data
 * @returns {number|null} Company ID or null
 */
function getCompanyId() {
    const user = getUserData();
    return user ? user.company_id : null;
}

/**
 * Check if user is admin
 * @returns {boolean} True if user is admin
 */
function isAdmin() {
    const role = getUserRole();
    return role === 'admin';
}

/**
 * Check if user is company owner
 * @returns {boolean} True if user is company owner
 */
function isCompanyOwner() {
    const role = getUserRole();
    return role === 'owner';
}

/**
 * Redirect based on user role
 */
function redirectBasedOnRole() {
    const user = getUserData();
    if (!user) {
        window.location.href = '/frontend/auth/login.html';
        return;
    }
    
    if (user.role === 'admin') {
        window.location.href = '/frontend/admin/index.html';
    } else {
        // Get company slug from user data
        const companySlug = getCompanySlug();
        if (companySlug) {
            window.location.href = `/frontend/company/index.html?slug=${companySlug}`;
        } else {
            // Fallback if no company slug
            alert('Unable to determine your company. Please contact support.');
            handleLogout();
        }
    }
}

/**
 * Initialize logout button handler
 */
function initLogoutHandler() {
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (confirm('Are you sure you want to logout?')) {
                handleLogout();
            }
        });
    }
}

// Auto-initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Skip auth check on login and public pages
    const publicPages = ['/frontend/auth/login.html', '/frontend/auth/forgot-password.html', '/frontend/index.html'];
    const currentPath = window.location.pathname;
    
    if (!publicPages.includes(currentPath) && !currentPath.endsWith('/')) {
        checkAuth();
    }
    
    // Initialize logout handler
    initLogoutHandler();
});
