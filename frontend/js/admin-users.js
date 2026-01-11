// Admin Users Management

let users = [];
let companies = [];

/**
 * Load all users
 */
async function loadUsers() {
    try {
        users = await apiRequest('/admin/users', 'GET', null, true);
        displayUsers(users);
    } catch (error) {
        console.error('Error loading users:', error);
        showError('Failed to load users');
    }
}

/**
 * Load companies for dropdown
 */
async function loadCompaniesDropdown() {
    try {
        companies = await apiRequest('/admin/companies', 'GET', null, true);
        populateCompaniesDropdown();
    } catch (error) {
        console.error('Error loading companies:', error);
        showError('Failed to load companies');
    }
}

/**
 * Populate companies dropdown
 */
function populateCompaniesDropdown() {
    const select = document.getElementById('user-company');
    if (!select) return;
    
    select.innerHTML = '<option value="">None (Admin user)</option>' +
        companies.map(company => 
            `<option value="${company.id}">${escapeHtml(company.name)}</option>`
        ).join('');
}

/**
 * Display users in grid
 * @param {Array} usersToDisplay - Array of user objects
 */
function displayUsers(usersToDisplay) {
    const grid = document.getElementById('users-grid');
    if (!grid) return;
    
    if (usersToDisplay.length === 0) {
        grid.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">👥</div>
                <h3 class="empty-title">No Users Yet</h3>
                <p class="empty-text">Get started by creating your first user</p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = usersToDisplay.map(user => {
        const company = companies.find(c => c.id === user.company_id);
        
        return `
            <div class="user-card">
                <div class="user-info">
                    <div class="user-name">${escapeHtml(user.first_name)} ${escapeHtml(user.last_name)}</div>
                    <div class="user-meta">
                        <span class="user-meta-item">📧 ${escapeHtml(user.email)}</span>
                        ${company ? `<span class="user-meta-item">🏢 ${escapeHtml(company.name)}</span>` : ''}
                        <span class="user-meta-item">🔑 ${user.role}</span>
                        <span class="badge badge-${user.is_active ? 'active' : 'suspended'}">
                            ${user.is_active ? 'Active' : 'Inactive'}
                        </span>
                    </div>
                </div>
                <div class="user-actions">
                    <button class="btn btn-sm btn-primary" onclick="editUser(${user.id})">Edit</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteUser(${user.id})">Delete</button>
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Show create user form modal
 */
function showCreateUserForm() {
    const modal = document.getElementById('user-modal');
    const form = document.getElementById('user-form');
    const modalTitle = document.getElementById('user-modal-title');
    const passwordGroup = document.getElementById('password-group');
    
    if (modal && form && modalTitle) {
        modalTitle.textContent = 'Create New User';
        form.reset();
        form.dataset.mode = 'create';
        form.dataset.userId = '';
        
        // Show password field for new users
        if (passwordGroup) {
            passwordGroup.style.display = 'block';
            passwordGroup.querySelector('input').required = true;
        }
        
        modal.classList.add('active');
    }
}

/**
 * Hide user form modal
 */
function hideUserForm() {
    const modal = document.getElementById('user-modal');
    if (modal) {
        modal.classList.remove('active');
    }
}

/**
 * Handle user form submission
 */
async function handleUserSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitButton = form.querySelector('button[type="submit"]');
    
    const userData = {
        email: form.email.value,
        first_name: form.first_name.value,
        last_name: form.last_name.value,
        role: form.role.value,
        company_id: form.company_id.value ? parseInt(form.company_id.value) : null
    };
    
    // Add password for new users
    if (form.dataset.mode === 'create') {
        userData.password = form.password.value;
    }
    
    setButtonLoading(submitButton, true);
    
    try {
        const mode = form.dataset.mode;
        const userId = form.dataset.userId;
        
        if (mode === 'create') {
            await apiRequest('/admin/users', 'POST', userData, true);
            showSuccess('User created successfully');
        } else {
            await apiRequest(`/admin/users/${userId}`, 'PUT', userData, true);
            showSuccess('User updated successfully');
        }
        
        hideUserForm();
        loadUsers();
        
    } catch (error) {
        console.error('Error saving user:', error);
        showError(error.message);
    } finally {
        setButtonLoading(submitButton, false);
    }
}

/**
 * Edit user (placeholder)
 */
async function editUser(id) {
    showError('Edit user functionality coming soon');
}

/**
 * Delete user
 */
async function deleteUser(id) {
    if (!confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
        return;
    }
    
    try {
        await apiRequest(`/admin/users/${id}`, 'DELETE', null, true);
        showSuccess('User deleted successfully');
        loadUsers();
    } catch (error) {
        console.error('Error deleting user:', error);
        showError(error.message);
    }
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Initialize users page
 */
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes('/admin/users.html')) {
        loadUsers();
        loadCompaniesDropdown();
        
        // Setup form submission
        const form = document.getElementById('user-form');
        if (form) {
            form.addEventListener('submit', handleUserSubmit);
        }
        
        // Setup modal close buttons
        const closeButtons = document.querySelectorAll('[data-action="close-user-modal"]');
        closeButtons.forEach(button => {
            button.addEventListener('click', hideUserForm);
        });
        
        // Close modal when clicking outside
        const modal = document.getElementById('user-modal');
        if (modal) {
            modal.addEventListener('click', (event) => {
                if (event.target === modal) {
                    hideUserForm();
                }
            });
        }
    }
});
