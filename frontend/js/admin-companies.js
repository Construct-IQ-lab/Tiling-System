// Admin Companies Management

let companies = [];

/**
 * Load and display all companies
 */
async function loadCompanies() {
    try {
        const loadingEl = document.getElementById('loading');
        if (loadingEl) loadingEl.style.display = 'block';
        
        companies = await adminAPI.getCompanies();
        displayCompanies(companies);
        
        if (loadingEl) loadingEl.style.display = 'none';
    } catch (error) {
        console.error('Failed to load companies:', error);
        showError('Failed to load companies');
    }
}

/**
 * Display companies in grid
 */
function displayCompanies(companiesData) {
    const container = document.getElementById('companies-grid');
    if (!container) return;
    
    if (companiesData.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🏢</div>
                <div class="empty-state-text">No companies found</div>
                <button class="btn btn-primary" onclick="showCreateForm()">Create First Company</button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = companiesData.map(company => `
        <div class="entity-card">
            <div class="entity-header">
                <div>
                    <div class="entity-title">${company.name}</div>
                    <div style="font-size: 14px; color: #666;">/${company.slug}</div>
                </div>
                <span class="badge badge-${getStatusBadgeClass(company.status)}">${company.status}</span>
            </div>
            <div class="entity-info">
                <div class="entity-info-item">
                    <strong>Email:</strong> ${company.email}
                </div>
                ${company.phone ? `<div class="entity-info-item"><strong>Phone:</strong> ${company.phone}</div>` : ''}
                ${company.address ? `<div class="entity-info-item"><strong>Address:</strong> ${company.address}</div>` : ''}
                <div class="entity-info-item">
                    <strong>Plan:</strong> ${company.subscription_plan}
                </div>
            </div>
            <div class="entity-actions">
                <button class="btn btn-sm btn-primary" onclick="editCompany('${company.id}')">Edit</button>
                <button class="btn btn-sm btn-danger" onclick="deleteCompany('${company.id}', '${company.name}')">Delete</button>
            </div>
        </div>
    `).join('');
}

/**
 * Get badge class for status
 */
function getStatusBadgeClass(status) {
    const classes = {
        'active': 'success',
        'suspended': 'warning',
        'archived': 'secondary'
    };
    return classes[status] || 'secondary';
}

/**
 * Show create company form
 */
function showCreateForm() {
    document.getElementById('modal-title').textContent = 'Create New Company';
    document.getElementById('company-form').reset();
    document.getElementById('company-id').value = '';
    document.getElementById('company-modal').classList.add('active');
}

/**
 * Hide create company form
 */
function hideCreateForm() {
    document.getElementById('company-modal').classList.remove('active');
}

/**
 * Auto-generate slug from company name
 */
function autoGenerateSlug() {
    const nameInput = document.getElementById('company-name');
    const slugInput = document.getElementById('company-slug');
    
    if (nameInput && slugInput) {
        nameInput.addEventListener('input', () => {
            slugInput.value = generateSlug(nameInput.value);
        });
    }
}

/**
 * Handle company form submission
 */
async function handleCompanySubmit(event) {
    event.preventDefault();
    
    const companyId = document.getElementById('company-id').value;
    const formData = {
        name: document.getElementById('company-name').value,
        slug: document.getElementById('company-slug').value,
        email: document.getElementById('company-email').value,
        phone: document.getElementById('company-phone').value || null,
        address: document.getElementById('company-address').value || null,
        primary_color: document.getElementById('company-primary-color').value,
        secondary_color: document.getElementById('company-secondary-color').value,
        subscription_plan: document.getElementById('company-plan').value
    };
    
    try {
        if (companyId) {
            // Update existing company
            await adminAPI.updateCompany(companyId, formData);
        } else {
            // Create new company
            await adminAPI.createCompany(formData);
        }
        
        hideCreateForm();
        await loadCompanies();
    } catch (error) {
        console.error('Failed to save company:', error);
        showError(error.message || 'Failed to save company');
    }
}

/**
 * Edit company
 */
async function editCompany(id) {
    try {
        const company = await adminAPI.getCompany(id);
        
        document.getElementById('modal-title').textContent = 'Edit Company';
        document.getElementById('company-id').value = company.id;
        document.getElementById('company-name').value = company.name;
        document.getElementById('company-slug').value = company.slug;
        document.getElementById('company-email').value = company.email;
        document.getElementById('company-phone').value = company.phone || '';
        document.getElementById('company-address').value = company.address || '';
        document.getElementById('company-primary-color').value = company.primary_color;
        document.getElementById('company-secondary-color').value = company.secondary_color;
        document.getElementById('company-plan').value = company.subscription_plan;
        
        document.getElementById('company-modal').classList.add('active');
    } catch (error) {
        console.error('Failed to load company:', error);
        showError('Failed to load company details');
    }
}

/**
 * Delete company
 */
async function deleteCompany(id, name) {
    if (!confirm(`Are you sure you want to archive ${name}? This will set the company status to archived.`)) {
        return;
    }
    
    try {
        await adminAPI.deleteCompany(id);
        await loadCompanies();
    } catch (error) {
        console.error('Failed to delete company:', error);
        showError('Failed to archive company');
    }
}

// Initialize when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        loadCompanies();
        autoGenerateSlug();
    });
} else {
    loadCompanies();
    autoGenerateSlug();
}
