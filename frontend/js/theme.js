// Dynamic Theme Loading for Company Portals

/**
 * Load and apply company theme
 * @param {string} companySlug - Company slug from URL or localStorage
 */
async function loadCompanyTheme(companySlug) {
    if (!companySlug) {
        companySlug = getCompanySlugFromUrl() || localStorage.getItem('company_slug');
    }
    
    if (!companySlug) {
        console.error('No company slug found');
        return;
    }
    
    try {
        const theme = await apiRequest(`/companies/${companySlug}/theme`, 'GET', null, true);
        
        // Apply CSS variables for theme colors
        document.documentElement.style.setProperty('--company-primary', theme.primary_color);
        document.documentElement.style.setProperty('--company-secondary', theme.secondary_color);
        
        // Update company name in navigation
        const companyNameElements = document.querySelectorAll('.company-name');
        companyNameElements.forEach(el => {
            el.textContent = theme.company_name;
        });
        
        // Update company logo if exists
        if (theme.logo_url) {
            const logoElements = document.querySelectorAll('.company-logo');
            logoElements.forEach(el => {
                el.src = theme.logo_url;
                el.alt = `${theme.company_name} Logo`;
                el.style.display = 'block';
            });
        }
        
        // Update page title
        const pageTitle = document.querySelector('title');
        if (pageTitle && !pageTitle.textContent.includes(theme.company_name)) {
            pageTitle.textContent = `${theme.company_name} - ${pageTitle.textContent}`;
        }
        
        // Update navigation links with company slug
        updateNavigationLinks(companySlug);
        
    } catch (error) {
        console.error('Error loading company theme:', error);
        showError('Failed to load company theme');
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
    if (match && match[1] !== 'admin' && match[1] !== 'auth') {
        return match[1];
    }
    
    return null;
}

/**
 * Update navigation links with company slug
 * @param {string} companySlug - Company slug
 */
function updateNavigationLinks(companySlug) {
    const navLinks = document.querySelectorAll('[data-nav-link]');
    
    navLinks.forEach(link => {
        const page = link.getAttribute('data-nav-link');
        link.href = `/${companySlug}/${page}`;
    });
    
    // Update active link based on current page
    const currentPage = window.location.pathname.split('/').pop();
    navLinks.forEach(link => {
        const linkPage = link.getAttribute('data-nav-link');
        if (currentPage === linkPage) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

/**
 * Initialize theme on page load for company portal pages
 */
document.addEventListener('DOMContentLoaded', () => {
    const isCompanyPage = window.location.pathname.includes('/') && 
                          !window.location.pathname.includes('/admin/') && 
                          !window.location.pathname.includes('/auth/');
    
    if (isCompanyPage) {
        const companySlug = getCompanySlugFromUrl();
        if (companySlug) {
            loadCompanyTheme(companySlug);
        }
    }
});
