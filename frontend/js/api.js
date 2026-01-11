// API Base URL - change this if your backend runs on a different host/port
const API_BASE_URL = 'http://localhost:8000/api/v1';

/**
 * API client for Tiling System backend
 */
class API {
    /**
     * Make a request to the API
     * @param {string} endpoint - API endpoint path
     * @param {object} options - Fetch options
     * @returns {Promise} Response data
     */
    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        };

        try {
            const response = await fetch(url, config);
            
            // Handle 204 No Content
            if (response.status === 204) {
                return null;
            }

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || `HTTP error! status: ${response.status}`);
            }

            return data;
        } catch (error) {
            console.error('API request error:', error);
            throw error;
        }
    }

    // Projects endpoints
    async getProjects(skip = 0, limit = 100) {
        return this.request(`/projects?skip=${skip}&limit=${limit}`);
    }

    async getProject(id) {
        return this.request(`/projects/${id}`);
    }

    async createProject(data) {
        return this.request('/projects/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async updateProject(id, data) {
        return this.request(`/projects/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    async deleteProject(id) {
        return this.request(`/projects/${id}`, {
            method: 'DELETE',
        });
    }

    // Calculations endpoints
    async calculateArea(length, width, unit = 'meters') {
        return this.request('/calculations/area', {
            method: 'POST',
            body: JSON.stringify({ length, width, unit }),
        });
    }

    async calculateMaterials(data) {
        return this.request('/calculations/materials', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async calculateCost(data) {
        return this.request('/calculations/cost', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }
}

// Export API instance
const api = new API();
