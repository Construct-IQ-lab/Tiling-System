// Theme JavaScript - Dynamic Company Theming

const API_URL = 'http://localhost:8000';

// Load and apply company theme
async function loadCompanyTheme() {
    const user = JSON.parse(localStorage.getItem('user'));
    const token = localStorage.getItem('token');
    
    if (!user || !user.company_slug) {
        console.error('No company slug found');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/api/companies/${user.company_slug}/theme`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to load theme');
        }
        
        const theme = await response.json();
        
        // Apply CSS variables
        document.documentElement.style.setProperty('--company-primary', theme.primary_color);
        document.documentElement.style.setProperty('--company-secondary', theme.secondary_color);
        
        // Update company name
        const companyNameElement = document.getElementById('companyName');
        if (companyNameElement) {
            companyNameElement.textContent = theme.name; // Use textContent to prevent XSS
        }
        
        // Update company logo
        const companyLogoElement = document.getElementById('companyLogo');
        if (companyLogoElement && theme.logo_url) {
            // Validate logo URL is a valid image URL
            const img = document.createElement('img');
            img.src = theme.logo_url;
            img.alt = escapeHtml(theme.name);
            companyLogoElement.innerHTML = '';
            companyLogoElement.appendChild(img);
        }
        
        // Update navigation links with company slug
        updateNavigationLinks(theme.slug);
        
        return theme;
    } catch (error) {
        console.error('Error loading theme:', error);
        return null;
    }
}

// Update navigation links to include company slug
function updateNavigationLinks(slug) {
    const navItems = document.querySelectorAll('.nav-item[data-page]');
    navItems.forEach(item => {
        const page = item.getAttribute('data-page');
        // For company portal, links are relative
        if (page === 'dashboard') {
            item.href = 'index.html';
        } else {
            item.href = `${page}.html`;
        }
    });
}

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', async () => {
    const user = JSON.parse(localStorage.getItem('user'));
    
    // Only load theme for company users
    if (user && user.company_slug) {
        await loadCompanyTheme();
    }
});
