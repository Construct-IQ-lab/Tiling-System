/**
 * Admin Users Management Script
 */

let users = [];
let companies = [];

/**
 * Load all users
 */
async function loadUsers() {
    try {
        showLoading('users-container');
        
        users = await get('/admin/users');
        
        displayUsers(users);
        
    } catch (error) {
        console.error('Error loading users:', error);
        showError('users-container', 'Failed to load users');
        showToast('Failed to load users', 'error');
    }
}

/**
 * Load companies for dropdown
 */
async function loadCompaniesDropdown() {
    try {
        companies = await get('/admin/companies');
        
        const select = document.getElementById('user-company');
        select.innerHTML = '<option value="">Select Company (Optional for Admin)</option>' +
            companies.map(company => 
                `<option value="${company.id}">${company.name}</option>`
            ).join('');
        
    } catch (error) {
        console.error('Error loading companies:', error);
        showToast('Failed to load companies', 'error');
    }
}

/**
 * Display users in table
 * @param {Array} usersList - List of users
 */
function displayUsers(usersList) {
    const container = document.getElementById('users-container');
    
    if (usersList.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">👤</div>
                <div class="empty-state-title">No Users Found</div>
                <div class="empty-state-text">Get started by creating your first user</div>
                <button onclick="showCreateModal()" class="btn btn-primary">Add New User</button>
            </div>
        `;
        return;
    }
    
    const html = `
        <table class="users-table">
            <thead>
                <tr>
                    <th>User</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Company</th>
                    <th>Status</th>
                    <th>Created</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${usersList.map(user => `
                    <tr>
                        <td>
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <div class="user-avatar">
                                    ${getInitials(user.first_name, user.last_name)}
                                </div>
                                <div>
                                    <strong>${user.first_name} ${user.last_name}</strong>
                                </div>
                            </div>
                        </td>
                        <td>${user.email}</td>
                        <td>${user.role.toUpperCase()}</td>
                        <td>${user.company_id ? getCompanyName(user.company_id) : 'N/A'}</td>
                        <td>${user.is_active ? getStatusBadge('active') : getStatusBadge('suspended')}</td>
                        <td>${formatDate(user.created_at)}</td>
                        <td>
                            <div class="actions">
                                <button onclick="viewUser(${user.id})" class="btn btn-sm btn-primary">
                                    View
                                </button>
                            </div>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    
    container.innerHTML = html;
}

/**
 * Get company name by ID
 * @param {number} companyId - Company ID
 * @returns {string} Company name
 */
function getCompanyName(companyId) {
    const company = companies.find(c => c.id === companyId);
    return company ? company.name : 'Unknown';
}

/**
 * Show create user modal
 */
function showCreateModal() {
    const modal = document.getElementById('create-modal');
    modal.classList.add('active');
    
    // Reset form
    document.getElementById('user-form').reset();
    
    // Load companies dropdown
    if (companies.length === 0) {
        loadCompaniesDropdown();
    }
}

/**
 * Hide create user modal
 */
function hideCreateModal() {
    const modal = document.getElementById('create-modal');
    modal.classList.remove('active');
}

/**
 * Handle role change to show/hide company field
 */
function handleRoleChange() {
    const role = document.getElementById('user-role').value;
    const companyGroup = document.getElementById('company-group');
    const companySelect = document.getElementById('user-company');
    
    if (role === 'admin') {
        companyGroup.style.display = 'none';
        companySelect.required = false;
    } else {
        companyGroup.style.display = 'block';
        companySelect.required = true;
    }
}

/**
 * Handle user form submission
 */
async function handleUserFormSubmit(e) {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submit-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Creating...';
    
    try {
        const role = document.getElementById('user-role').value;
        const companyId = document.getElementById('user-company').value;
        
        const formData = {
            email: document.getElementById('user-email').value,
            password: document.getElementById('user-password').value,
            first_name: document.getElementById('user-first-name').value,
            last_name: document.getElementById('user-last-name').value,
            role: role,
            company_id: companyId ? parseInt(companyId) : null,
        };
        
        await post('/admin/users', formData);
        showToast('User created successfully', 'success');
        
        // Reload users and close modal
        await loadUsers();
        hideCreateModal();
        
    } catch (error) {
        console.error('Error creating user:', error);
        showToast(error.message || 'Failed to create user', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Create User';
    }
}

/**
 * View user details
 * @param {number} userId - User ID
 */
function viewUser(userId) {
    const user = users.find(u => u.id === userId);
    if (!user) return;
    
    alert(`User Details:\n\nName: ${user.first_name} ${user.last_name}\nEmail: ${user.email}\nRole: ${user.role}\nCompany ID: ${user.company_id || 'N/A'}\nStatus: ${user.is_active ? 'Active' : 'Inactive'}\nCreated: ${formatDateTime(user.created_at)}`);
}

/**
 * Initialize users page
 */
function initUsersPage() {
    // Highlight active nav item
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        if (link.href.includes('users.html')) {
            link.classList.add('active');
        }
    });
    
    // Setup event listeners
    document.getElementById('add-user-btn').addEventListener('click', showCreateModal);
    document.getElementById('user-form').addEventListener('submit', handleUserFormSubmit);
    document.getElementById('cancel-btn').addEventListener('click', hideCreateModal);
    document.querySelector('.close').addEventListener('click', hideCreateModal);
    document.getElementById('user-role').addEventListener('change', handleRoleChange);
    
    // Close modal on outside click
    document.getElementById('create-modal').addEventListener('click', (e) => {
        if (e.target.id === 'create-modal') {
            hideCreateModal();
        }
    });
    
    // Load data
    loadUsers();
    loadCompaniesDropdown();
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initUsersPage);
