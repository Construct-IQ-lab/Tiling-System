// Company Dashboard JavaScript

const API_URL = 'http://localhost:8000';

// Load company dashboard data
async function loadCompanyDashboard() {
    const user = JSON.parse(localStorage.getItem('user'));
    const token = localStorage.getItem('token');
    const slug = user.company_slug;
    
    if (!slug) {
        console.error('No company slug found');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/api/companies/${slug}/dashboard`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to load dashboard');
        }
        
        const dashboard = await response.json();
        
        // Update stat values
        document.getElementById('totalProjects').textContent = dashboard.total_projects;
        document.getElementById('activeProjects').textContent = dashboard.active_projects;
        document.getElementById('completedProjects').textContent = dashboard.completed_projects;
        document.getElementById('totalUsers').textContent = dashboard.total_users;
        
        // Load recent projects
        await loadRecentProjects(slug);
    } catch (error) {
        console.error('Error loading dashboard:', error);
        document.getElementById('totalProjects').textContent = '0';
        document.getElementById('activeProjects').textContent = '0';
        document.getElementById('completedProjects').textContent = '0';
        document.getElementById('totalUsers').textContent = '0';
    }
}

// Load recent projects
async function loadRecentProjects(slug) {
    const token = localStorage.getItem('token');
    const container = document.getElementById('recentProjects');
    
    try {
        const response = await fetch(`${API_URL}/api/companies/${slug}/projects?limit=5`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to load projects');
        }
        
        const projects = await response.json();
        
        if (projects.length === 0) {
            container.innerHTML = '<div class="loading-message">No projects yet. Create your first project!</div>';
            return;
        }
        
        container.innerHTML = projects.map(project => `
            <div class="project-item">
                <h3>${escapeHtml(project.name)}</h3>
                <p>${escapeHtml(project.description || 'No description')}</p>
                <div style="margin-top: 8px; font-size: 13px; color: var(--company-text-muted);">
                    Status: <strong>${escapeHtml(project.status)}</strong> | 
                    Client: <strong>${escapeHtml(project.client_name || 'N/A')}</strong>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading projects:', error);
        container.innerHTML = '<div class="loading-message">Error loading projects</div>';
    }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
    await loadCompanyTheme();
    await loadCompanyDashboard();
});
