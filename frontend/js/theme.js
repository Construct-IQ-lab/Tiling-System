// Theme Management for Company Portal

/**
 * Load and apply company theme
 * @param {string} slug - Company slug from URL or localStorage
 */
async function loadCompanyTheme(slug) {
    try {
        const theme = await companyAPI.getTheme(slug);
        
        // Apply CSS variables
        document.documentElement.style.setProperty('--company-primary', theme.primary_color);
        document.documentElement.style.setProperty('--company-secondary', theme.secondary_color);
        
        // Update logo if available
        const logoEl = document.getElementById('company-logo');
        if (logoEl && theme.logo_url) {
            logoEl.src = theme.logo_url;
            logoEl.style.display = 'block';
        } else if (logoEl) {
            logoEl.style.display = 'none';
        }
        
        // Update company name
        const nameEls = document.querySelectorAll('.company-name');
        nameEls.forEach(el => {
            el.textContent = theme.company_name;
        });
        
        // Update page title
        document.title = `${theme.company_name} - Tiling System`;
        
        // Update navigation links with correct slug
        updateNavigationLinks(slug);
        
        return theme;
    } catch (error) {
        console.error('Failed to load company theme:', error);
        showError('Failed to load company branding');
    }
}

/**
 * Update navigation links with company slug
 * @param {string} slug - Company slug
 */
function updateNavigationLinks(slug) {
    const links = {
        'nav-dashboard': `/frontend/company/index.html?slug=${slug}`,
        'nav-projects': `/frontend/company/projects.html?slug=${slug}`,
        'nav-calculator': `/frontend/company/calculator.html?slug=${slug}`,
        'nav-quotes': `/frontend/company/quotes.html?slug=${slug}`,
        'nav-profile': `/frontend/company/profile.html?slug=${slug}`
    };
    
    Object.entries(links).forEach(([id, href]) => {
        const link = document.getElementById(id);
        if (link) {
            link.href = href;
        }
    });
    
    // Highlight active page
    const currentPage = window.location.pathname.split('/').pop();
    Object.keys(links).forEach(id => {
        const link = document.getElementById(id);
        if (link && link.href.includes(currentPage)) {
            link.classList.add('active');
        }
    });
}

/**
 * Get company slug from URL parameters or localStorage
 */
function getSlugFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('slug') || localStorage.getItem('company_slug');
}

/**
 * Initialize theme on page load
 * Call this function when the page loads on company portal pages
 */
async function initTheme() {
    const slug = getSlugFromURL();
    if (slug) {
        await loadCompanyTheme(slug);
    } else {
        showError('Company information not found');
        setTimeout(() => {
            window.location.href = '/frontend/auth/login.html';
        }, 2000);
    }
}
