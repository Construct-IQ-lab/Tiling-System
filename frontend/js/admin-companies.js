// Admin Companies Management JavaScript

const API_URL = 'http://localhost:8000';

// HTML Escape function to prevent XSS
function escapeHtml(text) {
    if (text === null || text === undefined) {
        return '';
    }
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Generate slug from company name
function generateSlug(name) {
    return name
        .toLowerCase()
        .replace(/[^a-z0-9\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .trim();
}

// Load companies list
async function loadCompanies() {
    const token = localStorage.getItem('token');
    const grid = document.getElementById('companiesGrid');
    
    try {
        const response = await fetch(`${API_URL}/api/admin/companies`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to load companies');
        }
        
        const companies = await response.json();
        
        if (companies.length === 0) {
            grid.innerHTML = '<div class="loading-spinner">No companies found. Create your first company!</div>';
            return;
        }
        
        // Render companies
        grid.innerHTML = companies.map(company => `
            <div class="company-card">
                <div class="company-header">
                    <div>
                        <div class="company-name">${escapeHtml(company.name)}</div>
                        <div class="company-slug">/${escapeHtml(company.slug)}/</div>
                    </div>
                    <span class="status-badge ${escapeHtml(company.status)}">${escapeHtml(company.status)}</span>
                </div>
                <div class="company-info">
                    <p><strong>Email:</strong> ${escapeHtml(company.email)}</p>
                    ${company.phone ? `<p><strong>Phone:</strong> ${escapeHtml(company.phone)}</p>` : ''}
                    <p><strong>Plan:</strong> ${escapeHtml(company.subscription_plan)}</p>
                </div>
                <div class="company-stats">
                    <div class="company-stat">
                        <div class="company-stat-value">${company.user_count || 0}</div>
                        <div class="company-stat-label">Users</div>
                    </div>
                    <div class="company-stat">
                        <div class="company-stat-value">${company.project_count || 0}</div>
                        <div class="company-stat-label">Projects</div>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading companies:', error);
        grid.innerHTML = '<div class="loading-spinner">Error loading companies</div>';
    }
}

// Show create company modal
function showCreateModal() {
    const modal = document.getElementById('createCompanyModal');
    modal.style.display = 'flex';
}

// Hide create company modal
function hideCreateModal() {
    const modal = document.getElementById('createCompanyModal');
    modal.style.display = 'none';
    document.getElementById('createCompanyForm').reset();
    document.getElementById('formError').style.display = 'none';
}

// Create company
async function createCompany(formData) {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/api/admin/companies`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to create company');
        }
        
        return data;
    } catch (error) {
        throw error;
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
    await loadCompanies();
    
    // Auto-generate slug from name
    const nameInput = document.getElementById('companyName');
    const slugInput = document.getElementById('companySlug');
    
    nameInput.addEventListener('input', (e) => {
        const slug = generateSlug(e.target.value);
        slugInput.value = slug;
    });
    
    // Show modal on button click
    document.getElementById('createCompanyButton').addEventListener('click', showCreateModal);
    
    // Hide modal on close button
    document.getElementById('closeModalButton').addEventListener('click', hideCreateModal);
    document.getElementById('cancelButton').addEventListener('click', hideCreateModal);
    
    // Hide modal on outside click
    document.getElementById('createCompanyModal').addEventListener('click', (e) => {
        if (e.target.id === 'createCompanyModal') {
            hideCreateModal();
        }
    });
    
    // Handle form submission
    document.getElementById('createCompanyForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formError = document.getElementById('formError');
        const submitButton = document.getElementById('submitButton');
        
        formError.style.display = 'none';
        submitButton.disabled = true;
        submitButton.textContent = 'Creating...';
        
        const formData = {
            name: document.getElementById('companyName').value,
            slug: document.getElementById('companySlug').value,
            email: document.getElementById('companyEmail').value,
            phone: document.getElementById('companyPhone').value || null,
            address: document.getElementById('companyAddress').value || null,
            logo_url: document.getElementById('logoUrl').value || null,
            primary_color: document.getElementById('primaryColor').value,
            secondary_color: document.getElementById('secondaryColor').value
        };
        
        try {
            await createCompany(formData);
            hideCreateModal();
            await loadCompanies();
        } catch (error) {
            console.error('Error creating company:', error);
            formError.textContent = error.message;
            formError.style.display = 'block';
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = 'Create Company';
        }
    });
});
