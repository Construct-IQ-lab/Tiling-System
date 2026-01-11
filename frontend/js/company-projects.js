// Company Projects Management JavaScript

const API_URL = 'http://localhost:8000';

let currentFilter = 'all';

// Load projects
async function loadProjects(status = null) {
    const user = JSON.parse(localStorage.getItem('user'));
    const token = localStorage.getItem('token');
    const slug = user.company_slug;
    const grid = document.getElementById('projectsGrid');
    
    if (!slug) {
        grid.innerHTML = '<div class="loading-message">No company associated</div>';
        return;
    }
    
    try {
        let url = `${API_URL}/api/companies/${slug}/projects`;
        if (status && status !== 'all') {
            url += `?status=${status}`;
        }
        
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to load projects');
        }
        
        const projects = await response.json();
        
        if (projects.length === 0) {
            grid.innerHTML = '<div class="loading-message">No projects found. Create your first project!</div>';
            return;
        }
        
        // Render projects
        grid.innerHTML = projects.map(project => `
            <div class="project-card">
                <h3>${escapeHtml(project.name)}</h3>
                <p>${escapeHtml(project.description || 'No description')}</p>
                <div style="margin-top: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 13px; color: var(--company-text-muted);">Status:</span>
                        <span style="font-weight: 600; text-transform: capitalize;">${escapeHtml(project.status.replace('_', ' '))}</span>
                    </div>
                    ${project.client_name ? `
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 13px; color: var(--company-text-muted);">Client:</span>
                        <span>${escapeHtml(project.client_name)}</span>
                    </div>
                    ` : ''}
                    ${project.budget ? `
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 13px; color: var(--company-text-muted);">Budget:</span>
                        <span style="font-weight: 600;">$${parseFloat(project.budget).toFixed(2)}</span>
                    </div>
                    ` : ''}
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading projects:', error);
        grid.innerHTML = '<div class="loading-message">Error loading projects</div>';
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
    await loadCompanyTheme();
    await loadProjects();
    
    // Setup filter buttons
    const filterButtons = document.querySelectorAll('.filter-button');
    filterButtons.forEach(button => {
        button.addEventListener('click', async () => {
            // Update active state
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Load projects with filter
            const status = button.getAttribute('data-status');
            currentFilter = status;
            await loadProjects(status === 'all' ? null : status);
        });
    });
});
