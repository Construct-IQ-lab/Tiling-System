// Company Dashboard Functions

/**
 * Load and display company dashboard statistics
 */
async function loadCompanyDashboard() {
    const slug = getSlugFromURL();
    if (!slug) {
        showError('Company information not found');
        return;
    }
    
    try {
        const stats = await companyAPI.getDashboard(slug);
        
        // Update stat cards
        document.getElementById('total-projects').textContent = stats.total_projects;
        document.getElementById('active-projects').textContent = stats.active_projects;
        document.getElementById('completed-projects').textContent = stats.completed_projects;
    } catch (error) {
        console.error('Failed to load dashboard stats:', error);
        showError('Failed to load dashboard statistics');
    }
}

// Initialize dashboard when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        initTheme().then(() => loadCompanyDashboard());
    });
} else {
    initTheme().then(() => loadCompanyDashboard());
}
