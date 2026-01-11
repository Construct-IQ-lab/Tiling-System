/**
 * Utility functions for Tiling System
 */

/**
 * Format date string to readable format
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date
 */
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

/**
 * Format date with time
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date and time
 */
function formatDateTime(dateString) {
    if (!dateString) return 'N/A';
    
    const date = new Date(dateString);
    const dateOptions = { year: 'numeric', month: 'short', day: 'numeric' };
    const timeOptions = { hour: '2-digit', minute: '2-digit' };
    
    return date.toLocaleDateString('en-US', dateOptions) + ' ' + 
           date.toLocaleTimeString('en-US', timeOptions);
}

/**
 * Format number as currency
 * @param {number} amount - Amount to format
 * @param {string} currency - Currency code (default: USD)
 * @returns {string} Formatted currency string
 */
function formatCurrency(amount, currency = 'USD') {
    if (amount === null || amount === undefined) return '$0.00';
    
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
    }).format(amount);
}

/**
 * Generate URL-safe slug from name
 * @param {string} name - Name to convert
 * @returns {string} URL-safe slug
 */
function generateSlug(name) {
    return name
        .toLowerCase()
        .trim()
        .replace(/[^\w\s-]/g, '')  // Remove special characters
        .replace(/[\s_-]+/g, '-')   // Replace spaces and underscores with hyphens
        .replace(/^-+|-+$/g, '');   // Remove leading/trailing hyphens
}

/**
 * Show toast notification
 * @param {string} message - Message to display
 * @param {string} type - Type of toast (success, error, warning, info)
 */
function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    // Add styles
    toast.style.position = 'fixed';
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.padding = '1rem 1.5rem';
    toast.style.borderRadius = '0.5rem';
    toast.style.zIndex = '10000';
    toast.style.animation = 'slideIn 0.3s ease-out';
    toast.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
    toast.style.minWidth = '250px';
    toast.style.maxWidth = '400px';
    
    // Set colors based on type
    const colors = {
        success: { bg: '#10B981', text: '#fff' },
        error: { bg: '#EF4444', text: '#fff' },
        warning: { bg: '#F59E0B', text: '#fff' },
        info: { bg: '#3B82F6', text: '#fff' }
    };
    
    const color = colors[type] || colors.info;
    toast.style.backgroundColor = color.bg;
    toast.style.color = color.text;
    
    // Add to document
    document.body.appendChild(toast);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

/**
 * Validate email address
 * @param {string} email - Email to validate
 * @returns {boolean} True if valid email
 */
function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

/**
 * Validate required field
 * @param {string} value - Value to validate
 * @returns {boolean} True if not empty
 */
function validateRequired(value) {
    return value !== null && value !== undefined && value.trim() !== '';
}

/**
 * Show loading spinner
 * @param {string} containerId - Container element ID
 */
function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = `
        <div style="text-align: center; padding: 2rem;">
            <div class="spinner"></div>
            <p style="margin-top: 1rem; color: var(--text-muted);">Loading...</p>
        </div>
    `;
}

/**
 * Show error message
 * @param {string} containerId - Container element ID
 * @param {string} message - Error message
 */
function showError(containerId, message) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = `
        <div class="alert alert-danger">
            <strong>Error:</strong> ${message}
        </div>
    `;
}

/**
 * Show success message
 * @param {string} containerId - Container element ID
 * @param {string} message - Success message
 */
function showSuccess(containerId, message) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = `
        <div class="alert alert-success">
            ${message}
        </div>
    `;
}

/**
 * Debounce function
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Get status badge HTML
 * @param {string} status - Status value
 * @returns {string} HTML for status badge
 */
function getStatusBadge(status) {
    const statusMap = {
        'active': 'success',
        'completed': 'success',
        'approved': 'success',
        'paid': 'success',
        'in_progress': 'info',
        'pending': 'warning',
        'sent': 'warning',
        'suspended': 'danger',
        'cancelled': 'danger',
        'overdue': 'danger',
        'draft': 'secondary'
    };
    
    const badgeType = statusMap[status.toLowerCase()] || 'secondary';
    const displayStatus = status.replace(/_/g, ' ').toUpperCase();
    
    return `<span class="badge badge-${badgeType}">${displayStatus}</span>`;
}

/**
 * Truncate text to specified length
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
function truncateText(text, maxLength) {
    if (!text || text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

/**
 * Get initials from name
 * @param {string} firstName - First name
 * @param {string} lastName - Last name
 * @returns {string} Initials
 */
function getInitials(firstName, lastName) {
    const first = firstName ? firstName.charAt(0).toUpperCase() : '';
    const last = lastName ? lastName.charAt(0).toUpperCase() : '';
    return first + last;
}

// Add CSS for toast animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
