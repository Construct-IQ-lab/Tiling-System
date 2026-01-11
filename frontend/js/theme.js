/**
 * Theme Management for Company Portal
 * Handles dynamic theming and branding
 */

/**
 * Load and apply company theme
 * @param {string} companySlug - Company slug
 */
async function loadCompanyTheme(companySlug) {
    try {
        const theme = await get(`/companies/${companySlug}/theme`);
        
        // Apply colors to CSS variables
        if (theme.primary_color) {
            document.documentElement.style.setProperty('--company-primary', theme.primary_color);
        }
        
        if (theme.secondary_color) {
            document.documentElement.style.setProperty('--company-secondary', theme.secondary_color);
        }
        
        // Update company logo if exists
        const logoElement = document.getElementById('company-logo');
        if (logoElement && theme.logo_url) {
            logoElement.src = theme.logo_url;
            logoElement.style.display = 'block';
        }
        
        // Update company name
        const nameElements = document.querySelectorAll('.company-name');
        nameElements.forEach(element => {
            element.textContent = theme.company_name;
        });
        
        // Update page title
        if (theme.company_name) {
            const currentTitle = document.title;
            if (currentTitle.includes('-')) {
                const pageName = currentTitle.split('-')[0].trim();
                document.title = `${pageName} - ${theme.company_name}`;
            } else {
                document.title = `${currentTitle} - ${theme.company_name}`;
            }
        }
        
        return theme;
    } catch (error) {
        console.error('Error loading company theme:', error);
        // Continue with default theme
    }
}

/**
 * Update navigation links with company slug
 * @param {string} companySlug - Company slug
 */
function updateNavigationLinks(companySlug) {
    const navLinks = document.querySelectorAll('[data-company-link]');
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && !href.includes('slug=')) {
            // Add slug as query parameter
            const separator = href.includes('?') ? '&' : '?';
            link.href = `${href}${separator}slug=${companySlug}`;
        }
    });
}

/**
 * Get company slug from URL
 * @returns {string|null} Company slug from URL or user data
 */
function getCompanySlugFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    let slug = urlParams.get('slug');
    
    // If not in URL, try to get from user data
    if (!slug) {
        slug = getCompanySlug();
    }
    
    return slug;
}

/**
 * Initialize company theme
 * Call this on company portal pages
 */
async function initializeCompanyTheme() {
    const companySlug = getCompanySlugFromUrl();
    
    if (!companySlug) {
        console.error('No company slug found');
        return;
    }
    
    // Load and apply theme
    await loadCompanyTheme(companySlug);
    
    // Update navigation links
    updateNavigationLinks(companySlug);
    
    // Store slug for future use
    sessionStorage.setItem('current_company_slug', companySlug);
}

/**
 * Apply theme colors to preview elements
 * Useful for profile/settings pages
 * @param {string} primaryColor - Primary color hex
 * @param {string} secondaryColor - Secondary color hex
 */
function applyThemePreview(primaryColor, secondaryColor) {
    if (primaryColor) {
        document.documentElement.style.setProperty('--company-primary', primaryColor);
        
        const primaryPreview = document.getElementById('primary-color-preview');
        if (primaryPreview) {
            primaryPreview.style.backgroundColor = primaryColor;
        }
    }
    
    if (secondaryColor) {
        document.documentElement.style.setProperty('--company-secondary', secondaryColor);
        
        const secondaryPreview = document.getElementById('secondary-color-preview');
        if (secondaryPreview) {
            secondaryPreview.style.backgroundColor = secondaryColor;
        }
    }
}

// Auto-initialize on company portal pages
document.addEventListener('DOMContentLoaded', () => {
    const isCompanyPage = window.location.pathname.includes('/company/');
    
    if (isCompanyPage) {
        initializeCompanyTheme();
    }
});
