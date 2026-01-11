// Company Dashboard Logic

/**
 * Load company dashboard statistics
 */
async function loadCompanyDashboard() {
    const companySlug = getCompanySlugFromUrl() || localStorage.getItem('company_slug');
    
    if (!companySlug) {
        showError('Company not found');
        return;
    }
    
    try {
        const stats = await apiRequest(`/companies/${companySlug}/dashboard`, 'GET', null, true);
        
        // Update stat cards
        updateStatCard('total-projects', stats.projects?.total || 0);
        updateStatCard('active-projects', stats.projects?.active || 0);
        updateStatCard('completed-projects', stats.projects?.completed || 0);
        
    } catch (error) {
        console.error('Error loading company dashboard:', error);
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
 * Initialize company dashboard
 */
document.addEventListener('DOMContentLoaded', () => {
    // Load dashboard stats if on company index page
    if (window.location.pathname.includes('index.html') && !window.location.pathname.includes('/admin/')) {
        loadCompanyDashboard();
    }
});
