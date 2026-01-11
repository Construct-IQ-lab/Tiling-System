// Admin Dashboard Logic

/**
 * Load admin dashboard statistics
 */
async function loadAdminDashboard() {
    try {
        const stats = await apiRequest('/admin/dashboard', 'GET', null, true);
        
        // Update stat cards
        updateStatCard('total-companies', stats.companies?.total || 0);
        updateStatCard('active-companies', stats.companies?.active || 0);
        updateStatCard('total-users', stats.users?.total || 0);
        updateStatCard('active-users', stats.users?.active || 0);
        updateStatCard('total-projects', stats.projects?.total || 0);
        updateStatCard('active-projects', stats.projects?.active || 0);
        
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
        showError('Failed to load dashboard statistics');
    }
}

/**
 * Update stat card value
 * @param {string} statId - Stat card element ID
 * @param {number} value - Value to display
 */
function updateStatCard(statId, value) {
    const element = document.getElementById(statId);
    if (element) {
        element.textContent = value;
    }
}

/**
 * Initialize admin dashboard
 */
document.addEventListener('DOMContentLoaded', () => {
    // Load dashboard stats if on admin index page
    if (window.location.pathname.includes('/admin/index.html')) {
        loadAdminDashboard();
    }
});
