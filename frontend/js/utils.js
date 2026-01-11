// HTML Sanitization utility

/**
 * Escape HTML special characters to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} - Escaped text
 */
function escapeHtml(text) {
    if (text === null || text === undefined) {
        return '';
    }
    
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Create a safe HTML element with escaped text content
 * @param {string} tag - HTML tag name
 * @param {string} text - Text content to escape
 * @param {object} attributes - Optional attributes
 * @returns {string} - Safe HTML string
 */
function createSafeElement(tag, text, attributes = {}) {
    const escapedText = escapeHtml(text);
    const attrs = Object.entries(attributes)
        .map(([key, value]) => `${key}="${escapeHtml(value)}"`)
        .join(' ');
    
    return `<${tag}${attrs ? ' ' + attrs : ''}>${escapedText}</${tag}>`;
}

// Make functions available globally
window.escapeHtml = escapeHtml;
window.createSafeElement = createSafeElement;
