// Company Projects Management

let projects = [];

/**
 * Load and display company projects
 */
async function loadCompanyProjects() {
    const slug = getSlugFromURL();
    if (!slug) {
        showError('Company information not found');
        return;
    }
    
    try {
        const loadingEl = document.getElementById('loading');
        if (loadingEl) loadingEl.style.display = 'block';
        
        projects = await companyAPI.getProjects(slug);
        displayProjects(projects);
        
        if (loadingEl) loadingEl.style.display = 'none';
    } catch (error) {
        console.error('Failed to load projects:', error);
        showError('Failed to load projects');
    }
}

/**
 * Display projects in grid
 */
function displayProjects(projectsData) {
    const container = document.getElementById('projects-grid');
    if (!container) return;
    
    if (projectsData.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📋</div>
                <div class="empty-state-text">No projects found</div>
                <button class="btn btn-company-primary" onclick="showCreateProjectForm()">Create First Project</button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = projectsData.map(project => `
        <div class="project-card">
            <div class="project-header">
                <div class="project-title">${project.name}</div>
                <span class="project-status ${project.status}">${project.status.replace('_', ' ')}</span>
            </div>
            ${project.description ? `<p style="color: #666; font-size: 14px; margin-bottom: 15px;">${project.description}</p>` : ''}
            <div class="project-details">
                ${project.client_name ? `
                    <div class="project-detail">
                        <span class="project-detail-label">Client:</span>
                        <span class="project-detail-value">${project.client_name}</span>
                    </div>
                ` : ''}
                ${project.budget ? `
                    <div class="project-detail">
                        <span class="project-detail-label">Budget:</span>
                        <span class="project-detail-value">$${project.budget.toFixed(2)}</span>
                    </div>
                ` : ''}
                <div class="project-detail">
                    <span class="project-detail-label">Created:</span>
                    <span class="project-detail-value">${new Date(project.created_at).toLocaleDateString()}</span>
                </div>
            </div>
            <div class="project-actions">
                <button class="btn btn-sm btn-company-primary" onclick="viewProject('${project.id}')">View</button>
            </div>
        </div>
    `).join('');
}

/**
 * Show create project form
 */
function showCreateProjectForm() {
    document.getElementById('project-modal').classList.add('active');
}

/**
 * Hide create project form
 */
function hideCreateProjectForm() {
    document.getElementById('project-modal').classList.remove('active');
    document.getElementById('project-form').reset();
}

/**
 * Handle project form submission
 */
async function handleProjectSubmit(event) {
    event.preventDefault();
    
    const slug = getSlugFromURL();
    if (!slug) {
        showError('Company information not found');
        return;
    }
    
    const formData = {
        name: document.getElementById('project-name').value,
        description: document.getElementById('project-description').value || null,
        client_name: document.getElementById('project-client-name').value || null,
        client_email: document.getElementById('project-client-email').value || null,
        client_phone: document.getElementById('project-client-phone').value || null,
        budget: parseFloat(document.getElementById('project-budget').value) || null
    };
    
    try {
        await companyAPI.createProject(slug, formData);
        hideCreateProjectForm();
        await loadCompanyProjects();
    } catch (error) {
        console.error('Failed to create project:', error);
        showError(error.message || 'Failed to create project');
    }
}

/**
 * View project details
 */
function viewProject(id) {
    // For now, just alert. In a full implementation, this would show a detail view
    alert(`View project details for ID: ${id}\n\nFull project detail view would be implemented here.`);
}

// Initialize when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        initTheme().then(() => loadCompanyProjects());
    });
} else {
    initTheme().then(() => loadCompanyProjects());
}
