/**
 * Admin Companies Management Script
 */

let companies = [];

/**
 * Load all companies
 */
async function loadCompanies() {
    try {
        showLoading('companies-container');
        
        companies = await get('/admin/companies');
        
        displayCompanies(companies);
        
    } catch (error) {
        console.error('Error loading companies:', error);
        showError('companies-container', 'Failed to load companies');
        showToast('Failed to load companies', 'error');
    }
}

/**
 * Display companies in grid
 * @param {Array} companiesList - List of companies
 */
function displayCompanies(companiesList) {
    const container = document.getElementById('companies-container');
    
    if (companiesList.length === 0) {
        container.innerHTML = `
            <div class="empty-state" style="grid-column: 1 / -1;">
                <div class="empty-state-icon">🏢</div>
                <div class="empty-state-title">No Companies Found</div>
                <div class="empty-state-text">Get started by creating your first company</div>
                <button onclick="showCreateModal()" class="btn btn-primary">Add New Company</button>
            </div>
        `;
        return;
    }
    
    const html = companiesList.map(company => `
        <div class="company-card">
            <div class="company-card-header">
                <div>
                    <h3 class="company-card-title">${company.name}</h3>
                    <div class="company-card-slug">/${company.slug}</div>
                </div>
                ${getStatusBadge(company.status)}
            </div>
            
            <div class="company-card-body">
                <p>📧 ${company.email || 'N/A'}</p>
                <p>📱 ${company.phone || 'N/A'}</p>
                <p>📅 Created: ${formatDate(company.created_at)}</p>
                <p>💼 Plan: ${company.subscription_plan}</p>
            </div>
            
            <div class="company-card-footer">
                <button onclick="editCompany(${company.id})" class="btn btn-sm btn-primary">
                    Edit
                </button>
                <button onclick="deleteCompany(${company.id}, '${company.name}')" class="btn btn-sm btn-danger">
                    Delete
                </button>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

/**
 * Show create company modal
 */
function showCreateModal() {
    const modal = document.getElementById('create-modal');
    modal.classList.add('active');
    
    // Reset form
    document.getElementById('company-form').reset();
    document.getElementById('company-id').value = '';
    document.getElementById('modal-title').textContent = 'Add New Company';
}

/**
 * Hide create company modal
 */
function hideCreateModal() {
    const modal = document.getElementById('create-modal');
    modal.classList.remove('active');
}

/**
 * Auto-generate slug from company name
 */
function setupSlugGeneration() {
    const nameInput = document.getElementById('company-name');
    const slugInput = document.getElementById('company-slug');
    
    nameInput.addEventListener('input', (e) => {
        if (!slugInput.dataset.manuallyEdited) {
            slugInput.value = generateSlug(e.target.value);
        }
    });
    
    // Mark slug as manually edited if user types in it
    slugInput.addEventListener('input', () => {
        slugInput.dataset.manuallyEdited = 'true';
    });
}

/**
 * Handle company form submission
 */
async function handleCompanyFormSubmit(e) {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submit-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Saving...';
    
    try {
        const companyId = document.getElementById('company-id').value;
        const formData = {
            name: document.getElementById('company-name').value,
            slug: document.getElementById('company-slug').value,
            email: document.getElementById('company-email').value,
            phone: document.getElementById('company-phone').value,
            address: document.getElementById('company-address').value,
            primary_color: document.getElementById('primary-color').value,
            secondary_color: document.getElementById('secondary-color').value,
        };
        
        if (companyId) {
            // Update existing company
            await put(`/admin/companies/${companyId}`, formData);
            showToast('Company updated successfully', 'success');
        } else {
            // Create new company
            await post('/admin/companies', formData);
            showToast('Company created successfully', 'success');
        }
        
        // Reload companies and close modal
        await loadCompanies();
        hideCreateModal();
        
    } catch (error) {
        console.error('Error saving company:', error);
        showToast(error.message || 'Failed to save company', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = companyId ? 'Update Company' : 'Create Company';
    }
}

/**
 * Edit company
 * @param {number} companyId - Company ID
 */
async function editCompany(companyId) {
    try {
        const company = await get(`/admin/companies/${companyId}`);
        
        // Fill form with company data
        document.getElementById('company-id').value = company.id;
        document.getElementById('company-name').value = company.name;
        document.getElementById('company-slug').value = company.slug;
        document.getElementById('company-email').value = company.email || '';
        document.getElementById('company-phone').value = company.phone || '';
        document.getElementById('company-address').value = company.address || '';
        document.getElementById('primary-color').value = company.primary_color;
        document.getElementById('secondary-color').value = company.secondary_color;
        
        // Mark slug as manually edited
        document.getElementById('company-slug').dataset.manuallyEdited = 'true';
        
        // Update modal title
        document.getElementById('modal-title').textContent = 'Edit Company';
        
        // Show modal
        showCreateModal();
        
    } catch (error) {
        console.error('Error loading company:', error);
        showToast('Failed to load company details', 'error');
    }
}

/**
 * Delete company
 * @param {number} companyId - Company ID
 * @param {string} companyName - Company name
 */
async function deleteCompany(companyId, companyName) {
    if (!confirm(`Are you sure you want to delete "${companyName}"? This will delete all associated data including users and projects.`)) {
        return;
    }
    
    try {
        await deleteRequest(`/admin/companies/${companyId}`);
        showToast('Company deleted successfully', 'success');
        await loadCompanies();
    } catch (error) {
        console.error('Error deleting company:', error);
        showToast(error.message || 'Failed to delete company', 'error');
    }
}

/**
 * Initialize companies page
 */
function initCompaniesPage() {
    // Highlight active nav item
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        if (link.href.includes('companies.html')) {
            link.classList.add('active');
        }
    });
    
    // Setup event listeners
    document.getElementById('add-company-btn').addEventListener('click', showCreateModal);
    document.getElementById('company-form').addEventListener('submit', handleCompanyFormSubmit);
    document.getElementById('cancel-btn').addEventListener('click', hideCreateModal);
    document.querySelector('.close').addEventListener('click', hideCreateModal);
    
    // Close modal on outside click
    document.getElementById('create-modal').addEventListener('click', (e) => {
        if (e.target.id === 'create-modal') {
            hideCreateModal();
        }
    });
    
    // Setup slug generation
    setupSlugGeneration();
    
    // Load companies
    loadCompanies();
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initCompaniesPage);
