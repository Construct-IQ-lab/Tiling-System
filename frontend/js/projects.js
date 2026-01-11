/**
 * Projects page functionality
 */

// Load projects on page load
document.addEventListener('DOMContentLoaded', loadProjects);

/**
 * Load and display all projects
 */
async function loadProjects() {
    try {
        const projects = await api.getProjects();
        displayProjects(projects);
    } catch (error) {
        console.error('Error loading projects:', error);
        document.getElementById('projects-grid').innerHTML = 
            '<p style="text-align: center; color: #666;">Failed to load projects. Make sure the backend is running.</p>';
    }
}

/**
 * Display projects in grid
 * @param {Array} projects - Array of project objects
 */
function displayProjects(projects) {
    const grid = document.getElementById('projects-grid');
    
    if (projects.length === 0) {
        grid.innerHTML = '<p style="text-align: center; color: #666;">No projects yet. Create your first project!</p>';
        return;
    }
    
    grid.innerHTML = projects.map(project => `
        <div class="project-card">
            <h3>${project.name}</h3>
            <p>${project.description || 'No description'}</p>
            <p><strong>Client:</strong> ${project.client_name || 'N/A'}</p>
            <p><strong>Area:</strong> ${project.area ? project.area + ' m²' : 'N/A'}</p>
            <p><strong>Budget:</strong> ${project.budget ? '$' + project.budget.toFixed(2) : 'N/A'}</p>
            <div class="project-card-footer">
                <span class="status-badge status-${project.status}">${formatStatus(project.status)}</span>
                <button class="btn btn-danger" onclick="deleteProjectHandler(${project.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

/**
 * Format status for display
 * @param {string} status - Status string
 * @returns {string} Formatted status
 */
function formatStatus(status) {
    return status.split('-').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

/**
 * Show create project form
 */
function showCreateForm() {
    document.getElementById('create-modal').classList.add('active');
}

/**
 * Hide create project form
 */
function hideCreateForm() {
    document.getElementById('create-modal').classList.remove('active');
    document.getElementById('create-project-form').reset();
}

/**
 * Create project form submission
 */
document.getElementById('create-project-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const projectData = {
        name: document.getElementById('project-name').value,
        description: document.getElementById('project-description').value || null,
        client_name: document.getElementById('client-name').value || null,
        client_contact: document.getElementById('client-contact').value || null,
        client_address: document.getElementById('client-address').value || null,
        area: parseFloat(document.getElementById('project-area').value) || null,
        budget: parseFloat(document.getElementById('project-budget').value) || null,
        status: document.getElementById('project-status').value
    };
    
    try {
        await api.createProject(projectData);
        hideCreateForm();
        loadProjects();
        alert('Project created successfully!');
    } catch (error) {
        alert('Error creating project: ' + error.message);
    }
});

/**
 * Delete project handler
 * @param {number} id - Project ID
 */
async function deleteProjectHandler(id) {
    if (!confirm('Are you sure you want to delete this project?')) {
        return;
    }
    
    try {
        await api.deleteProject(id);
        loadProjects();
        alert('Project deleted successfully!');
    } catch (error) {
        alert('Error deleting project: ' + error.message);
    }
}

// Close modal when clicking outside
document.getElementById('create-modal').addEventListener('click', (e) => {
    if (e.target.id === 'create-modal') {
        hideCreateForm();
    }
});
