/**
 * Dashboard functionality
 */

// Load projects and update statistics
async function loadDashboard() {
    try {
        const projects = await api.getProjects();
        updateStatistics(projects);
    } catch (error) {
        console.error('Error loading dashboard:', error);
        // Show zeros if API is not available
        updateStatistics([]);
    }
}

/**
 * Calculate and display statistics
 * @param {Array} projects - Array of project objects
 */
function updateStatistics(projects) {
    const total = projects.length;
    const active = projects.filter(p => 
        p.status === 'planning' || p.status === 'in-progress'
    ).length;
    const completed = projects.filter(p => p.status === 'completed').length;

    document.getElementById('stat-total').textContent = total;
    document.getElementById('stat-active').textContent = active;
    document.getElementById('stat-completed').textContent = completed;
}

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', loadDashboard);
