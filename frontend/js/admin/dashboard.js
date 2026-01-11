/**
 * Admin Dashboard Script
 * Handles loading and displaying admin dashboard data
 */

/**
 * Load admin dashboard statistics
 */
async function loadAdminDashboard() {
    try {
        showLoading('stats-container');
        
        const stats = await get('/admin/dashboard');
        
        // Update stats cards
        updateStatsCards(stats);
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showError('stats-container', 'Failed to load dashboard statistics');
        showToast('Failed to load dashboard data', 'error');
    }
}

/**
 * Update stats cards with data
 * @param {object} stats - Statistics data
 */
function updateStatsCards(stats) {
    const container = document.getElementById('stats-container');
    
    const html = `
        <div class="stat-card">
            <div class="stat-card-label">Total Companies</div>
            <div class="stat-card-value">${stats.companies?.total || 0}</div>
            <div class="stat-card-subtitle">${stats.companies?.active || 0} active</div>
        </div>
        
        <div class="stat-card secondary">
            <div class="stat-card-label">Total Projects</div>
            <div class="stat-card-value">${stats.projects?.total || 0}</div>
            <div class="stat-card-subtitle">${stats.projects?.active || 0} in progress</div>
        </div>
        
        <div class="stat-card warning">
            <div class="stat-card-label">Total Users</div>
            <div class="stat-card-value">${stats.users?.total || 0}</div>
            <div class="stat-card-subtitle">${stats.users?.active || 0} active</div>
        </div>
    `;
    
    container.innerHTML = html;
}

/**
 * Initialize dashboard
 */
function initDashboard() {
    // Highlight active nav item
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        if (link.href.includes('index.html')) {
            link.classList.add('active');
        }
    });
    
    // Load dashboard data
    loadAdminDashboard();
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initDashboard);
