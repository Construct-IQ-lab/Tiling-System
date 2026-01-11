// Company Projects Management

let projects = [];

/**
 * Load company projects
 */
async function loadCompanyProjects() {
    const companySlug = getCompanySlugFromUrl() || localStorage.getItem('company_slug');
    
    if (!companySlug) {
        showError('Company not found');
        return;
    }
    
    try {
        projects = await apiRequest(`/companies/${companySlug}/projects`, 'GET', null, true);
        displayProjects(projects);
    } catch (error) {
        console.error('Error loading projects:', error);
        showError('Failed to load projects');
    }
}

/**
 * Display projects in grid
 * @param {Array} projectsToDisplay - Array of project objects
 */
function displayProjects(projectsToDisplay) {
    const grid = document.getElementById('projects-grid');
    if (!grid) return;
    
    if (projectsToDisplay.length === 0) {
        grid.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📋</div>
                <h3 class="empty-title">No Projects Yet</h3>
                <p class="empty-text">Get started by creating your first project</p>
                <button class="btn btn-company-primary" onclick="showCreateProjectForm()">Create Project</button>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = projectsToDisplay.map(project => `
        <div class="project-card">
            <div class="project-header">
                <h3 class="project-name">${escapeHtml(project.name)}</h3>
                <span class="badge badge-${project.status}">${project.status.replace('_', ' ')}</span>
            </div>
            ${project.description ? `
                <p class="project-description">${escapeHtml(project.description)}</p>
            ` : ''}
            <div class="project-meta">
                <div class="project-meta-item">
                    <span class="meta-label">Client</span>
                    <span class="meta-value">${escapeHtml(project.client_name || 'N/A')}</span>
                </div>
                <div class="project-meta-item">
                    <span class="meta-label">Area</span>
                    <span class="meta-value">${project.area ? project.area + ' m²' : 'N/A'}</span>
                </div>
                <div class="project-meta-item">
                    <span class="meta-label">Budget</span>
                    <span class="meta-value">${project.budget ? formatCurrency(project.budget) : 'N/A'}</span>
                </div>
                <div class="project-meta-item">
                    <span class="meta-label">Created</span>
                    <span class="meta-value">${formatDate(project.created_at)}</span>
                </div>
            </div>
            <div class="project-footer">
                <button class="btn btn-sm btn-company-primary" onclick="viewProject(${project.id})">View Details</button>
            </div>
        </div>
    `).join('');
}

/**
 * Show create project form modal
 */
function showCreateProjectForm() {
    const modal = document.getElementById('project-modal');
    const form = document.getElementById('project-form');
    const modalTitle = document.getElementById('project-modal-title');
    
    if (modal && form && modalTitle) {
        modalTitle.textContent = 'Create New Project';
        form.reset();
        form.dataset.mode = 'create';
        form.dataset.projectId = '';
        modal.classList.add('active');
    }
}

/**
 * Hide project form modal
 */
function hideProjectForm() {
    const modal = document.getElementById('project-modal');
    if (modal) {
        modal.classList.remove('active');
    }
}

/**
 * Handle project form submission
 */
async function handleProjectSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitButton = form.querySelector('button[type="submit"]');
    const companySlug = getCompanySlugFromUrl() || localStorage.getItem('company_slug');
    
    const projectData = {
        name: form.name.value,
        description: form.description.value || null,
        client_name: form.client_name.value || null,
        client_contact: form.client_contact.value || null,
        client_address: form.client_address.value || null,
        area: form.area.value ? parseFloat(form.area.value) : null,
        budget: form.budget.value ? parseFloat(form.budget.value) : null
    };
    
    setButtonLoading(submitButton, true);
    
    try {
        // Note: This endpoint needs to be implemented in the backend
        await apiRequest(`/companies/${companySlug}/projects`, 'POST', projectData, true);
        showSuccess('Project created successfully');
        hideProjectForm();
        loadCompanyProjects();
        
    } catch (error) {
        console.error('Error saving project:', error);
        showError(error.message || 'Failed to create project. This feature is still in development.');
    } finally {
        setButtonLoading(submitButton, false);
    }
}

/**
 * View project details (placeholder)
 */
function viewProject(id) {
    showError('Project details view coming soon');
}

/**
 * Get company slug from URL pathname
 * @returns {string|null} Company slug or null
 */
function getCompanySlugFromUrl() {
    const pathname = window.location.pathname;
    
    // Pattern: /{company-slug}/page.html
    const match = pathname.match(/^\/([^\/]+)\//);
    if (match && match[1] !== 'admin' && match[1] !== 'auth' && match[1] !== 'frontend') {
        return match[1];
    }
    
    return null;
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
 * Initialize projects page
 */
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes('projects.html') && !window.location.pathname.includes('/admin/')) {
        loadCompanyProjects();
        
        // Setup form submission
        const form = document.getElementById('project-form');
        if (form) {
            form.addEventListener('submit', handleProjectSubmit);
        }
        
        // Setup modal close buttons
        const closeButtons = document.querySelectorAll('[data-action="close-project-modal"]');
        closeButtons.forEach(button => {
            button.addEventListener('click', hideProjectForm);
        });
        
        // Close modal when clicking outside
        const modal = document.getElementById('project-modal');
        if (modal) {
            modal.addEventListener('click', (event) => {
                if (event.target === modal) {
                    hideProjectForm();
                }
            });
        }
    }
});
