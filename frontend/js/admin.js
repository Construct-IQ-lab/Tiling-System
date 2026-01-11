// Admin Dashboard Functions

/**
 * Load and display admin dashboard statistics
 */
async function loadAdminDashboard() {
    try {
        const stats = await adminAPI.getDashboardStats();
        
        // Update stat cards
        document.getElementById('total-companies').textContent = stats.total_companies;
        document.getElementById('total-projects').textContent = stats.total_projects;
        document.getElementById('total-users').textContent = stats.total_users;
    } catch (error) {
        console.error('Failed to load dashboard stats:', error);
        showError('Failed to load dashboard statistics');
    }
}

// Initialize dashboard when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadAdminDashboard);
} else {
    loadAdminDashboard();
}
