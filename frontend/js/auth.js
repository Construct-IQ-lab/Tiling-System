// Authentication Logic

/**
 * Check if user is authenticated
 * Redirects to login page if not authenticated
 */
function checkAuth() {
    const token = localStorage.getItem('access_token');
    const currentPage = window.location.pathname;
    
    // Skip auth check for auth pages
    if (currentPage.includes('/auth/')) {
        return;
    }
    
    if (!token) {
        // Save current page to redirect back after login
        localStorage.setItem('redirect_after_login', currentPage);
        window.location.href = '/auth/login.html';
    }
}

/**
 * Get current user information from localStorage
 * @returns {object|null} User object or null
 */
function getCurrentUser() {
    const userRole = localStorage.getItem('user_role');
    const companySlug = localStorage.getItem('company_slug');
    const userId = localStorage.getItem('user_id');
    const userEmail = localStorage.getItem('user_email');
    const userFullName = localStorage.getItem('user_full_name');
    
    if (!userRole) {
        return null;
    }
    
    return {
        id: userId,
        email: userEmail,
        full_name: userFullName,
        role: userRole,
        company_slug: companySlug
    };
}

/**
 * Handle login form submission
 */
async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const submitButton = event.target.querySelector('button[type="submit"]');
    const errorElement = document.getElementById('error-message');
    
    // Clear previous errors
    if (errorElement) {
        errorElement.classList.remove('active');
    }
    
    // Set loading state
    setButtonLoading(submitButton, true);
    
    try {
        // Create FormData for OAuth2 password flow
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);
        
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Login failed');
        }
        
        // Store token and user info
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('user_role', data.user.role);
        localStorage.setItem('user_id', data.user.id);
        localStorage.setItem('user_email', data.user.email);
        localStorage.setItem('user_full_name', data.user.full_name);
        
        // Store company slug for company users
        if (data.user.company_id && data.user.role !== 'admin') {
            // Fetch company details to get slug
            const companyResponse = await apiRequest(`/admin/companies/${data.user.company_id}`, 'GET', null, true);
            if (companyResponse && companyResponse.slug) {
                localStorage.setItem('company_slug', companyResponse.slug);
            }
        }
        
        // Redirect based on role
        const redirectUrl = getRedirectUrl(data.user.role);
        window.location.href = redirectUrl;
        
    } catch (error) {
        setButtonLoading(submitButton, false);
        showError(error.message, 'error-message');
    }
}

/**
 * Get redirect URL based on user role
 * @param {string} role - User role
 * @returns {string} Redirect URL
 */
function getRedirectUrl(role) {
    // Check if there's a saved redirect URL
    const savedRedirect = localStorage.getItem('redirect_after_login');
    if (savedRedirect && savedRedirect !== '/auth/login.html') {
        localStorage.removeItem('redirect_after_login');
        return savedRedirect;
    }
    
    // Default redirects based on role
    if (role === 'admin') {
        return '/admin/index.html';
    } else {
        // For company users, redirect to company dashboard
        const companySlug = localStorage.getItem('company_slug');
        if (companySlug) {
            return `/${companySlug}/index.html`;
        }
        // Fallback
        return '/auth/login.html';
    }
}

/**
 * Handle logout
 */
async function handleLogout(event) {
    if (event) {
        event.preventDefault();
    }
    
    try {
        // Call logout endpoint (optional)
        await apiRequest('/auth/logout', 'POST');
    } catch (error) {
        console.error('Logout error:', error);
    } finally {
        // Clear all stored data
        localStorage.clear();
        
        // Redirect to login
        window.location.href = '/auth/login.html';
    }
}

/**
 * Toggle password visibility
 */
function togglePasswordVisibility(inputId, buttonId) {
    const input = document.getElementById(inputId);
    const button = document.getElementById(buttonId);
    
    if (input.type === 'password') {
        input.type = 'text';
        button.innerHTML = '👁️';
    } else {
        input.type = 'password';
        button.innerHTML = '👁️';
    }
}

/**
 * Initialize authentication on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    // Check authentication for non-auth pages
    checkAuth();
    
    // Setup login form if on login page
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Setup logout buttons
    const logoutButtons = document.querySelectorAll('[data-action="logout"]');
    logoutButtons.forEach(button => {
        button.addEventListener('click', handleLogout);
    });
    
    // Setup password toggle buttons
    const passwordToggle = document.getElementById('password-toggle');
    if (passwordToggle) {
        passwordToggle.addEventListener('click', () => {
            togglePasswordVisibility('password', 'password-toggle');
        });
    }
});
