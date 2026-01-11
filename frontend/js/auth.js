// Authentication Helper Functions

/**
 * Check if user is authenticated
 * Redirects to login if not authenticated
 */
function checkAuth() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/frontend/auth/login.html';
        return false;
    }
    return true;
}

/**
 * Get current user role
 */
function getUserRole() {
    return localStorage.getItem('user_role');
}

/**
 * Get current user's company slug
 */
function getCompanySlug() {
    return localStorage.getItem('company_slug');
}

/**
 * Handle login form submission
 */
async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('error-message');
    const submitBtn = event.target.querySelector('button[type="submit"]');
    
    // Disable submit button
    submitBtn.disabled = true;
    submitBtn.textContent = 'Logging in...';
    
    // Hide previous errors
    if (errorDiv) {
        errorDiv.classList.remove('active');
    }
    
    try {
        const response = await authAPI.login(email, password);
        
        // Store authentication data
        localStorage.setItem('access_token', response.access_token);
        localStorage.setItem('user_role', response.user.role);
        localStorage.setItem('user_id', response.user.id);
        localStorage.setItem('user_email', response.user.email);
        localStorage.setItem('user_name', `${response.user.first_name} ${response.user.last_name}`);
        
        if (response.user.company_slug) {
            localStorage.setItem('company_slug', response.user.company_slug);
        }
        
        // Redirect based on role
        if (response.user.role === 'admin') {
            window.location.href = '/frontend/admin/index.html';
        } else {
            const slug = response.user.company_slug;
            if (slug) {
                window.location.href = `/frontend/company/index.html?slug=${slug}`;
            } else {
                throw new Error('Company information not found');
            }
        }
    } catch (error) {
        console.error('Login error:', error);
        if (errorDiv) {
            errorDiv.textContent = error.message || 'Login failed. Please check your credentials.';
            errorDiv.classList.add('active');
        }
        
        // Re-enable submit button
        submitBtn.disabled = false;
        submitBtn.textContent = 'Sign In';
    }
}

/**
 * Handle logout
 */
async function handleLogout() {
    try {
        await authAPI.logout();
    } catch (error) {
        console.error('Logout error:', error);
    } finally {
        // Clear local storage regardless of API call result
        localStorage.clear();
        window.location.href = '/frontend/auth/login.html';
    }
}

/**
 * Initialize auth check on page load
 * Call this on non-auth pages
 */
function initAuthCheck() {
    // Don't check auth on login page
    if (window.location.pathname.includes('/auth/')) {
        return;
    }
    
    checkAuth();
}

// Auto-check auth when script loads on non-auth pages
if (!window.location.pathname.includes('/auth/')) {
    checkAuth();
}
