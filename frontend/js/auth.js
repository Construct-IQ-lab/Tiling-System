// Authentication JavaScript - Login/Logout and JWT Handling

const API_URL = 'http://localhost:8000';

// Check if user is authenticated
async function checkAuth() {
    const token = localStorage.getItem('token');
    const currentPath = window.location.pathname;
    
    // If no token and not on login page, redirect to login
    if (!token && !currentPath.includes('login.html')) {
        window.location.href = '/frontend/auth/login.html';
        return null;
    }
    
    // If token exists, verify it
    if (token) {
        try {
            const response = await fetch(`${API_URL}/api/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (!response.ok) {
                // Token invalid, clear and redirect to login
                localStorage.clear();
                if (!currentPath.includes('login.html')) {
                    window.location.href = '/frontend/auth/login.html';
                }
                return null;
            }
            
            const user = await response.json();
            localStorage.setItem('user', JSON.stringify(user));
            
            // Update user info in sidebar if element exists
            updateUserInfo(user);
            
            return user;
        } catch (error) {
            console.error('Auth check failed:', error);
            localStorage.clear();
            if (!currentPath.includes('login.html')) {
                window.location.href = '/frontend/auth/login.html';
            }
            return null;
        }
    }
    
    return null;
}

// Update user info display
function updateUserInfo(user) {
    const userInfoElement = document.getElementById('userInfo');
    if (userInfoElement) {
        const initial = user.username ? user.username.charAt(0).toUpperCase() : 'U';
        userInfoElement.innerHTML = `
            <div class="user-avatar">${initial}</div>
            <div class="user-details">
                <div class="user-name">${user.username}</div>
                <div class="user-email">${user.email}</div>
            </div>
        `;
    }
}

// Login form handler
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const errorMessage = document.getElementById('errorMessage');
        const loginButton = document.getElementById('loginButton');
        const buttonText = loginButton.querySelector('.button-text');
        const buttonLoader = loginButton.querySelector('.button-loader');
        
        // Hide error message
        errorMessage.style.display = 'none';
        
        // Show loading state
        loginButton.disabled = true;
        buttonText.style.display = 'none';
        buttonLoader.style.display = 'inline-block';
        
        try {
            const response = await fetch(`${API_URL}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || 'Login failed');
            }
            
            // Store token and user info
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            
            // Redirect based on role
            if (data.user.role === 'admin') {
                window.location.href = '/frontend/admin/index.html';
            } else {
                // Redirect to company dashboard
                const slug = data.user.company_slug;
                if (slug) {
                    window.location.href = '/frontend/company/index.html';
                } else {
                    throw new Error('No company associated with user');
                }
            }
        } catch (error) {
            console.error('Login error:', error);
            errorMessage.textContent = error.message;
            errorMessage.style.display = 'block';
            
            // Reset button state
            loginButton.disabled = false;
            buttonText.style.display = 'inline-block';
            buttonLoader.style.display = 'none';
        }
    });
}

// Logout handler
function setupLogout() {
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', async () => {
            const token = localStorage.getItem('token');
            
            try {
                await fetch(`${API_URL}/api/auth/logout`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
            } catch (error) {
                console.error('Logout error:', error);
            }
            
            // Clear local storage and redirect
            localStorage.clear();
            window.location.href = '/frontend/auth/login.html';
        });
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    setupLogout();
});
