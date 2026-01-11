// Admin Dashboard JavaScript

const API_URL = 'http://localhost:8000';

// Load dashboard statistics
async function loadDashboardStats() {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/api/admin/dashboard/stats`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to load dashboard stats');
        }
        
        const stats = await response.json();
        
        // Update stat values
        document.getElementById('totalCompanies').textContent = stats.total_companies;
        document.getElementById('activeCompanies').textContent = stats.active_companies;
        document.getElementById('totalUsers').textContent = stats.total_users;
        document.getElementById('totalProjects').textContent = stats.total_projects;
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
        // Set default values on error
        document.getElementById('totalCompanies').textContent = '0';
        document.getElementById('activeCompanies').textContent = '0';
        document.getElementById('totalUsers').textContent = '0';
        document.getElementById('totalProjects').textContent = '0';
    }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
    await loadDashboardStats();
});
