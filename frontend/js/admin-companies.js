// Admin Companies Management

let companies = [];

/**
 * Load all companies
 */
async function loadCompanies() {
    try {
        companies = await apiRequest('/admin/companies', 'GET', null, true);
        displayCompanies(companies);
    } catch (error) {
        console.error('Error loading companies:', error);
        showError('Failed to load companies');
    }
}

/**
 * Display companies in grid
 * @param {Array} companiesToDisplay - Array of company objects
 */
function displayCompanies(companiesToDisplay) {
    const grid = document.getElementById('companies-grid');
    if (!grid) return;
    
    if (companiesToDisplay.length === 0) {
        grid.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">🏢</div>
                <h3 class="empty-title">No Companies Yet</h3>
                <p class="empty-text">Get started by creating your first company</p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = companiesToDisplay.map(company => `
        <div class="company-card">
            <div class="company-header">
                <h3 class="company-name">${escapeHtml(company.name)}</h3>
                <span class="company-slug">/${company.slug}</span>
            </div>
            <div class="company-details">
                <div class="company-detail">
                    <span>📧</span>
                    <span>${escapeHtml(company.email)}</span>
                </div>
                ${company.phone ? `
                <div class="company-detail">
                    <span>📱</span>
                    <span>${escapeHtml(company.phone)}</span>
                </div>
                ` : ''}
            </div>
            <div class="company-footer">
                <span class="badge badge-${company.status}">${company.status}</span>
                <div class="company-actions">
                    <button class="btn btn-sm btn-primary" onclick="editCompany(${company.id})">Edit</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteCompany(${company.id})">Delete</button>
                </div>
            </div>
        </div>
    `).join('');
}

/**
 * Show create company form modal
 */
function showCreateForm() {
    const modal = document.getElementById('company-modal');
    const form = document.getElementById('company-form');
    const modalTitle = document.getElementById('modal-title');
    
    if (modal && form && modalTitle) {
        modalTitle.textContent = 'Create New Company';
        form.reset();
        form.dataset.mode = 'create';
        form.dataset.companyId = '';
        modal.classList.add('active');
    }
}

/**
 * Hide company form modal
 */
function hideCreateForm() {
    const modal = document.getElementById('company-modal');
    if (modal) {
        modal.classList.remove('active');
    }
}

/**
 * Handle company form submission
 */
async function handleCompanySubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitButton = form.querySelector('button[type="submit"]');
    
    const companyData = {
        name: form.name.value,
        slug: form.slug.value,
        email: form.email.value,
        phone: form.phone.value || null,
        address: form.address.value || null,
        primary_color: form.primary_color.value || '#3498db',
        secondary_color: form.secondary_color.value || '#2ecc71'
    };
    
    setButtonLoading(submitButton, true);
    
    try {
        const mode = form.dataset.mode;
        const companyId = form.dataset.companyId;
        
        if (mode === 'create') {
            await apiRequest('/admin/companies', 'POST', companyData, true);
            showSuccess('Company created successfully');
        } else {
            await apiRequest(`/admin/companies/${companyId}`, 'PUT', companyData, true);
            showSuccess('Company updated successfully');
        }
        
        hideCreateForm();
        loadCompanies();
        
    } catch (error) {
        console.error('Error saving company:', error);
        showError(error.message);
    } finally {
        setButtonLoading(submitButton, false);
    }
}

/**
 * Auto-generate slug from company name
 */
function setupSlugGeneration() {
    const nameInput = document.getElementById('company-name');
    const slugInput = document.getElementById('company-slug');
    
    if (nameInput && slugInput) {
        nameInput.addEventListener('input', () => {
            // Only auto-generate if slug is empty or hasn't been manually edited
            if (!slugInput.dataset.manuallyEdited) {
                slugInput.value = generateSlug(nameInput.value);
            }
        });
        
        // Mark slug as manually edited when user types in it
        slugInput.addEventListener('input', () => {
            slugInput.dataset.manuallyEdited = 'true';
        });
    }
}

/**
 * Edit company (placeholder)
 */
async function editCompany(id) {
    try {
        const company = await apiRequest(`/admin/companies/${id}`, 'GET', null, true);
        
        const modal = document.getElementById('company-modal');
        const form = document.getElementById('company-form');
        const modalTitle = document.getElementById('modal-title');
        
        if (modal && form && modalTitle) {
            modalTitle.textContent = 'Edit Company';
            form.dataset.mode = 'edit';
            form.dataset.companyId = id;
            
            // Populate form
            form.name.value = company.name;
            form.slug.value = company.slug;
            form.email.value = company.email;
            form.phone.value = company.phone || '';
            form.address.value = company.address || '';
            form.primary_color.value = company.primary_color;
            form.secondary_color.value = company.secondary_color;
            
            modal.classList.add('active');
        }
    } catch (error) {
        console.error('Error loading company:', error);
        showError('Failed to load company details');
    }
}

/**
 * Delete company
 */
async function deleteCompany(id) {
    if (!confirm('Are you sure you want to delete this company? This action cannot be undone.')) {
        return;
    }
    
    try {
        await apiRequest(`/admin/companies/${id}`, 'DELETE', null, true);
        showSuccess('Company deleted successfully');
        loadCompanies();
    } catch (error) {
        console.error('Error deleting company:', error);
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
 * Initialize companies page
 */
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes('/admin/companies.html')) {
        loadCompanies();
        setupSlugGeneration();
        
        // Setup form submission
        const form = document.getElementById('company-form');
        if (form) {
            form.addEventListener('submit', handleCompanySubmit);
        }
        
        // Setup modal close buttons
        const closeButtons = document.querySelectorAll('[data-action="close-modal"]');
        closeButtons.forEach(button => {
            button.addEventListener('click', hideCreateForm);
        });
        
        // Close modal when clicking outside
        const modal = document.getElementById('company-modal');
        if (modal) {
            modal.addEventListener('click', (event) => {
                if (event.target === modal) {
                    hideCreateForm();
                }
            });
        }
    }
});
